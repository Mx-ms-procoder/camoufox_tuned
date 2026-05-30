/*
Camoufox uTLS Sidecar Proxy — MitM-capable TLS fingerprint proxy.

STATUS: EXPERIMENTAL.
No registered TLS profile in pythonlib/camoufox/tls_profiles.py currently sets
transport_mode="utls-sidecar", so the standard Python launch path
(launch_options()) never routes traffic through this binary. The sidecar
builds and is invocable manually, but it is not part of the operational
identity pipeline. See AUDIT_2026-05-15.md (priority fix #2) before depending
on it for stealth claims.

Modes (CAMOU_UTLS_MODE):

	"transparent" — Raw TCP relay for CONNECT. Browser's NSS handles TLS. (default)
	"mitm"        — Full MitM: terminate browser TLS, re-establish with uTLS to target.

Environment variables:

	CAMOU_UTLS_PROFILE       : Fallback profile ID (default "firefox150")
	CAMOU_UTLS_LISTEN        : Listen address (default "127.0.0.1:8080")
	CAMOU_UTLS_DEBUG         : "1" to enable debug logging
	CAMOU_UTLS_MODE          : "transparent" or "mitm"
	CAMOU_UTLS_IDENTITY_JSON : JSON blob from IdentityCoherenceEngine for custom ClientHelloSpec
	CAMOU_UTLS_CA_CERT       : Path to CA certificate PEM (for mitm mode)
	CAMOU_UTLS_CA_KEY        : Path to CA private key PEM (for mitm mode)
*/
package main

import (
	"context"
	"crypto"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"io"
	"log"
	"math/big"
	"net"
	"net/http"
	"os"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	utls "github.com/refraction-networking/utls"
	"golang.org/x/net/http2"
)

// ── Identity JSON schema ────────────────────────────────────────────

type IdentityTLS struct {
	CipherSuiteCodes []uint16 `json:"cipherSuiteCodes"`
	ExtensionCodes   []uint16 `json:"extensionCodes"`
	NamedGroupCodes  []uint16 `json:"namedGroupCodes"`
	SigAlgCodes      []uint16 `json:"sigAlgCodes"`
	ALPN             []string `json:"alpn"`
}

type IdentityHTTP2 struct {
	HeaderTableSize   uint32 `json:"headerTableSize"`
	EnablePush        uint32 `json:"enablePush"`
	InitialWindowSize uint32 `json:"initialWindowSize"`
	MaxFrameSize      uint32 `json:"maxFrameSize"`
	WindowUpdate      uint32 `json:"windowUpdate"`
}

type IdentityBlob struct {
	TLS   IdentityTLS   `json:"tls"`
	HTTP2 IdentityHTTP2 `json:"http2"`
}

// ── Certificate Authority ───────────────────────────────────────────

type mitmCA struct {
	cert    *x509.Certificate
	key     crypto.PrivateKey
	certPEM []byte
	mu      sync.RWMutex
	cache   map[string]*tls.Certificate
	// inflight de-duplicates concurrent certFor() calls for the same
	// hostname. Without this, N parallel CONNECTs to the same host
	// would each generate a fresh ECDSA keypair + cert (a "cert
	// generation storm") because the RLock-then-Lock pattern lets
	// multiple goroutines miss the cache simultaneously.
	inflight map[string]*certFlight
}

type certFlight struct {
	done chan struct{}
	cert *tls.Certificate
	err  error
}

func newMitmCA(certPath, keyPath string) (*mitmCA, error) {
	if certPath != "" && keyPath != "" {
		return loadMitmCA(certPath, keyPath)
	}
	return generateMitmCA()
}

func generateMitmCA() (*mitmCA, error) {
	key, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		return nil, fmt.Errorf("generate CA key: %w", err)
	}
	serial, _ := rand.Int(rand.Reader, new(big.Int).Lsh(big.NewInt(1), 128))
	tmpl := &x509.Certificate{
		SerialNumber:          serial,
		Subject:               pkix.Name{Organization: []string{"Camoufox Local CA"}, CommonName: "Camoufox MitM CA"},
		NotBefore:             time.Now().Add(-24 * time.Hour),
		NotAfter:              time.Now().Add(3 * 365 * 24 * time.Hour),
		KeyUsage:              x509.KeyUsageCertSign | x509.KeyUsageCRLSign,
		BasicConstraintsValid: true,
		IsCA:                  true,
		MaxPathLen:            0,
	}
	certDER, err := x509.CreateCertificate(rand.Reader, tmpl, tmpl, &key.PublicKey, key)
	if err != nil {
		return nil, fmt.Errorf("create CA cert: %w", err)
	}
	cert, err := x509.ParseCertificate(certDER)
	if err != nil {
		return nil, err
	}
	certPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: certDER})
	log.Printf("[INFO] Generated ephemeral MitM CA (expires %s)", tmpl.NotAfter.Format("2006-01-02"))
	return &mitmCA{
		cert:     cert,
		key:      key,
		certPEM:  certPEM,
		cache:    make(map[string]*tls.Certificate),
		inflight: make(map[string]*certFlight),
	}, nil
}

func loadMitmCA(certPath, keyPath string) (*mitmCA, error) {
	certPEM, err := os.ReadFile(certPath)
	if err != nil {
		return nil, fmt.Errorf("read CA cert: %w", err)
	}
	keyPEM, err := os.ReadFile(keyPath)
	if err != nil {
		return nil, fmt.Errorf("read CA key: %w", err)
	}
	block, _ := pem.Decode(certPEM)
	if block == nil {
		return nil, fmt.Errorf("decode CA cert: no PEM block found")
	}
	cert, err := x509.ParseCertificate(block.Bytes)
	if err != nil {
		return nil, err
	}
	key, err := parsePrivateKeyPEM(keyPEM)
	if err != nil {
		return nil, err
	}
	log.Printf("[INFO] Loaded MitM CA from %s", certPath)
	return &mitmCA{
		cert:     cert,
		key:      key,
		certPEM:  certPEM,
		cache:    make(map[string]*tls.Certificate),
		inflight: make(map[string]*certFlight),
	}, nil
}

func parsePrivateKeyPEM(keyPEM []byte) (crypto.PrivateKey, error) {
	keyBlock, _ := pem.Decode(keyPEM)
	if keyBlock == nil {
		return nil, fmt.Errorf("decode CA key: no PEM block found")
	}
	if key, err := x509.ParseECPrivateKey(keyBlock.Bytes); err == nil {
		return key, nil
	}
	if key, err := x509.ParsePKCS1PrivateKey(keyBlock.Bytes); err == nil {
		return key, nil
	}
	key, err := x509.ParsePKCS8PrivateKey(keyBlock.Bytes)
	if err != nil {
		return nil, fmt.Errorf("parse CA key: unsupported private key format")
	}
	switch typed := key.(type) {
	case *ecdsa.PrivateKey:
		return typed, nil
	case *rsa.PrivateKey:
		return typed, nil
	default:
		return nil, fmt.Errorf("parse CA key: unsupported private key type %T", key)
	}
}

func (ca *mitmCA) certFor(hostname string) (*tls.Certificate, error) {
	// Fast path: cache hit under read lock.
	ca.mu.RLock()
	if cached, ok := ca.cache[hostname]; ok {
		ca.mu.RUnlock()
		return cached, nil
	}
	ca.mu.RUnlock()

	// Slow path: take the write lock, re-check the cache (another
	// goroutine may have populated it during the lock upgrade), and
	// either claim the flight for this hostname or wait on an existing
	// one. Singleflight ensures only ONE goroutine generates the cert
	// for a given hostname under concurrent load.
	ca.mu.Lock()
	if cached, ok := ca.cache[hostname]; ok {
		ca.mu.Unlock()
		return cached, nil
	}
	if flight, ok := ca.inflight[hostname]; ok {
		ca.mu.Unlock()
		<-flight.done
		return flight.cert, flight.err
	}
	flight := &certFlight{done: make(chan struct{})}
	ca.inflight[hostname] = flight
	ca.mu.Unlock()

	// Generate the cert without holding the lock so other hostnames
	// remain unblocked. Result is committed under the lock below.
	tlsCert, err := ca.generateCertFor(hostname)
	flight.cert = tlsCert
	flight.err = err

	ca.mu.Lock()
	delete(ca.inflight, hostname)
	if err == nil {
		if len(ca.cache) > 4096 {
			ca.cache = make(map[string]*tls.Certificate) // evict all on overflow
		}
		ca.cache[hostname] = tlsCert
	}
	ca.mu.Unlock()

	close(flight.done)
	return tlsCert, err
}

// generateCertFor mints a fresh leaf certificate for the given hostname
// signed by the in-memory CA. Must NOT be called while holding ca.mu.
func (ca *mitmCA) generateCertFor(hostname string) (*tls.Certificate, error) {
	key, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		return nil, err
	}
	serial, _ := rand.Int(rand.Reader, new(big.Int).Lsh(big.NewInt(1), 128))
	tmpl := &x509.Certificate{
		SerialNumber: serial,
		Subject:      pkix.Name{CommonName: hostname},
		NotBefore:    time.Now().Add(-1 * time.Hour),
		NotAfter:     time.Now().Add(24 * time.Hour),
		KeyUsage:     x509.KeyUsageDigitalSignature,
		ExtKeyUsage:  []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
	}
	if ip := net.ParseIP(hostname); ip != nil {
		tmpl.IPAddresses = []net.IP{ip}
	} else {
		tmpl.DNSNames = []string{hostname}
	}
	certDER, err := x509.CreateCertificate(rand.Reader, tmpl, ca.cert, &key.PublicKey, ca.key)
	if err != nil {
		return nil, err
	}
	return &tls.Certificate{
		Certificate: [][]byte{certDER, ca.cert.Raw},
		PrivateKey:  key,
	}, nil
}

// ── Built-in Firefox identity defaults ──────────────────────────────
//
// T3.2 (audit 2026-05-25): the sidecar previously fell through to
// utls.HelloFirefox_120 for every Firefox release >= 135 because
// upstream utls ships no preset for them. That made the JA4 fingerprint
// match Firefox 120 — provably wrong for any Camoufox launched as 135+.
//
// These constants mirror the cipher / extension / curve order from
// pythonlib/camoufox/tls_profiles.FIREFOX_135_TLS, which is the
// baseline NSS uses for every supported Firefox version up to 150
// (NSS source verified: no order change between 135 and 150). With
// no CAMOU_UTLS_IDENTITY_JSON supplied the sidecar synthesises a blob
// from these defaults so buildCustomSpec runs the modern path instead
// of the 120 fallback. When the launcher DOES pass an identity blob
// (the normal Camoufox flow) that takes precedence as before.

// firefoxBaselineIdentity returns the static FF135-derived identity used
// for every modern Firefox profile in the absence of a runtime blob.
// Keep this in lockstep with FIREFOX_135_TLS in tls_profiles.py.
func firefoxBaselineIdentity() *IdentityBlob {
	return &IdentityBlob{
		TLS: IdentityTLS{
			CipherSuiteCodes: []uint16{
				0x1301, 0x1303, 0x1302,
				0xc02b, 0xc02f, 0xcca9, 0xcca8,
				0xc02c, 0xc030,
				0xc00a, 0xc009, 0xc013, 0xc014,
				0x009c, 0x009d, 0x002f, 0x0035,
			},
			ExtensionCodes: []uint16{
				0, 23, 65281, 10, 11, 35, 16, 5, 34, 51, 43, 13, 45, 28, 21,
			},
			NamedGroupCodes: []uint16{
				// Firefox 132+: mlkem768x25519 (0x11ec) inserted after secp521r1.
				// Keep in lockstep with FIREFOX_135_TLS.namedGroupCodes in tls_profiles.py.
				0x001d, 0x0017, 0x0018, 0x0019, 0x11ec, 0x0100, 0x0101,
			},
			SigAlgCodes: []uint16{
				0x0403, 0x0503, 0x0603,
				0x0804, 0x0805, 0x0806,
				0x0401, 0x0501, 0x0601,
				0x0203, 0x0201,
			},
			ALPN: []string{"h2", "http/1.1"},
		},
		HTTP2: IdentityHTTP2{
			HeaderTableSize:   65536,
			EnablePush:        0,
			InitialWindowSize: 131072,
			MaxFrameSize:      16384,
			WindowUpdate:      12517377, // 12 MiB session bump, matches FF135+
		},
	}
}

// ── Custom ClientHelloSpec builder ──────────────────────────────────

func buildCustomSpec(id *IdentityBlob) *utls.ClientHelloSpec {
	if id == nil || len(id.TLS.CipherSuiteCodes) == 0 {
		return nil
	}

	// Build cipher suites
	suites := make([]uint16, len(id.TLS.CipherSuiteCodes))
	copy(suites, id.TLS.CipherSuiteCodes)

	// Build named groups (curves)
	var curves []utls.CurveID
	for _, code := range id.TLS.NamedGroupCodes {
		curves = append(curves, utls.CurveID(code))
	}
	if len(curves) == 0 {
		curves = []utls.CurveID{utls.X25519, utls.CurveP256, utls.CurveP384}
	}

	// Build signature algorithms
	var sigAlgs []utls.SignatureScheme
	for _, code := range id.TLS.SigAlgCodes {
		sigAlgs = append(sigAlgs, utls.SignatureScheme(code))
	}

	// Build key shares (Firefox 132+: x25519 + mlkem768x25519 PQ hybrid).
	// Do NOT take the first 2 from the supported_groups list — after inserting
	// 0x11ec at position 4, that would pick secp256r1 instead of mlkem768x25519.
	var keyShares []utls.KeyShareExtension
	if len(curves) > 0 {
		ks := utls.KeyShareExtension{KeyShares: []utls.KeyShare{}}
		for _, target := range []utls.CurveID{utls.CurveID(0x001d), utls.CurveID(0x11ec)} {
			for _, c := range curves {
				if c == target {
					ks.KeyShares = append(ks.KeyShares, utls.KeyShare{Group: target})
					break
				}
			}
		}
		if len(ks.KeyShares) == 0 {
			ks.KeyShares = append(ks.KeyShares, utls.KeyShare{Group: curves[0]})
		}
		keyShares = append(keyShares, ks)
	}

	// ALPN
	alpn := id.TLS.ALPN
	if len(alpn) == 0 {
		alpn = []string{"h2", "http/1.1"}
	}

	// Build extensions list (Firefox 150 order — same as 135 baseline,
	// no observed reordering in upstream Mozilla NSS handshake between
	// 135 and 150. Re-capture if behavioural drift is suspected.)
	extensions := []utls.TLSExtension{
		&utls.SNIExtension{},
		&utls.ExtendedMasterSecretExtension{},
		&utls.RenegotiationInfoExtension{Renegotiation: utls.RenegotiateOnceAsClient},
		&utls.SupportedCurvesExtension{Curves: curves},
		&utls.SupportedPointsExtension{SupportedPoints: []byte{0}}, // uncompressed
		&utls.SessionTicketExtension{},
		&utls.ALPNExtension{AlpnProtocols: alpn},
		&utls.StatusRequestExtension{},
		&utls.DelegatedCredentialsExtension{
			SupportedSignatureAlgorithms: sigAlgs,
		},
	}

	if len(keyShares) > 0 {
		extensions = append(extensions, &keyShares[0])
	}

	extensions = append(extensions,
		&utls.SupportedVersionsExtension{Versions: []uint16{utls.VersionTLS13, utls.VersionTLS12}},
		&utls.SignatureAlgorithmsExtension{SupportedSignatureAlgorithms: sigAlgs},
		&utls.PSKKeyExchangeModesExtension{Modes: []uint8{utls.PskModeDHE}},
		&utls.FakeRecordSizeLimitExtension{Limit: 0x4001},
		&utls.UtlsPaddingExtension{GetPaddingLen: utls.BoringPaddingStyle},
	)

	return &utls.ClientHelloSpec{
		TLSVersMax:         utls.VersionTLS13,
		TLSVersMin:         utls.VersionTLS12,
		CipherSuites:       suites,
		CompressionMethods: []byte{0},
		Extensions:         extensions,
	}
}

// ── Proxy Server ────────────────────────────────────────────────────

type proxyServer struct {
	mu            sync.RWMutex
	profileName   string
	identity      *IdentityBlob
	customSpec    *utls.ClientHelloSpec
	fallbackHello utls.ClientHelloID
	debug         bool
	mitmMode      bool
	ca            *mitmCA
	connCount     atomic.Int64
	transport     *http.Transport
}

// defaultProfileSpec maps Camoufox profile IDs to the closest static utls
// ClientHello preset. This is now only the *last-resort* fallback for
// pre-135 profiles. Profiles >= 135 synthesise a ClientHelloSpec from
// firefoxBaselineIdentity() instead (see modernFirefoxProfiles) so the
// JA4 fingerprint matches the Firefox-family TLS handshake rather than
// the obsolete Firefox 120 preset.
var defaultProfileSpec = map[string]utls.ClientHelloID{
	"firefox105": utls.HelloFirefox_105,
	"firefox120": utls.HelloFirefox_120,
}

// modernFirefoxProfiles lists profile IDs that synthesise a Firefox 135+
// ClientHelloSpec from firefoxBaselineIdentity() when no runtime blob
// is supplied. Without this map these profiles would fall back to
// HelloFirefox_120 — provably wrong on the wire.
var modernFirefoxProfiles = map[string]bool{
	"firefox135": true,
	"firefox140": true,
	"firefox146": true,
	"firefox150": true,
}

func newProxyServer(profileName string, debug, mitmMode bool, ca *mitmCA) *proxyServer {
	helloID, ok := defaultProfileSpec[profileName]
	if !ok {
		helloID = utls.HelloFirefox_120
	}
	ps := &proxyServer{
		profileName:   profileName,
		fallbackHello: helloID,
		debug:         debug,
		mitmMode:      mitmMode,
		ca:            ca,
	}
	// Load identity JSON if present
	if raw := os.Getenv("CAMOU_UTLS_IDENTITY_JSON"); raw != "" {
		var blob IdentityBlob
		if err := json.Unmarshal([]byte(raw), &blob); err != nil {
			log.Printf("[WARN] Failed to parse CAMOU_UTLS_IDENTITY_JSON: %v", err)
		} else {
			ps.identity = &blob
			ps.customSpec = buildCustomSpec(&blob)
			if ps.customSpec != nil {
				log.Printf("[INFO] Loaded custom ClientHelloSpec from identity blob (%d ciphers, %d groups)",
					len(blob.TLS.CipherSuiteCodes), len(blob.TLS.NamedGroupCodes))
			}
		}
	}

	// T3.2 (audit 2026-05-25): for modern Firefox profiles without a
	// runtime identity blob, synthesise one from firefoxBaselineIdentity()
	// instead of silently downgrading to the static HelloFirefox_120
	// preset (which produces a Firefox 120 JA4 fingerprint regardless
	// of the profile name).
	if ps.customSpec == nil && modernFirefoxProfiles[profileName] {
		blob := firefoxBaselineIdentity()
		ps.identity = blob
		ps.customSpec = buildCustomSpec(blob)
		if ps.customSpec != nil {
			log.Printf("[INFO] Profile %q has no CAMOU_UTLS_IDENTITY_JSON; "+
				"using built-in firefoxBaselineIdentity (FF135+ baseline) "+
				"with %d ciphers, %d groups",
				profileName,
				len(blob.TLS.CipherSuiteCodes),
				len(blob.TLS.NamedGroupCodes))
		}
	}

	ps.transport = &http.Transport{
		DialTLSContext: func(ctx context.Context, network, addr string) (net.Conn, error) {
			return ps.dialUTLS(network, addr)
		},
		MaxIdleConns:          100,
		IdleConnTimeout:       90 * time.Second,
		TLSHandshakeTimeout:   10 * time.Second,
		ExpectContinueTimeout: 1 * time.Second,
	}

	// Apply HTTP/2 SETTINGS parity to the extent Go's stdlib http2 transport
	// exposes them. Go's net/http does not speak HTTP/2 in a configurable way
	// on its own — http2.ConfigureTransports upgrades the *http.Transport and
	// returns a *http2.Transport for further tuning.
	//
	// Limitations (acknowledged, not silently ignored):
	//   * SETTINGS_HEADER_TABLE_SIZE, SETTINGS_INITIAL_WINDOW_SIZE,
	//     SETTINGS_MAX_FRAME_SIZE, SETTINGS_ENABLE_PUSH, and the connection
	//     WINDOW_UPDATE increment are NOT exposed by the pinned x/net version.
	//     Until we ship a hand-rolled http2.Framer transport, those bits of
	//     the identity blob (EnablePush, InitialWindowSize, MaxFrameSize,
	//     WindowUpdate, HeaderTableSize) silently take Go's defaults. JA4H
	//     and HTTP/2-derived fingerprints WILL diverge from a real Firefox
	//     client.
	//
	// PREVIOUS BUG: this code used to alias IdentityBlob.HTTP2.HeaderTableSize
	// onto h2Transport.MaxHeaderListSize. Those are two semantically
	// different HTTP/2 settings (HPACK dynamic-table size vs. maximum
	// allowed header-list size). Aliasing them clamped the latter to
	// ~65536 instead of Firefox's ~262144 default — actively WORSENING
	// the H2 fingerprint that this proxy is meant to spoof. Removed; we
	// now configure HTTP/2 transport upgrade without misapplying the
	// identity blob.
	if ps.identity != nil {
		if _, err := http2.ConfigureTransports(ps.transport); err != nil {
			log.Printf("[WARN] http2.ConfigureTransports failed: %v", err)
		}
	}

	return ps
}

func (ps *proxyServer) logDebug(format string, args ...interface{}) {
	if ps.debug {
		log.Printf("[DEBUG] "+format, args...)
	}
}

func normalizeHostPort(addr, defaultPort string) (host, hostport string) {
	if h, p, err := net.SplitHostPort(addr); err == nil {
		h = strings.Trim(h, "[]")
		return h, net.JoinHostPort(h, p)
	}
	trimmed := strings.Trim(addr, "[]")
	if ip := net.ParseIP(trimmed); ip != nil {
		return ip.String(), net.JoinHostPort(ip.String(), defaultPort)
	}
	return trimmed, net.JoinHostPort(trimmed, defaultPort)
}

// ── uTLS dialer ─────────────────────────────────────────────────────

func (ps *proxyServer) dialUTLS(network, addr string) (net.Conn, error) {
	hostname, targetAddr := normalizeHostPort(addr, "443")
	rawConn, err := net.DialTimeout(network, targetAddr, 15*time.Second)
	if err != nil {
		return nil, err
	}

	// Bound the TLS handshake. net.DialTimeout only times out the TCP
	// connect; without a per-conn deadline a slow or unresponsive peer
	// can pin a goroutine forever inside utlsConn.Handshake(), leaking
	// goroutines + memory under any concurrent load. 10s mirrors the
	// http.Transport.TLSHandshakeTimeout we already set elsewhere.
	if err := rawConn.SetDeadline(time.Now().Add(10 * time.Second)); err != nil {
		rawConn.Close()
		return nil, fmt.Errorf("set handshake deadline: %w", err)
	}

	utlsConfig := &utls.Config{
		ServerName:         hostname,
		InsecureSkipVerify: false,
		MinVersion:         tls.VersionTLS12,
	}

	ps.mu.RLock()
	spec := ps.customSpec
	fallback := ps.fallbackHello
	ps.mu.RUnlock()

	var utlsConn *utls.UConn
	usedCustom := false
	if spec != nil {
		utlsConn = utls.UClient(rawConn, utlsConfig, utls.HelloCustom)
		if applyErr := utlsConn.ApplyPreset(spec); applyErr != nil {
			// Custom spec rejected by utls (e.g. unsupported KeyShare
			// group like 0x11ec on older utls). Don't fail the whole
			// connection — fall back to the static preset so traffic
			// keeps flowing with a *known* (if slightly mismatched)
			// fingerprint instead of a 502 Bad Gateway for every host.
			ps.logDebug("ApplyPreset failed for host=%s (%v); falling back to %v", hostname, applyErr, fallback)
			utlsConn = utls.UClient(rawConn, utlsConfig, fallback)
		} else {
			usedCustom = true
		}
	} else {
		utlsConn = utls.UClient(rawConn, utlsConfig, fallback)
	}

	if err := utlsConn.Handshake(); err != nil {
		rawConn.Close()
		return nil, fmt.Errorf("uTLS handshake (host=%s): %w", hostname, err)
	}

	// Clear the handshake deadline. From here on, the conn is owned by
	// http.Transport (or the caller's relay loop), and an absolute
	// deadline would prematurely kill long-lived idle keepalives.
	if err := rawConn.SetDeadline(time.Time{}); err != nil {
		// Non-fatal: log and continue; idle close is bounded by
		// http.Server timeouts.
		ps.logDebug("clear handshake deadline failed (host=%s): %v", hostname, err)
	}
	ps.logDebug("uTLS handshake OK (host=%s, version=0x%04x, custom=%t)",
		hostname, utlsConn.ConnectionState().Version, usedCustom)
	return utlsConn, nil
}

// ── CONNECT: transparent (raw relay) ────────────────────────────────

func (ps *proxyServer) handleConnectTransparent(w http.ResponseWriter, r *http.Request) {
	connID := ps.connCount.Add(1)
	_, targetHost := normalizeHostPort(r.Host, "443")
	ps.logDebug("[%d] CONNECT %s (transparent)", connID, targetHost)

	targetConn, err := net.DialTimeout("tcp", targetHost, 15*time.Second)
	if err != nil {
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
		return
	}
	defer targetConn.Close()

	hijacker, ok := w.(http.Hijacker)
	if !ok {
		http.Error(w, "Hijacking not supported", http.StatusInternalServerError)
		return
	}
	clientConn, _, err := hijacker.Hijack()
	if err != nil {
		return
	}
	defer clientConn.Close()

	_, _ = clientConn.Write([]byte("HTTP/1.1 200 Connection Established\r\n\r\n"))
	relay(clientConn, targetConn)
}

// ── CONNECT: MitM (TLS intercept + uTLS re-establishment) ──────────

func (ps *proxyServer) handleConnectMitM(w http.ResponseWriter, r *http.Request) {
	connID := ps.connCount.Add(1)
	hostname, targetHost := normalizeHostPort(r.Host, "443")
	ps.logDebug("[%d] CONNECT %s (mitm)", connID, targetHost)

	// Hijack the client connection
	hijacker, ok := w.(http.Hijacker)
	if !ok {
		http.Error(w, "Hijacking not supported", http.StatusInternalServerError)
		return
	}
	clientConn, _, err := hijacker.Hijack()
	if err != nil {
		return
	}
	defer clientConn.Close()

	// Send 200 so browser starts TLS
	_, _ = clientConn.Write([]byte("HTTP/1.1 200 Connection Established\r\n\r\n"))

	// Generate per-host certificate
	cert, err := ps.ca.certFor(hostname)
	if err != nil {
		ps.logDebug("[%d] cert generation failed for %s: %v", connID, hostname, err)
		return
	}

	// Bound the browser-side TLS handshake. A misbehaving or stalled
	// client could otherwise pin this goroutine indefinitely with no
	// upstream deadline (the underlying clientConn was hijacked from
	// the http server; its read/write timeouts no longer apply).
	if err := clientConn.SetDeadline(time.Now().Add(15 * time.Second)); err != nil {
		ps.logDebug("[%d] set client handshake deadline failed: %v", connID, err)
		return
	}

	// Terminate browser's TLS (browser connects to us with standard TLS)
	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{*cert},
		NextProtos:   []string{"h2", "http/1.1"},
	}
	browserTLS := tls.Server(clientConn, tlsConfig)
	if err := browserTLS.Handshake(); err != nil {
		ps.logDebug("[%d] browser TLS handshake failed: %v", connID, err)
		return
	}
	defer browserTLS.Close()

	// Clear the deadline so the relay below isn't artificially capped.
	if err := clientConn.SetDeadline(time.Time{}); err != nil {
		ps.logDebug("[%d] clear client deadline failed: %v", connID, err)
	}

	// Connect to target with uTLS (spoofed Client Hello)
	targetConn, err := ps.dialUTLS("tcp", targetHost)
	if err != nil {
		ps.logDebug("[%d] target uTLS dial failed: %v", connID, err)
		return
	}
	defer targetConn.Close()

	// Relay decrypted traffic
	relay(browserTLS, targetConn)
	ps.logDebug("[%d] MitM tunnel closed", connID)
}

// ── HTTP forward (non-CONNECT, with uTLS + HTTP/2 SETTINGS) ────────

func (ps *proxyServer) handleHTTP(w http.ResponseWriter, r *http.Request) {
	connID := ps.connCount.Add(1)
	ps.logDebug("[%d] HTTP %s %s", connID, r.Method, r.URL.String())

	outReq := r.Clone(r.Context())
	outReq.RequestURI = ""
	if outReq.URL.Scheme == "" {
		outReq.URL.Scheme = "http"
	}
	if outReq.URL.Host == "" {
		outReq.URL.Host = r.Host
	}
	removeHopByHopHeaders(outReq.Header)

	resp, err := ps.transport.RoundTrip(outReq)
	if err != nil {
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	for key, values := range resp.Header {
		for _, v := range values {
			w.Header().Add(key, v)
		}
	}
	w.WriteHeader(resp.StatusCode)
	_, _ = io.Copy(w, resp.Body)
}

// ── Relay helper ────────────────────────────────────────────────────

func removeHopByHopHeaders(header http.Header) {
	for _, key := range []string{
		"Connection",
		"Proxy-Connection",
		"Keep-Alive",
		"Proxy-Authenticate",
		"Proxy-Authorization",
		"Te",
		"Trailer",
		"Transfer-Encoding",
		"Upgrade",
	} {
		header.Del(key)
	}
}

func relay(a, b net.Conn) {
	var wg sync.WaitGroup
	// halfClose shuts down the write half of a connection when possible
	// (plain TCP). For *tls.Conn (which has no CloseWrite) it instead
	// sets a short read deadline on the *other* side so the blocked
	// io.Copy returns promptly instead of hanging forever.
	halfClose := func(writer, reader net.Conn) {
		if cw, ok := writer.(interface{ CloseWrite() error }); ok {
			_ = cw.CloseWrite()
		} else {
			// Force the peer's io.Copy to unblock by tightening
			// the deadline on the connection it is reading from.
			reader.SetReadDeadline(time.Now().Add(5 * time.Second))
		}
	}
	wg.Add(2)
	go func() {
		defer wg.Done()
		_, _ = io.Copy(b, a)
		halfClose(b, a)
	}()
	go func() {
		defer wg.Done()
		_, _ = io.Copy(a, b)
		halfClose(a, b)
	}()
	wg.Wait()
}

// ── Control API ─────────────────────────────────────────────────────

func (ps *proxyServer) handleControl(w http.ResponseWriter, r *http.Request) {
	switch r.URL.Path {
	case "/healthz":
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, `{"ok":true,"profile":"%s","mode":"%s","connections":%d,"custom_spec":%t}`,
			ps.profileName, modeStr(ps.mitmMode), ps.connCount.Load(), ps.customSpec != nil)
	case "/ca.pem":
		if ps.ca != nil {
			w.Header().Set("Content-Type", "application/x-pem-file")
			w.Write(ps.ca.certPEM)
		} else {
			http.Error(w, "No CA available", http.StatusNotFound)
		}
	default:
		http.NotFound(w, r)
	}
}

func modeStr(mitm bool) string {
	if mitm {
		return "mitm"
	}
	return "transparent"
}

// ── Main Handler ────────────────────────────────────────────────────

func (ps *proxyServer) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.URL.Host == "" && (r.URL.Path == "/healthz" || r.URL.Path == "/ca.pem") {
		ps.handleControl(w, r)
		return
	}
	if r.Method == http.MethodConnect {
		if ps.mitmMode && ps.ca != nil {
			ps.handleConnectMitM(w, r)
		} else {
			ps.handleConnectTransparent(w, r)
		}
		return
	}
	ps.handleHTTP(w, r)
}

// ── Entry Point ─────────────────────────────────────────────────────

func main() {
	profileName := os.Getenv("CAMOU_UTLS_PROFILE")
	if profileName == "" {
		profileName = "firefox150"
	}
	listenAddr := os.Getenv("CAMOU_UTLS_LISTEN")
	if listenAddr == "" {
		listenAddr = "127.0.0.1:8080"
	}
	debug := os.Getenv("CAMOU_UTLS_DEBUG") == "1"
	mitmMode := os.Getenv("CAMOU_UTLS_MODE") == "mitm"

	var ca *mitmCA
	if mitmMode {
		var err error
		ca, err = newMitmCA(
			os.Getenv("CAMOU_UTLS_CA_CERT"),
			os.Getenv("CAMOU_UTLS_CA_KEY"),
		)
		if err != nil {
			log.Fatalf("[FATAL] Failed to initialize MitM CA: %v", err)
		}
	}

	ps := newProxyServer(profileName, debug, mitmMode, ca)

	log.Printf("[INFO] Camoufox uTLS Proxy starting")
	log.Printf("[INFO]   Listen:     %s", listenAddr)
	log.Printf("[INFO]   Profile:    %s", profileName)
	log.Printf("[INFO]   Mode:       %s", modeStr(mitmMode))
	log.Printf("[INFO]   CustomSpec: %t", ps.customSpec != nil)
	log.Printf("[INFO]   Debug:      %v", debug)

	server := &http.Server{
		Addr:         listenAddr,
		Handler:      ps,
		ReadTimeout:  30 * time.Second,
		WriteTimeout: 60 * time.Second,
		IdleTimeout:  120 * time.Second,
	}
	if err := server.ListenAndServe(); err != nil {
		log.Fatalf("[FATAL] Server failed: %v", err)
	}
}
