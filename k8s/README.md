# Camoufox Kubernetes manifests — EXPERIMENTAL

> [!WARNING]
> **This deployment is experimental and not production-ready.**
> The session broker is a working metadata service, but the warm-pool
> Deployment in `camoufox-pool.yaml` does **not** yet run distinct
> browser workers — it runs the same `camoufox-slim` image as the broker
> with the same default command. Until separate worker images and a
> broker→worker dispatch protocol land, treat these manifests as a
> reference architecture and a starting point, not a turnkey platform.
> See [`AUDIT_2026-05-18.md`](../AUDIT_2026-05-18.md) for the full
> caveat list.

## What's in here

| File | Role | Status |
|---|---|---|
| [`session-broker.yaml`](session-broker.yaml) | Deployment + Service for the HTTP session broker (`camoufox cloud-broker`). Exposes session leases and snapshot storage over HTTP. | Working metadata service. Lease state is in-process — see [§Limits](#limits). |
| [`camoufox-pool.yaml`](camoufox-pool.yaml) | Deployment for a "warm pool" of browser workers with anti-affinity spread across nodes. | **Stub.** The pods run the broker image, not a distinct worker. No browser is launched by `SessionBroker.create_session`. |
| [`redis-state.yaml`](redis-state.yaml) | StatefulSet + Service + Secret for Redis. Optional backing store for snapshots and (eventually) lease state. | Working. Password-auth + AOF persistence enabled by default. |

## Limits you need to know about

1. **Single-replica broker.** `SessionBroker._leases` lives in process memory
   (`pythonlib/camoufox/cloud_native.py`). The Deployment is pinned to
   `replicas: 1` because two brokers without sticky sessions would each
   return 404 for sessions created on the sibling. The HPA block in the
   manifest is **commented-out / aspirational** — only enable it after
   externalising the lease table to Redis and adding ingress-layer
   sticky-session affinity.

2. **No real worker dispatch.** `camoufox-pool.yaml` deploys 5 replicas
   that share the broker's command. `create_session` does **not** call
   into them, does not proxy browser traffic, and does not pin a session
   to a specific worker pod. Treat the pool count as a placeholder for
   future capacity, not as actual concurrent browsers.

3. **Bearer-token enforcement.** `serve_broker()` aborts at startup if it
   binds to a non-loopback host without `CAMOUFOX_BROKER_TOKEN`. There
   is no escape hatch — the previously available
   `CAMOUFOX_BROKER_ALLOW_UNAUTHENTICATED=1` was removed in K-5 of the
   2026-05-18 audit. Provision the token via a Kubernetes Secret before
   applying `session-broker.yaml`.

4. **Snapshot storage.** The broker accepts a `--snapshot-dir` flag and
   can also be pointed at S3 via env vars (`CAMOUFOX_S3_BUCKET`, etc.) —
   see the `SnapshotStore` Protocol in `cloud_native.py`. The default
   manifest uses an `emptyDir` mount; switch to a `PersistentVolumeClaim`
   or S3 for any data you care about across pod restarts.

## When NOT to use these manifests

- You want a **drop-in browser farm**. These don't give you one. Use
  Playwright-on-Kubernetes recipes from upstream Playwright instead, or
  wait for the worker dispatch path to land.
- You need **horizontal scaling of the broker**. Not supported without
  the Redis-backed lease work.
- You're **exposing this to the internet without an authenticating
  proxy/ingress in front of it**. The bearer token is necessary but not
  sufficient; rate-limiting and TLS termination belong at the ingress.

## Roadmap

- [ ] Externalise `SessionBroker._leases` to Redis (already wired for
  snapshots; lease store needs the same `RedisLeaseStore` Protocol).
- [ ] Build a distinct `camoufox-worker` image and a broker→worker RPC
  (likely gRPC + CDP forwarding) so `create_session` actually launches.
- [ ] Replace the placeholder warm-pool replica count with a real HPA
  based on broker-reported queue depth.
- [ ] Document an end-to-end test-cluster recipe (kind/minikube) once
  the worker path works.

Until those items land, this directory is a reference architecture, not
a recommended production deployment.
