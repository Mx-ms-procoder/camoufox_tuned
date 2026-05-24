from camoufox.tls_profiles import get_tls_env_vars, get_tls_profile


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
