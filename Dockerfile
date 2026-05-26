# Pinned to a specific Ubuntu LTS so build behavior is reproducible across
# rebuilds. `ubuntu:latest` previously caused silent drift when Canonical
# republished the tag. Bump intentionally rather than chasing `latest`.
# See AUDIT_2026-05-15.md priority fix #5.
FROM ubuntu:24.04

WORKDIR /app

# Copy the current directory into the container at /app
COPY . /app

# Install necessary packages.
#
# Note: the apt-installed `rustc` is intentionally NOT included. The
# Rust toolchain is managed below via the pinned rustup-init flow so
# that one source-of-truth governs MSRV. Mixing apt-rustc with rustup
# previously caused MSRV disagreements on Ubuntu 24.04 (apt ships an
# older rustc than the Firefox 150 baseline requires).
RUN apt-get update && apt-get install -y \
    # Mach build tools
    build-essential make msitools wget zip unzip nasm yasm nodejs pkg-config \
    patch clang-18 lld-18 llvm-18 libclang-18-dev cbindgen \
    # Python
    python3 python3-dev python3-pip \
    # Camoufox build system tools
    git p7zip-full golang-go aria2 curl rsync \
    # Platform-specific libraries for Linux builds
    libdbus-glib-1-dev libgtk-3-dev libpulse-dev libsqlite3-dev libx11-xcb-dev libxt-dev \
    # CA certificates
    ca-certificates \
    && update-ca-certificates

RUN update-alternatives --install /usr/bin/clang clang /usr/bin/clang-18 100 && \
    update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-18 100 && \
    update-alternatives --install /usr/bin/lld lld /usr/bin/lld-18 100 && \
    update-alternatives --install /usr/bin/llvm-ar llvm-ar /usr/bin/llvm-ar-18 100 && \
    update-alternatives --install /usr/bin/llvm-nm llvm-nm /usr/bin/llvm-nm-18 100 && \
    update-alternatives --install /usr/bin/llvm-objcopy llvm-objcopy /usr/bin/llvm-objcopy-18 100 && \
    update-alternatives --install /usr/bin/llvm-objdump llvm-objdump /usr/bin/llvm-objdump-18 100 && \
    update-alternatives --install /usr/bin/llvm-readelf llvm-readelf /usr/bin/llvm-readelf-18 100

# K-17 (AUDIT_2026-05-18.md): replace pipe-to-shell Rust install with a
# pinned, checksum-verified rustup-init download. The previous form
#   `curl https://sh.rustup.rs -sSf | bash -s -- -y`
# is the classic supply-chain anti-pattern — the build trusts whatever
# bytes the CDN happens to serve at build time, with no version pinning
# and no integrity check. We now:
#   1) pin the rustup-init version and pull it from the canonical
#      static.rust-lang.org/rustup/archive path (not the rolling
#      sh.rustup.rs redirector),
#   2) fetch the matching upstream .sha256 file from the same release
#      directory and verify the binary against it,
#   3) optionally cross-verify against RUSTUP_INIT_SHA256 if the
#      operator has pre-pinned a known-good value via --build-arg
#      (recommended for hardened builds — set it once, fail fast if
#      upstream changes it),
#   4) install a pinned toolchain matching the Firefox 150 baseline
#      kept in .github/workflows/build.yml.
# Bump RUSTUP_INIT_VERSION + RUST_TOOLCHAIN together when the Firefox
# baseline moves.
ARG RUSTUP_INIT_VERSION=1.27.1
ARG RUSTUP_INIT_SHA256=
ARG RUST_TOOLCHAIN=1.94.0
RUN set -eux; \
    arch="$(dpkg --print-architecture)"; \
    case "$arch" in \
      amd64)  rust_arch=x86_64-unknown-linux-gnu ;; \
      arm64)  rust_arch=aarch64-unknown-linux-gnu ;; \
      *) echo "Unsupported arch: $arch"; exit 1 ;; \
    esac; \
    base="https://static.rust-lang.org/rustup/archive/${RUSTUP_INIT_VERSION}/${rust_arch}"; \
    curl --proto '=https' --tlsv1.2 -fsSL -o /tmp/rustup-init       "${base}/rustup-init"; \
    curl --proto '=https' --tlsv1.2 -fsSL -o /tmp/rustup-init.sha256 "${base}/rustup-init.sha256"; \
    upstream_sha="$(awk '{print $1}' /tmp/rustup-init.sha256)"; \
    actual_sha="$(sha256sum /tmp/rustup-init | awk '{print $1}')"; \
    if [ "${upstream_sha}" != "${actual_sha}" ]; then \
        echo "rustup-init SHA mismatch vs upstream .sha256 (${actual_sha} != ${upstream_sha})"; exit 1; \
    fi; \
    if [ -n "${RUSTUP_INIT_SHA256}" ] && [ "${RUSTUP_INIT_SHA256}" != "${actual_sha}" ]; then \
        echo "rustup-init SHA mismatch vs pinned --build-arg (${actual_sha} != ${RUSTUP_INIT_SHA256})"; exit 1; \
    fi; \
    chmod +x /tmp/rustup-init; \
    /tmp/rustup-init -y --no-modify-path --profile minimal \
        --default-toolchain "${RUST_TOOLCHAIN}"; \
    rm -f /tmp/rustup-init /tmp/rustup-init.sha256
ENV PATH="/root/.cargo/bin:${PATH}"

# Fetch Firefox & apply initial patches
RUN make setup-minimal && \
    mkdir -p /app/dist

# Mount .mozbuild directory and dist folder
VOLUME /root/.mozbuild
VOLUME /app/dist

ENTRYPOINT ["python3", "./multibuild.py"]
