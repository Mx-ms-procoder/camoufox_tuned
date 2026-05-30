from camoufox.tls_profiles import get_http2_config, get_tls_env_vars, get_tls_profile


def test_firefox_network_profile_exports_metadata():
    profile = get_tls_profile("firefox", 135)

    assert profile is not None
    assert profile.validate_browser_family("firefox")
    assert profile.validate_browser_major(135)
    assert profile.is_nss_native()

    env_vars = get_tls_env_vars(profile)
    assert "CAMOU_NET_PROFILE" in env_vars
    assert "firefox135" in env_vars["CAMOU_NET_PROFILE"]
    # Firefox profiles are nss-native and currently advertise
    # supports_nss_env_overrides=True, so the NSS-side CAMOU_TLS_* knobs
    # are present. If a profile drops env-override support that should be
    # asserted by a dedicated negative test on that specific profile.
    assert "CAMOU_TLS_CIPHERS" in env_vars
    assert env_vars["CAMOU_TLS_CIPHERS"].startswith("0x")
    assert "CAMOU_TLS_ALPN" not in env_vars


def test_newer_firefox_profile_uses_native_runtime_fingerprint():
    profile = get_tls_profile("firefox", 150)

    assert profile is not None
    assert profile.fingerprint_source == "native-nss-runtime"
    assert profile.supports_nss_env_overrides is False
    assert profile.client_hello_template == {}
    assert profile.http2_template == {}

    env_vars = get_tls_env_vars(profile)
    assert "CAMOU_NET_PROFILE" in env_vars
    assert "CAMOU_TLS_CIPHERS" not in env_vars
    assert "CAMOU_TLS_GROUPS" not in env_vars
    assert "CAMOU_TLS_SIGALGS" not in env_vars
    assert "CAMOU_TLS_ALPN" not in env_vars
    assert get_http2_config(profile) == {}
