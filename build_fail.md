build (windows, x86_64, ubuntu-24.04)

build

Run python3 ./multibuild.py --target windows --arch x86_64
python3 scripts/patch.py 135.0.1 beta.24 --mozconfig-only
~/.cargo/bin/rustup target add "x86_64-pc-windows-gnu"
info: downloading component rust-std
~/.cargo/bin/rustup target add "i686-pc-windows-gnu"
info: downloading component rust-std
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: x86_64-pc-mingw32
-> Updating mozconfig, target is x86_64-pc-mingw32
Complete!
rm -rf camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox-bin \
	camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox
make[1]: Entering directory '/home/runner/work/firefox/firefox'
python3 scripts/patch.py 135.0.1 beta.24
~/.cargo/bin/rustup target add "x86_64-pc-windows-gnu"
info: component rust-std for target x86_64-pc-windows-gnu is up to date
~/.cargo/bin/rustup target add "i686-pc-windows-gnu"
info: component rust-std for target i686-pc-windows-gnu is up to date
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: x86_64-pc-mingw32
-> Updating mozconfig, target is x86_64-pc-mingw32

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/ghostery/Disable-Onboarding-Messages.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/ghostery/Disable-Onboarding-Messages.patch
patching file browser/components/asrouter/modules/OnboardingMessageProvider.sys.mjs
Hunk #1 succeeded at 1370 (offset 155 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/all-addons-private-mode.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/all-addons-private-mode.patch
patching file toolkit/components/extensions/Extension.sys.mjs
Hunk #1 succeeded at 3892 (offset 606 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/allow-searchengines-non-esr.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/allow-searchengines-non-esr.patch
patching file browser/components/enterprisepolicies/schemas/policies-schema.json
Hunk #1 succeeded at 1385 (offset 311 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/anti-font-fingerprinting.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/anti-font-fingerprinting.patch
patching file gfx/thebes/gfxHarfBuzzShaper.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/audio-context-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/audio-context-spoofing.patch
patching file dom/media/CubebUtils.cpp
Hunk #1 succeeded at 43 (offset 3 lines).
Hunk #2 succeeded at 411 (offset 11 lines).
patching file dom/media/moz.build
patching file dom/media/webaudio/AudioContext.cpp
Hunk #2 succeeded at 556 (offset -6 lines).
Hunk #3 succeeded at 712 (offset -6 lines).
patching file dom/media/webaudio/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/bootstrap.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/bootstrap.patch
patching file python/mozversioncontrol/mozversioncontrol/repo/source.py

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/browser-init.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/browser-init.patch
patching file browser/base/content/browser-init.js
Hunk #3 succeeded at 120 with fuzz 2 (offset 1 line).
Hunk #4 succeeded at 320 (offset -16 lines).
Hunk #5 succeeded at 371 (offset -16 lines).
Hunk #6 succeeded at 417 (offset -16 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/chromeutil.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/chromeutil.patch
patching file dom/base/ChromeUtils.cpp
Hunk #2 succeeded at 2416 (offset 299 lines).
Hunk #3 succeeded at 2460 (offset 299 lines).
patching file dom/base/ChromeUtils.h
Hunk #1 succeeded at 315 (offset 10 lines).
Hunk #2 succeeded at 328 (offset 10 lines).
patching file dom/chrome-webidl/ChromeUtils.webidl
Hunk #1 succeeded at 769 (offset 19 lines).
Hunk #2 succeeded at 787 (offset 19 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/config.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/config.patch
patching file browser/installer/package-manifest.in
Hunk #1 succeeded at 256 (offset 12 lines).
patching file lw/moz.build
patching file moz.build
Hunk #1 succeeded at 226 with fuzz 1 (offset 6 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/context-menu.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/context-menu.patch
patching file browser/base/content/browser-context.inc
Hunk #1 succeeded at 106 (offset -1 lines).
Hunk #2 succeeded at 259 (offset -2 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/custom-ubo-assets-bootstrap-location.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/custom-ubo-assets-bootstrap-location.patch
patching file toolkit/components/extensions/parent/ext-storage.js
Hunk #1 succeeded at 403 (offset 226 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/dbus_name.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/dbus_name.patch
patching file toolkit/components/remote/nsDBusRemoteClient.cpp
Hunk #3 succeeded at 121 (offset 4 lines).
Hunk #4 succeeded at 132 (offset 4 lines).
patching file toolkit/components/remote/nsDBusRemoteServer.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/devtools-bypass.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/devtools-bypass.patch
patching file devtools/server/actors/thread.js
patching file devtools/server/actors/webconsole/listeners/console-api.js
Hunk #1 succeeded at 97 with fuzz 1.

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/disable-data-reporting-at-compile-time.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/disable-data-reporting-at-compile-time.patch
patching file browser/moz.configure
patching file python/mach/mach/telemetry.py
Hunk #1 succeeded at 95 (offset -3 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/disable-extension-newtab.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/disable-extension-newtab.patch
patching file browser/components/extensions/parent/ext-browser.js
patching file browser/components/extensions/parent/ext-tabs.js

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/disable-pocket.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/disable-pocket.patch
patching file browser/base/content/browser.js
Hunk #1 succeeded at 3399 with fuzz 2 (offset -2079 lines).
patching file browser/components/BrowserGlue.sys.mjs
Hunk #1 succeeded at 1585 with fuzz 2 (offset 311 lines).
patching file browser/components/moz.build
Hunk #1 succeeded at 48 (offset 4 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/disable-remote-subframes.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/disable-remote-subframes.patch
patching file docshell/base/BrowsingContext.cpp
Hunk #2 succeeded at 1770 (offset -3 lines).
patching file docshell/base/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/fingerprint-injection.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/fingerprint-injection.patch
patching file browser/app/moz.build
patching file dom/base/Element.cpp
Hunk #1 succeeded at 12 with fuzz 2.
Hunk #2 succeeded at 1012 (offset 27 lines).
patching file dom/base/Navigator.cpp
Hunk #6 succeeded at 374 with fuzz 1 (offset -1 lines).
Hunk #7 succeeded at 429 (offset -4 lines).
Hunk #8 succeeded at 452 (offset -10 lines).
Hunk #9 succeeded at 484 (offset -10 lines).
Hunk #10 succeeded at 529 (offset -10 lines).
Hunk #11 succeeded at 570 (offset -10 lines).
Hunk #12 succeeded at 600 (offset -10 lines).
Hunk #13 succeeded at 649 (offset -10 lines).
Hunk #14 succeeded at 665 (offset -10 lines).
Hunk #15 succeeded at 727 (offset -10 lines).
Hunk #16 succeeded at 747 (offset -10 lines).
Hunk #17 succeeded at 762 (offset -10 lines).
Hunk #18 succeeded at 964 (offset -10 lines).
patching file dom/base/moz.build
Hunk #1 succeeded at 659 (offset 18 lines).
patching file dom/base/nsGlobalWindowInner.cpp
Hunk #2 succeeded at 3425 (offset 14 lines).
Hunk #3 succeeded at 3439 (offset 14 lines).
Hunk #4 succeeded at 3458 (offset 14 lines).
Hunk #5 succeeded at 3486 (offset 14 lines).
Hunk #6 succeeded at 3530 (offset 14 lines).
Hunk #7 succeeded at 3604 (offset 14 lines).
patching file dom/base/nsHistory.cpp
patching file dom/base/nsScreen.cpp
Hunk #3 succeeded at 91 with fuzz 1 (offset -3 lines).
patching file dom/battery/BatteryManager.cpp
patching file dom/battery/moz.build
patching file dom/workers/WorkerNavigator.cpp
Hunk #2 succeeded at 104 (offset 11 lines).
Hunk #3 succeeded at 130 (offset 11 lines).
Hunk #4 succeeded at 158 (offset 11 lines).
Hunk #5 succeeded at 224 (offset 7 lines).
Hunk #6 succeeded at 241 (offset 7 lines).
patching file dom/workers/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/firefox-view.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/firefox-view.patch
patching file browser/base/content/navigator-toolbox.inc.xhtml
Hunk #2 succeeded at 663 (offset 4 lines).
patching file browser/components/customizableui/CustomizableUI.sys.mjs
Hunk #1 succeeded at 356 (offset 9 lines).
Hunk #2 succeeded at 715 (offset 9 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/font-hijacker.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/font-hijacker.patch
patching file gfx/thebes/gfxPlatformFontList.cpp
patching file gfx/thebes/moz.build
Hunk #1 succeeded at 303 (offset -2 lines).
patching file layout/style/FontFace.cpp
Hunk #1 succeeded at 243 (offset 6 lines).
Hunk #2 succeeded at 262 (offset 6 lines).
patching file layout/style/FontFaceImpl.cpp
Hunk #1 succeeded at 358 (offset 1 line).
patching file layout/style/FontFaceImpl.h
Hunk #1 succeeded at 8 with fuzz 2.
Hunk #2 succeeded at 33 (offset -3 lines).
patching file layout/style/moz.build
Hunk #1 succeeded at 366 (offset 15 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/force-default-pointer.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/force-default-pointer.patch
patching file layout/style/nsMediaFeatures.cpp
Hunk #1 succeeded at 376 (offset 4 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/geolocation-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/geolocation-spoofing.patch
patching file dom/geolocation/Geolocation.cpp
Hunk #1 succeeded at 39 (offset 5 lines).
Hunk #2 succeeded at 1427 with fuzz 2 (offset 159 lines).
patching file dom/geolocation/GeolocationPosition.cpp
patching file dom/geolocation/moz.build
Hunk #1 succeeded at 81 (offset 23 lines).
patching file dom/system/NetworkGeolocationProvider.sys.mjs

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/global-style-sheets.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/global-style-sheets.patch
patching file layout/style/GlobalStyleSheetCache.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/handlers.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/handlers.patch
patching file uriloader/exthandler/HandlerList.sys.mjs

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/hide-default-browser.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/hide-default-browser.patch
patching file browser/components/preferences/main.inc.xhtml
Hunk #2 succeeded at 54 (offset 6 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/locale-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/locale-spoofing.patch
patching file intl/components/src/Locale.cpp
patching file intl/components/src/Locale.h
patching file intl/locale/OSPreferences.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/macos-backgroundtasks-disabled.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/macos-backgroundtasks-disabled.patch
patching file toolkit/xre/nsAppRunner.cpp
Hunk #1 succeeded at 5669 (offset 36 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/media-device-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/media-device-spoofing.patch
patching file dom/media/MediaDevices.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/mozilla_dirs.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/mozilla_dirs.patch
patching file toolkit/xre/nsXREDirProvider.cpp
Hunk #1 succeeded at 285 with fuzz 1 (offset -15 lines).
Hunk #2 succeeded at 366 (offset -5 lines).
Hunk #3 succeeded at 398 with fuzz 2 (offset -13 lines).
Hunk #4 succeeded at 932 (offset -182 lines).
Hunk #5 succeeded at 1192 (offset -171 lines).
Hunk #6 succeeded at 1202 (offset -171 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/network-patches.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/network-patches.patch
patching file netwerk/protocol/http/moz.build
Hunk #1 succeeded at 234 (offset 16 lines).
patching file netwerk/protocol/http/nsHttpHandler.cpp
Hunk #2 succeeded at 885 (offset 137 lines).
Hunk #3 succeeded at 1997 (offset 149 lines).
Hunk #4 succeeded at 2019 (offset 149 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-css-animations.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-css-animations.patch
patching file dom/animation/AnimationEffect.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-search-engines.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-search-engines.patch
patching file toolkit/components/search/SearchEngineSelector.sys.mjs
Hunk #1 succeeded at 181 (offset 23 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/nss-tls-override.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/nss-tls-override.patch
patching file security/manager/ssl/nsNSSComponent.cpp
Hunk #2 succeeded at 1617 with fuzz 1.
patching file security/manager/ssl/moz.build
Hunk #1 succeeded at 199 with fuzz 1.

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/pin-addons.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/pin-addons.patch
patching file browser/base/content/browser-addons.js
Hunk #1 succeeded at 2393 (offset 469 lines).
patching file browser/base/content/main-popupset.inc.xhtml
Hunk #1 succeeded at 365 (offset 79 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-branding-urlbar.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-branding-urlbar.patch
patching file browser/locales/en-US/browser/browser.ftl
Hunk #1 succeeded at 715 (offset 172 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-cfrprefs.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-cfrprefs.patch
patching file browser/components/preferences/main.inc.xhtml
Hunk #1 succeeded at 775 (offset 33 lines).
Hunk #2 succeeded at 785 (offset 33 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-organization-policy-banner.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-organization-policy-banner.patch
patching file browser/components/preferences/preferences.js
Hunk #1 succeeded at 241 (offset 7 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/remove_addons.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/remove_addons.patch
patching file browser/extensions/moz.build
patching file browser/locales/Makefile.in
Hunk #1 succeeded at 55 (offset -1 lines).
Hunk #2 succeeded at 75 (offset -2 lines).
patching file browser/locales/filter.py
Hunk #1 succeeded at 15 (offset -2 lines).
patching file browser/locales/l10n.ini
patching file browser/locales/l10n.toml
Hunk #1 succeeded at 135 (offset 2 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/rust-gentoo-musl.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/rust-gentoo-musl.patch
patching file build/moz.configure/rust.configure

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/screen-hijacker.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/screen-hijacker.patch
patching file dom/base/nsScreen.cpp
patching file gfx/src/moz.build
patching file gfx/src/nsDeviceContext.cpp
patching file layout/style/nsMediaFeatures.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/shadow-root-bypass.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/shadow-root-bypass.patch
patching file dom/webidl/Element.webidl

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch
patching file browser/components/asrouter/content/asrouter-admin.bundle.js
Hunk #1 succeeded at 1144 with fuzz 1.
patching file services/settings/Utils.sys.mjs
Hunk #1 succeeded at 51 (offset -3 lines).
patching file toolkit/components/search/SearchUtils.sys.mjs
Hunk #1 succeeded at 169 (offset -3 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/timezone-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/timezone-spoofing.patch
patching file intl/components/moz.build
patching file intl/components/src/TimeZone.cpp
Hunk #2 succeeded at 22 (offset -1 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/urlbarprovider-interventions.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/urlbarprovider-interventions.patch
patching file browser/components/urlbar/UrlbarProviderInterventions.sys.mjs
Hunk #1 succeeded at 453 (offset -1 lines).
Hunk #2 succeeded at 495 (offset 1 line).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/voice-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/voice-spoofing.patch
patching file dom/media/webspeech/synth/moz.build
patching file dom/media/webspeech/synth/nsSynthVoiceRegistry.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/webgl-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/webgl-spoofing.patch
patching file dom/canvas/ClientWebGLContext.cpp
Hunk #2 succeeded at 754 (offset 1 line).
Hunk #3 succeeded at 771 (offset 1 line).
Hunk #4 succeeded at 1022 (offset 1 line).
Hunk #5 succeeded at 2112 (offset 1 line).
Hunk #6 succeeded at 2268 (offset 1 line).
Hunk #7 succeeded at 2525 (offset 1 line).
Hunk #8 succeeded at 2538 (offset 1 line).
Hunk #9 succeeded at 2635 (offset 2 lines).
Hunk #10 succeeded at 3020 (offset 2 lines).
Hunk #11 succeeded at 6018 (offset 2 lines).
Hunk #12 succeeded at 6040 (offset 2 lines).
patching file dom/canvas/ClientWebGLContext.h
Hunk #1 succeeded at 1073 (offset -1 lines).
patching file dom/canvas/moz.build
Hunk #1 succeeded at 228 (offset 7 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/webrtc-ip-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/webrtc-ip-spoofing.patch
patching file dom/media/webrtc/jsapi/PeerConnectionImpl.cpp
patching file dom/media/webrtc/jsapi/PeerConnectionImpl.h
patching file dom/media/webrtc/jsapi/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/windows-theming-bug-modified.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/windows-theming-bug-modified.patch
patching file browser/app/Makefile.in
patching file browser/app/camoufox.exe.manifest (renamed from browser/app/firefox.exe.manifest)

--- Applied 48 patch(es) successfully ---
Complete!
touch camoufox-135.0.1-beta.24/_READY
make[1]: Leaving directory '/home/runner/work/firefox/firefox'
cd camoufox-135.0.1-beta.24 && ./mach build 
Collecting glean-sdk==63.0.0
  Downloading glean_sdk-63.0.0-py3-none-manylinux_2_34_x86_64.whl.metadata (4.8 kB)
Collecting semver>=2.13.0 (from glean-sdk==63.0.0)
  Downloading semver-3.0.4-py3-none-any.whl.metadata (6.8 kB)
Requirement already satisfied: glean-parser~=16.1 in ./third_party/python/glean_parser (from glean-sdk==63.0.0) (16.1.0)
Requirement already satisfied: Click>=7 in ./third_party/python/click (from glean-parser~=16.1->glean-sdk==63.0.0) (8.1.6)
Requirement already satisfied: diskcache>=4 in ./third_party/python/diskcache (from glean-parser~=16.1->glean-sdk==63.0.0) (5.6.3)
Requirement already satisfied: Jinja2>=2.10.1 in ./third_party/python/Jinja2 (from glean-parser~=16.1->glean-sdk==63.0.0) (3.1.2)
Requirement already satisfied: jsonschema>=3.0.2 in ./third_party/python/jsonschema (from glean-parser~=16.1->glean-sdk==63.0.0) (4.17.3)
Requirement already satisfied: platformdirs>=2.4.0 in ./third_party/python/platformdirs (from glean-parser~=16.1->glean-sdk==63.0.0) (4.3.6)
Requirement already satisfied: PyYAML>=5.3.1 in ./third_party/python/PyYAML/lib (from glean-parser~=16.1->glean-sdk==63.0.0) (6.0.1)
Requirement already satisfied: MarkupSafe>=2.0 in ./third_party/python/MarkupSafe/src (from Jinja2>=2.10.1->glean-parser~=16.1->glean-sdk==63.0.0) (2.0.1)
Requirement already satisfied: attrs>=17.4.0 in ./third_party/python/attrs (from jsonschema>=3.0.2->glean-parser~=16.1->glean-sdk==63.0.0) (23.1.0)
Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in ./third_party/python/pyrsistent (from jsonschema>=3.0.2->glean-parser~=16.1->glean-sdk==63.0.0) (0.20.0)
Downloading glean_sdk-63.0.0-py3-none-manylinux_2_34_x86_64.whl (861 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 861.6/861.6 kB 30.8 MB/s eta 0:00:00
Downloading semver-3.0.4-py3-none-any.whl (17 kB)
Installing collected packages: semver, glean-sdk
Successfully installed glean-sdk-63.0.0 semver-3.0.4
Collecting psutil<=5.9.4,>=5.4.2
  Downloading psutil-5.9.4-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (21 kB)
Downloading psutil-5.9.4-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (280 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 280.2/280.2 kB 21.9 MB/s eta 0:00:00
Installing collected packages: psutil
Successfully installed psutil-5.9.4
Collecting zstandard<=0.23.0,>=0.11.1
  Downloading zstandard-0.23.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (3.0 kB)
Downloading zstandard-0.23.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (5.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 71.8 MB/s eta 0:00:00
Installing collected packages: zstandard
Successfully installed zstandard-0.23.0
Mach and the build system store shared state in a common directory
on the filesystem. The following directory will be created:

  /home/runner/.mozbuild

If you would like to use a different directory, rename or move it to your
desired location, and set the MOZBUILD_STATE_PATH environment variable
accordingly.
Creating default state directory: /home/runner/.mozbuild
Creating local state directory: /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7
 0:00.78 W Clobber not needed.
 0:00.97 Using Python 3.11.15 from /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7/_virtualenvs/build/bin/python
 0:00.97 Adding configure options from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/mozconfig
 0:00.97   --enable-application=browser
 0:00.97   --allow-addon-sideload
 0:00.97   --disable-crashreporter
 0:00.97   --disable-backgroundtasks
 0:00.97   --disable-debug
 0:00.97   --disable-default-browser-agent
 0:00.97   --disable-tests
 0:00.97   --disable-updater
 0:00.97   --enable-release
 0:00.97   --disable-system-policies
 0:00.97   --without-wasm-sandboxed-libraries
 0:00.97   --with-app-name=camoufox
 0:00.97   --with-branding=browser/branding/camoufox
 0:00.97   --with-unsigned-addon-scopes=app,system
 0:00.97   --disable-bootstrap
 0:00.97   --with-libclang-path=/usr/lib/llvm-18/lib
 0:00.97   --target=x86_64-pc-mingw32
 0:00.97   --disable-maintenance-service
 0:00.97   --disable-update-agent
 0:00.97   --disable-accessibility
 0:00.97   RANLIB=x86_64-w64-mingw32-ranlib
 0:00.97   CC=clang --target=x86_64-w64-mingw32
 0:00.97   LIBCLANG_PATH=/usr/lib/llvm-18/lib
 0:00.97   CXX=clang++ --target=x86_64-w64-mingw32
 0:00.97   MOZ_REQUIRE_SIGNING=
 0:00.97   RC=x86_64-w64-mingw32-windres
 0:00.97   LLVM_DLLTOOL=llvm-dlltool-18
 0:00.97   FXC=/usr/local/bin/fxc2.exe
 0:00.97   AR=x86_64-w64-mingw32-ar
 0:00.97   WINDRES=x86_64-w64-mingw32-windres
 0:00.97   MINGW_TRIPLE=x86_64-w64-mingw32
 0:00.97 checking for vcs source checkout... no
 0:01.02 checking for a shell... /usr/bin/sh
 0:01.05 checking for host system type... x86_64-pc-linux-gnu
 0:01.06 checking for target system type... x86_64-pc-mingw32
 0:01.28 checking whether cross compiling... yes
 0:01.35 checking for Python 3... /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7/_virtualenvs/build/bin/python (3.11.15)
 0:01.36 checking for wget... /usr/bin/wget
 0:01.36 checking for ccache... not found
 0:01.36 checking for the target C compiler... /usr/bin/clang
 0:01.42 checking whether the target C compiler can be used... yes
 0:01.42 checking the target C compiler version... 18.1.8
 0:01.44 checking the target C compiler works... yes
 0:01.44 checking for the target C++ compiler... /usr/bin/clang++
 0:01.48 checking whether the target C++ compiler can be used... yes
 0:01.48 checking the target C++ compiler version... 18.1.8
 0:01.50 checking the target C++ compiler works... yes
 0:01.50 checking for the host C compiler... /usr/bin/clang
 0:01.52 checking whether the host C compiler can be used... yes
 0:01.52 checking the host C compiler version... 18.1.8
 0:01.54 checking the host C compiler works... yes
 0:01.55 checking for the host C++ compiler... /usr/bin/clang++
 0:01.57 checking whether the host C++ compiler can be used... yes
 0:01.57 checking the host C++ compiler version... 18.1.8
 0:01.59 checking the host C++ compiler works... yes
 0:01.63 checking for host linker... lld
 0:01.69 checking for 64-bit OS... yes
 0:01.71 checking for new enough STL headers from libstdc++... yes
 0:01.78 checking for __thread keyword for TLS variables... yes
 0:01.78 checking for Windows SDK... no
 0:01.78 checking for Universal CRT SDK... no
 0:01.78 checking for linker... /usr/bin/lld-link
 0:01.80 checking for w32api version >= 3.14... yes
 0:01.81 checking for the assembler... /usr/bin/clang
 0:01.83 checking for llvm-objdump... /usr/bin/llvm-objdump
 0:01.83 checking for rc... /usr/bin/x86_64-w64-mingw32-windres
 0:01.85 checking for ar... /usr/bin/x86_64-w64-mingw32-ar
 0:01.87 checking whether ar supports response files... no
 0:01.89 checking for host_ar... /usr/bin/llvm-ar
 0:01.93 checking for -mavxvnni support... yes
 0:01.95 checking for -mavx512bw support... yes
 0:01.97 checking for -mavx512vnni support... yes
 0:02.00 checking for malloc.h... yes
 0:02.03 checking for stdint.h... yes
 0:02.05 checking for inttypes.h... yes
 0:02.07 checking for alloca.h... no
 0:02.09 checking for sys/byteorder.h... no
 0:02.12 checking for getopt.h... yes
 0:02.15 checking for unistd.h... yes
 0:02.17 checking for nl_types.h... no
 0:02.19 checking for cpuid.h... yes
 0:02.21 checking for fts.h... no
 0:02.23 checking for sys/statvfs.h... no
 0:02.25 checking for sys/statfs.h... no
 0:02.27 checking for sys/vfs.h... no
 0:02.29 checking for sys/mount.h... no
 0:02.31 checking for sys/quota.h... no
 0:02.33 checking for sys/queue.h... no
 0:02.35 checking for sys/types.h... yes
 0:02.38 checking for netinet/in.h... no
 0:02.40 checking for byteswap.h... no
 0:02.42 checking for memfd_create in sys/mman.h... no
 0:02.47 checking for clock_gettime(CLOCK_MONOTONIC)... no
 0:02.53 checking for clock_gettime(CLOCK_MONOTONIC) in rt... no
 0:02.57 checking for res_ninit()... no
 0:02.62 checking for dladdr... no
 0:02.67 checking for dladdr in -ldl... no
 0:02.69 checking for dlfcn.h... no
 0:02.74 checking for dlopen in -ldl... no
 0:02.80 checking for dlopen... no
 0:02.85 checking for gethostbyname_r in -lc_r... no
 0:02.90 checking for socket in -lsocket... no
 0:02.95 checking for pthread_create... no
 0:03.01 checking for pthread_create in -lpthread... yes
 0:03.04 checking for pthread.h... yes
 0:03.06 checking whether the C compiler supports -pthread... yes
 0:03.16 checking whether 64-bits std::atomic requires -latomic... no
 0:03.18 checking whether the C compiler supports -Wbitfield-enum-conversion... yes
 0:03.20 checking whether the C++ compiler supports -Wbitfield-enum-conversion... yes
 0:03.22 checking whether the C compiler supports -Wformat-type-confusion... yes
 0:03.25 checking whether the C++ compiler supports -Wformat-type-confusion... yes
 0:03.27 checking whether the C compiler supports -Wshadow-field-in-constructor-modified... yes
 0:03.29 checking whether the C++ compiler supports -Wshadow-field-in-constructor-modified... yes
 0:03.31 checking whether the C compiler supports -Wtautological-constant-in-range-compare... yes
 0:03.34 checking whether the C++ compiler supports -Wtautological-constant-in-range-compare... yes
 0:03.36 checking whether the C compiler supports -Wno-error=tautological-type-limit-compare... yes
 0:03.38 checking whether the C++ compiler supports -Wno-error=tautological-type-limit-compare... yes
 0:03.40 checking whether the C compiler supports -Wunreachable-code-return... yes
 0:03.43 checking whether the C++ compiler supports -Wunreachable-code-return... yes
 0:03.45 checking whether the C compiler supports -Wunused-but-set-parameter... yes
 0:03.47 checking whether the C++ compiler supports -Wunused-but-set-parameter... yes
 0:03.50 checking whether the C compiler supports -Wclass-varargs... yes
 0:03.52 checking whether the C++ compiler supports -Wclass-varargs... yes
 0:03.54 checking whether the C++ compiler supports -Wempty-init-stmt... yes
 0:03.56 checking whether the C compiler supports -Wfloat-overflow-conversion... yes
 0:03.59 checking whether the C++ compiler supports -Wfloat-overflow-conversion... yes
 0:03.61 checking whether the C compiler supports -Wfloat-zero-conversion... yes
 0:03.63 checking whether the C++ compiler supports -Wfloat-zero-conversion... yes
 0:03.65 checking whether the C compiler supports -Wloop-analysis... yes
 0:03.68 checking whether the C++ compiler supports -Wloop-analysis... yes
 0:03.70 checking whether the C compiler supports -Wno-range-loop-analysis... yes
 0:03.72 checking whether the C++ compiler supports -Wno-range-loop-analysis... yes
 0:03.74 checking whether the C++ compiler supports -Wcomma-subscript... no
 0:03.76 checking whether the C compiler supports -Wenum-compare-conditional... yes
 0:03.78 checking whether the C++ compiler supports -Wenum-compare-conditional... yes
 0:03.80 checking whether the C compiler supports -Wenum-float-conversion... yes
 0:03.83 checking whether the C++ compiler supports -Wenum-float-conversion... yes
 0:03.84 checking whether the C++ compiler supports -Wvolatile... no
 0:03.87 checking whether the C++ compiler supports -Wno-deprecated-anon-enum-enum-conversion... yes
 0:03.89 checking whether the C++ compiler supports -Wno-deprecated-enum-enum-conversion... yes
 0:03.91 checking whether the C++ compiler supports -Wno-deprecated-this-capture... yes
 0:03.94 checking whether the C++ compiler supports -Wcomma... yes
 0:03.96 checking whether the C compiler supports -Wduplicated-cond... no
 0:03.97 checking whether the C++ compiler supports -Wduplicated-cond... no
 0:04.00 checking whether the C++ compiler supports -Wimplicit-fallthrough... yes
 0:04.02 checking whether the C compiler supports -Wlogical-op... no
 0:04.03 checking whether the C++ compiler supports -Wlogical-op... no
 0:04.06 checking whether the C compiler supports -Wstring-conversion... yes
 0:04.08 checking whether the C++ compiler supports -Wstring-conversion... yes
 0:04.11 checking whether the C++ compiler supports -Wno-inline-new-delete... yes
 0:04.13 checking whether the C compiler supports -Wno-error=maybe-uninitialized... no
 0:04.14 checking whether the C++ compiler supports -Wno-error=maybe-uninitialized... no
 0:04.17 checking whether the C compiler supports -Wno-error=deprecated-declarations... yes
 0:04.19 checking whether the C++ compiler supports -Wno-error=deprecated-declarations... yes
 0:04.21 checking whether the C compiler supports -Wno-error=array-bounds... yes
 0:04.23 checking whether the C++ compiler supports -Wno-error=array-bounds... yes
 0:04.25 checking whether the C compiler supports -Wno-error=free-nonheap-object... yes
 0:04.28 checking whether the C++ compiler supports -Wno-error=free-nonheap-object... yes
 0:04.30 checking whether the C compiler supports -Wno-multistatement-macros... no
 0:04.32 checking whether the C++ compiler supports -Wno-multistatement-macros... no
 0:04.33 checking whether the C compiler supports -Wno-error=class-memaccess... no
 0:04.35 checking whether the C++ compiler supports -Wno-error=class-memaccess... no
 0:04.37 checking whether the C compiler supports -Wno-error=atomic-alignment... yes
 0:04.40 checking whether the C++ compiler supports -Wno-error=atomic-alignment... yes
 0:04.42 checking whether the C compiler supports -Wno-error=deprecated-builtins... yes
 0:04.44 checking whether the C++ compiler supports -Wno-error=deprecated-builtins... yes
 0:04.46 checking whether the C compiler supports -Wno-unknown-pragmas... yes
 0:04.48 checking whether the C++ compiler supports -Wno-unknown-pragmas... yes
 0:04.51 checking whether the C compiler supports -Wno-unused-function... yes
 0:04.53 checking whether the C++ compiler supports -Wno-unused-function... yes
 0:04.55 checking whether the C compiler supports -Wno-conversion-null... yes
 0:04.58 checking whether the C++ compiler supports -Wno-conversion-null... yes
 0:04.60 checking whether the C compiler supports -Wno-switch... yes
 0:04.62 checking whether the C++ compiler supports -Wno-switch... yes
 0:04.64 checking whether the C compiler supports -Wno-enum-compare... yes
 0:04.67 checking whether the C++ compiler supports -Wno-enum-compare... yes
 0:04.70 checking whether the C compiler supports -Werror=implicit-function-declaration... yes
 0:04.72 checking whether the C compiler supports -Wno-psabi... yes
 0:04.74 checking whether the C++ compiler supports -Wno-psabi... yes
 0:04.77 checking whether the C compiler supports -Wthread-safety... yes
 0:04.79 checking whether the C++ compiler supports -Wthread-safety... yes
 0:04.81 checking whether the C compiler supports -Wno-error=builtin-macro-redefined... yes
 0:04.83 checking whether the C++ compiler supports -Wno-error=builtin-macro-redefined... yes
 0:04.86 checking whether the C++ compiler supports -Wno-vla-cxx-extension... yes
 0:04.88 checking whether the C compiler supports -Wno-unknown-warning-option... yes
 0:04.91 checking whether the C++ compiler supports -Wno-unknown-warning-option... yes
 0:04.94 checking whether the C++ compiler supports -fno-sized-deallocation... yes
 0:04.96 checking whether the C++ compiler supports -fno-aligned-new... yes
 0:05.00 checking whether the linker supports Identical Code Folding... no
 0:05.06 checking whether the C linker supports -Wl,--build-id=sha1... yes
 0:05.08 checking whether the C assembler supports -Wa,--noexecstack... yes
 0:05.12 checking whether the C linker supports -Wl,-z,noexecstack... no
 0:05.16 checking whether the C linker supports -Wl,-z,text... no
 0:05.20 checking whether the C linker supports -Wl,-z,relro... no
 0:05.24 checking whether the C linker supports -Wl,-z,now... no
 0:05.28 checking whether the C linker supports -Wl,-z,nocopyreloc... no
 0:05.33 checking what kind of list files are supported by the linker... linkerlist
 0:05.33 checking for llvm_profdata... not found
 0:05.37 checking for readelf... /usr/bin/llvm-readelf
 0:05.40 checking for objcopy... /usr/bin/llvm-objcopy
 0:05.40 checking for rustc... /home/runner/.cargo/bin/rustc
 0:05.40 checking for cargo... /home/runner/.cargo/bin/cargo
 0:05.43 Actually using '/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc'
 0:05.47 Actually using '/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/cargo'
 0:05.48 checking rustc version... 1.94.1
 0:05.50 checking cargo version... 1.94.1
 0:05.73 checking for rust host triplet... x86_64-unknown-linux-gnu
 0:05.82 checking for rust target triplet... x86_64-pc-windows-gnu
 0:05.82 checking for rustdoc... /home/runner/.cargo/bin/rustdoc
 0:05.82 checking for cbindgen... /usr/bin/cbindgen
 0:05.83 checking for rustfmt... /home/runner/.cargo/bin/rustfmt
 0:05.83 checking for clang for bindgen... /usr/bin/clang++
 0:05.83 checking for libclang for bindgen... /usr/lib/llvm-18/lib/libclang.so
 0:05.84 checking that libclang is new enough... yes
 0:05.84 checking bindgen cflags... -x c++ -fno-sized-deallocation -fno-aligned-new -DTRACING=1 -DIMPL_LIBXUL -DMOZILLA_INTERNAL_API -DRUST_BINDGEN -DWIN32=1 --target=x86_64-w64-mingw32
 0:05.86 checking for tm_zone and tm_gmtoff in struct tm... no
 0:05.92 checking for _getc_nolock... yes
 0:05.98 checking for localeconv... yes
 0:06.03 checking for nodejs... /usr/local/bin/node (20.20.2)
 0:06.03 checking for tar... /usr/bin/tar
 0:06.03 checking for unzip... /usr/bin/unzip
 0:06.03 checking for the Mozilla API key... no
 0:06.03 checking for the Google Location Service API key... no
 0:06.03 checking for the Google Safebrowsing API key... no
 0:06.03 checking for the Bing API key... no
 0:06.03 checking for the Adjust SDK key... no
 0:06.03 checking for the Leanplum SDK key... no
 0:06.03 checking for the Pocket API key... no
 0:06.04 checking for midl... not found
 0:06.04 checking for llvm-dlltool... /usr/bin/llvm-dlltool-18
 0:06.04 checking for fxc... /usr/local/bin/fxc2.exe
 0:06.04 checking for nasm... /usr/bin/nasm
 0:06.04 checking nasm version... 2.16.01
 0:06.04 checking for dxcompiler.dll and dxil.dll... <ReadOnlyNamespace {'enabled': False}>
 0:06.04 checking for dump_syms... not found
 0:06.05 checking for pdbstr... not found
 0:06.05 checking for winchecksec... not found
 0:06.05 checking for wine... /usr/bin/wine
 0:06.07 checking for sin_len in struct sockaddr_in... no
 0:06.09 checking for sin_len6 in struct sockaddr_in6... no
 0:06.11 checking for sa_len in struct sockaddr... no
 0:06.14 checking for pthread_cond_timedwait_monotonic_np... no
 0:06.16 checking for the windows rust crate source... no
 0:06.16 ERROR: Cannot find the windows rust crate source.
 0:06.16 Try downloading it with `cargo download -x windows=0.58.0`
 0:06.16 (you may need to `cargo install cargo-download` first)
 0:06.16 and set `MOZ_WINDOWS_RS_DIR` to location of the `windows-0.58.0` directory
 0:06.23 W Exception when writing resource usage file: [Errno 2] No such file or directory: '/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-x86_64-pc-mingw32/.mozbuild/profile_build_resources.json'
 Config object not found by mach.
*** Fix above errors and then restart with "./mach build"
make: *** [Makefile:132: build] Error 1

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.

build (windows, i686, ubuntu-24.04)

Build

Run python3 ./multibuild.py --target windows --arch i686
python3 scripts/patch.py 135.0.1 beta.24 --mozconfig-only
~/.cargo/bin/rustup target add "x86_64-pc-windows-gnu"
info: downloading component rust-std
~/.cargo/bin/rustup target add "i686-pc-windows-gnu"
info: downloading component rust-std
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: i686-pc-mingw32
-> Updating mozconfig, target is i686-pc-mingw32
Complete!
rm -rf camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox-bin \
	camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox
make[1]: Entering directory '/home/runner/work/firefox/firefox'
python3 scripts/patch.py 135.0.1 beta.24
~/.cargo/bin/rustup target add "x86_64-pc-windows-gnu"
info: component rust-std for target x86_64-pc-windows-gnu is up to date
~/.cargo/bin/rustup target add "i686-pc-windows-gnu"
info: component rust-std for target i686-pc-windows-gnu is up to date
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: i686-pc-mingw32
-> Updating mozconfig, target is i686-pc-mingw32

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/ghostery/Disable-Onboarding-Messages.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/ghostery/Disable-Onboarding-Messages.patch
patching file browser/components/asrouter/modules/OnboardingMessageProvider.sys.mjs
Hunk #1 succeeded at 1370 (offset 155 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/all-addons-private-mode.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/all-addons-private-mode.patch
patching file toolkit/components/extensions/Extension.sys.mjs
Hunk #1 succeeded at 3892 (offset 606 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/allow-searchengines-non-esr.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/allow-searchengines-non-esr.patch
patching file browser/components/enterprisepolicies/schemas/policies-schema.json
Hunk #1 succeeded at 1385 (offset 311 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/anti-font-fingerprinting.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/anti-font-fingerprinting.patch
patching file gfx/thebes/gfxHarfBuzzShaper.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/audio-context-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/audio-context-spoofing.patch
patching file dom/media/CubebUtils.cpp
Hunk #1 succeeded at 43 (offset 3 lines).
Hunk #2 succeeded at 411 (offset 11 lines).
patching file dom/media/moz.build
patching file dom/media/webaudio/AudioContext.cpp
Hunk #2 succeeded at 556 (offset -6 lines).
Hunk #3 succeeded at 712 (offset -6 lines).
patching file dom/media/webaudio/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/bootstrap.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/bootstrap.patch
patching file python/mozversioncontrol/mozversioncontrol/repo/source.py

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/browser-init.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/browser-init.patch
patching file browser/base/content/browser-init.js
Hunk #3 succeeded at 120 with fuzz 2 (offset 1 line).
Hunk #4 succeeded at 320 (offset -16 lines).
Hunk #5 succeeded at 371 (offset -16 lines).
Hunk #6 succeeded at 417 (offset -16 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/chromeutil.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/chromeutil.patch
patching file dom/base/ChromeUtils.cpp
Hunk #2 succeeded at 2416 (offset 299 lines).
Hunk #3 succeeded at 2460 (offset 299 lines).
patching file dom/base/ChromeUtils.h
Hunk #1 succeeded at 315 (offset 10 lines).
Hunk #2 succeeded at 328 (offset 10 lines).
patching file dom/chrome-webidl/ChromeUtils.webidl
Hunk #1 succeeded at 769 (offset 19 lines).
Hunk #2 succeeded at 787 (offset 19 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/config.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/config.patch
patching file browser/installer/package-manifest.in
Hunk #1 succeeded at 256 (offset 12 lines).
patching file lw/moz.build
patching file moz.build
Hunk #1 succeeded at 226 with fuzz 1 (offset 6 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/context-menu.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/context-menu.patch
patching file browser/base/content/browser-context.inc
Hunk #1 succeeded at 106 (offset -1 lines).
Hunk #2 succeeded at 259 (offset -2 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/custom-ubo-assets-bootstrap-location.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/custom-ubo-assets-bootstrap-location.patch
patching file toolkit/components/extensions/parent/ext-storage.js
Hunk #1 succeeded at 403 (offset 226 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/dbus_name.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/dbus_name.patch
patching file toolkit/components/remote/nsDBusRemoteClient.cpp
Hunk #3 succeeded at 121 (offset 4 lines).
Hunk #4 succeeded at 132 (offset 4 lines).
patching file toolkit/components/remote/nsDBusRemoteServer.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/devtools-bypass.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/devtools-bypass.patch
patching file devtools/server/actors/thread.js
patching file devtools/server/actors/webconsole/listeners/console-api.js
Hunk #1 succeeded at 97 with fuzz 1.

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/disable-data-reporting-at-compile-time.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/disable-data-reporting-at-compile-time.patch
patching file browser/moz.configure
patching file python/mach/mach/telemetry.py
Hunk #1 succeeded at 95 (offset -3 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/disable-extension-newtab.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/disable-extension-newtab.patch
patching file browser/components/extensions/parent/ext-browser.js
patching file browser/components/extensions/parent/ext-tabs.js

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/disable-pocket.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/disable-pocket.patch
patching file browser/base/content/browser.js
Hunk #1 succeeded at 3399 with fuzz 2 (offset -2079 lines).
patching file browser/components/BrowserGlue.sys.mjs
Hunk #1 succeeded at 1585 with fuzz 2 (offset 311 lines).
patching file browser/components/moz.build
Hunk #1 succeeded at 48 (offset 4 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/disable-remote-subframes.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/disable-remote-subframes.patch
patching file docshell/base/BrowsingContext.cpp
Hunk #2 succeeded at 1770 (offset -3 lines).
patching file docshell/base/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/fingerprint-injection.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/fingerprint-injection.patch
patching file browser/app/moz.build
patching file dom/base/Element.cpp
Hunk #1 succeeded at 12 with fuzz 2.
Hunk #2 succeeded at 1012 (offset 27 lines).
patching file dom/base/Navigator.cpp
Hunk #6 succeeded at 374 with fuzz 1 (offset -1 lines).
Hunk #7 succeeded at 429 (offset -4 lines).
Hunk #8 succeeded at 452 (offset -10 lines).
Hunk #9 succeeded at 484 (offset -10 lines).
Hunk #10 succeeded at 529 (offset -10 lines).
Hunk #11 succeeded at 570 (offset -10 lines).
Hunk #12 succeeded at 600 (offset -10 lines).
Hunk #13 succeeded at 649 (offset -10 lines).
Hunk #14 succeeded at 665 (offset -10 lines).
Hunk #15 succeeded at 727 (offset -10 lines).
Hunk #16 succeeded at 747 (offset -10 lines).
Hunk #17 succeeded at 762 (offset -10 lines).
Hunk #18 succeeded at 964 (offset -10 lines).
patching file dom/base/moz.build
Hunk #1 succeeded at 659 (offset 18 lines).
patching file dom/base/nsGlobalWindowInner.cpp
Hunk #2 succeeded at 3425 (offset 14 lines).
Hunk #3 succeeded at 3439 (offset 14 lines).
Hunk #4 succeeded at 3458 (offset 14 lines).
Hunk #5 succeeded at 3486 (offset 14 lines).
Hunk #6 succeeded at 3530 (offset 14 lines).
Hunk #7 succeeded at 3604 (offset 14 lines).
patching file dom/base/nsHistory.cpp
patching file dom/base/nsScreen.cpp
Hunk #3 succeeded at 91 with fuzz 1 (offset -3 lines).
patching file dom/battery/BatteryManager.cpp
patching file dom/battery/moz.build
patching file dom/workers/WorkerNavigator.cpp
Hunk #2 succeeded at 104 (offset 11 lines).
Hunk #3 succeeded at 130 (offset 11 lines).
Hunk #4 succeeded at 158 (offset 11 lines).
Hunk #5 succeeded at 224 (offset 7 lines).
Hunk #6 succeeded at 241 (offset 7 lines).
patching file dom/workers/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/firefox-view.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/firefox-view.patch
patching file browser/base/content/navigator-toolbox.inc.xhtml
Hunk #2 succeeded at 663 (offset 4 lines).
patching file browser/components/customizableui/CustomizableUI.sys.mjs
Hunk #1 succeeded at 356 (offset 9 lines).
Hunk #2 succeeded at 715 (offset 9 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/font-hijacker.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/font-hijacker.patch
patching file gfx/thebes/gfxPlatformFontList.cpp
patching file gfx/thebes/moz.build
Hunk #1 succeeded at 303 (offset -2 lines).
patching file layout/style/FontFace.cpp
Hunk #1 succeeded at 243 (offset 6 lines).
Hunk #2 succeeded at 262 (offset 6 lines).
patching file layout/style/FontFaceImpl.cpp
Hunk #1 succeeded at 358 (offset 1 line).
patching file layout/style/FontFaceImpl.h
Hunk #1 succeeded at 8 with fuzz 2.
Hunk #2 succeeded at 33 (offset -3 lines).
patching file layout/style/moz.build
Hunk #1 succeeded at 366 (offset 15 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/force-default-pointer.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/force-default-pointer.patch
patching file layout/style/nsMediaFeatures.cpp
Hunk #1 succeeded at 376 (offset 4 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/geolocation-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/geolocation-spoofing.patch
patching file dom/geolocation/Geolocation.cpp
Hunk #1 succeeded at 39 (offset 5 lines).
Hunk #2 succeeded at 1427 with fuzz 2 (offset 159 lines).
patching file dom/geolocation/GeolocationPosition.cpp
patching file dom/geolocation/moz.build
Hunk #1 succeeded at 81 (offset 23 lines).
patching file dom/system/NetworkGeolocationProvider.sys.mjs

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/global-style-sheets.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/global-style-sheets.patch
patching file layout/style/GlobalStyleSheetCache.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/handlers.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/handlers.patch
patching file uriloader/exthandler/HandlerList.sys.mjs

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/hide-default-browser.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/hide-default-browser.patch
patching file browser/components/preferences/main.inc.xhtml
Hunk #2 succeeded at 54 (offset 6 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/locale-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/locale-spoofing.patch
patching file intl/components/src/Locale.cpp
patching file intl/components/src/Locale.h
patching file intl/locale/OSPreferences.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/macos-backgroundtasks-disabled.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/macos-backgroundtasks-disabled.patch
patching file toolkit/xre/nsAppRunner.cpp
Hunk #1 succeeded at 5669 (offset 36 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/media-device-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/media-device-spoofing.patch
patching file dom/media/MediaDevices.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/mozilla_dirs.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/mozilla_dirs.patch
patching file toolkit/xre/nsXREDirProvider.cpp
Hunk #1 succeeded at 285 with fuzz 1 (offset -15 lines).
Hunk #2 succeeded at 366 (offset -5 lines).
Hunk #3 succeeded at 398 with fuzz 2 (offset -13 lines).
Hunk #4 succeeded at 932 (offset -182 lines).
Hunk #5 succeeded at 1192 (offset -171 lines).
Hunk #6 succeeded at 1202 (offset -171 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/network-patches.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/network-patches.patch
patching file netwerk/protocol/http/moz.build
Hunk #1 succeeded at 234 (offset 16 lines).
patching file netwerk/protocol/http/nsHttpHandler.cpp
Hunk #2 succeeded at 885 (offset 137 lines).
Hunk #3 succeeded at 1997 (offset 149 lines).
Hunk #4 succeeded at 2019 (offset 149 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-css-animations.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-css-animations.patch
patching file dom/animation/AnimationEffect.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-search-engines.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-search-engines.patch
patching file toolkit/components/search/SearchEngineSelector.sys.mjs
Hunk #1 succeeded at 181 (offset 23 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/nss-tls-override.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/nss-tls-override.patch
patching file security/manager/ssl/nsNSSComponent.cpp
Hunk #2 succeeded at 1617 with fuzz 1.
patching file security/manager/ssl/moz.build
Hunk #1 succeeded at 199 with fuzz 1.

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/pin-addons.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/pin-addons.patch
patching file browser/base/content/browser-addons.js
Hunk #1 succeeded at 2393 (offset 469 lines).
patching file browser/base/content/main-popupset.inc.xhtml
Hunk #1 succeeded at 365 (offset 79 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-branding-urlbar.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-branding-urlbar.patch
patching file browser/locales/en-US/browser/browser.ftl
Hunk #1 succeeded at 715 (offset 172 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-cfrprefs.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-cfrprefs.patch
patching file browser/components/preferences/main.inc.xhtml
Hunk #1 succeeded at 775 (offset 33 lines).
Hunk #2 succeeded at 785 (offset 33 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-organization-policy-banner.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-organization-policy-banner.patch
patching file browser/components/preferences/preferences.js
Hunk #1 succeeded at 241 (offset 7 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/remove_addons.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/remove_addons.patch
patching file browser/extensions/moz.build
patching file browser/locales/Makefile.in
Hunk #1 succeeded at 55 (offset -1 lines).
Hunk #2 succeeded at 75 (offset -2 lines).
patching file browser/locales/filter.py
Hunk #1 succeeded at 15 (offset -2 lines).
patching file browser/locales/l10n.ini
patching file browser/locales/l10n.toml
Hunk #1 succeeded at 135 (offset 2 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/rust-gentoo-musl.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/rust-gentoo-musl.patch
patching file build/moz.configure/rust.configure

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/screen-hijacker.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/screen-hijacker.patch
patching file dom/base/nsScreen.cpp
patching file gfx/src/moz.build
patching file gfx/src/nsDeviceContext.cpp
patching file layout/style/nsMediaFeatures.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/shadow-root-bypass.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/shadow-root-bypass.patch
patching file dom/webidl/Element.webidl

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch
patching file browser/components/asrouter/content/asrouter-admin.bundle.js
Hunk #1 succeeded at 1144 with fuzz 1.
patching file services/settings/Utils.sys.mjs
Hunk #1 succeeded at 51 (offset -3 lines).
patching file toolkit/components/search/SearchUtils.sys.mjs
Hunk #1 succeeded at 169 (offset -3 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/timezone-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/timezone-spoofing.patch
patching file intl/components/moz.build
patching file intl/components/src/TimeZone.cpp
Hunk #2 succeeded at 22 (offset -1 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/urlbarprovider-interventions.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/urlbarprovider-interventions.patch
patching file browser/components/urlbar/UrlbarProviderInterventions.sys.mjs
Hunk #1 succeeded at 453 (offset -1 lines).
Hunk #2 succeeded at 495 (offset 1 line).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/voice-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/voice-spoofing.patch
patching file dom/media/webspeech/synth/moz.build
patching file dom/media/webspeech/synth/nsSynthVoiceRegistry.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/webgl-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/webgl-spoofing.patch
patching file dom/canvas/ClientWebGLContext.cpp
Hunk #2 succeeded at 754 (offset 1 line).
Hunk #3 succeeded at 771 (offset 1 line).
Hunk #4 succeeded at 1022 (offset 1 line).
Hunk #5 succeeded at 2112 (offset 1 line).
Hunk #6 succeeded at 2268 (offset 1 line).
Hunk #7 succeeded at 2525 (offset 1 line).
Hunk #8 succeeded at 2538 (offset 1 line).
Hunk #9 succeeded at 2635 (offset 2 lines).
Hunk #10 succeeded at 3020 (offset 2 lines).
Hunk #11 succeeded at 6018 (offset 2 lines).
Hunk #12 succeeded at 6040 (offset 2 lines).
patching file dom/canvas/ClientWebGLContext.h
Hunk #1 succeeded at 1073 (offset -1 lines).
patching file dom/canvas/moz.build
Hunk #1 succeeded at 228 (offset 7 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/webrtc-ip-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/webrtc-ip-spoofing.patch
patching file dom/media/webrtc/jsapi/PeerConnectionImpl.cpp
patching file dom/media/webrtc/jsapi/PeerConnectionImpl.h
patching file dom/media/webrtc/jsapi/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/windows-theming-bug-modified.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/windows-theming-bug-modified.patch
patching file browser/app/Makefile.in
patching file browser/app/camoufox.exe.manifest (renamed from browser/app/firefox.exe.manifest)

--- Applied 48 patch(es) successfully ---
Complete!
touch camoufox-135.0.1-beta.24/_READY
make[1]: Leaving directory '/home/runner/work/firefox/firefox'
cd camoufox-135.0.1-beta.24 && ./mach build 
Collecting glean-sdk==63.0.0
  Downloading glean_sdk-63.0.0-py3-none-manylinux_2_34_x86_64.whl.metadata (4.8 kB)
Collecting semver>=2.13.0 (from glean-sdk==63.0.0)
  Downloading semver-3.0.4-py3-none-any.whl.metadata (6.8 kB)
Requirement already satisfied: glean-parser~=16.1 in ./third_party/python/glean_parser (from glean-sdk==63.0.0) (16.1.0)
Requirement already satisfied: Click>=7 in ./third_party/python/click (from glean-parser~=16.1->glean-sdk==63.0.0) (8.1.6)
Requirement already satisfied: diskcache>=4 in ./third_party/python/diskcache (from glean-parser~=16.1->glean-sdk==63.0.0) (5.6.3)
Requirement already satisfied: Jinja2>=2.10.1 in ./third_party/python/Jinja2 (from glean-parser~=16.1->glean-sdk==63.0.0) (3.1.2)
Requirement already satisfied: jsonschema>=3.0.2 in ./third_party/python/jsonschema (from glean-parser~=16.1->glean-sdk==63.0.0) (4.17.3)
Requirement already satisfied: platformdirs>=2.4.0 in ./third_party/python/platformdirs (from glean-parser~=16.1->glean-sdk==63.0.0) (4.3.6)
Requirement already satisfied: PyYAML>=5.3.1 in ./third_party/python/PyYAML/lib (from glean-parser~=16.1->glean-sdk==63.0.0) (6.0.1)
Requirement already satisfied: MarkupSafe>=2.0 in ./third_party/python/MarkupSafe/src (from Jinja2>=2.10.1->glean-parser~=16.1->glean-sdk==63.0.0) (2.0.1)
Requirement already satisfied: attrs>=17.4.0 in ./third_party/python/attrs (from jsonschema>=3.0.2->glean-parser~=16.1->glean-sdk==63.0.0) (23.1.0)
Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in ./third_party/python/pyrsistent (from jsonschema>=3.0.2->glean-parser~=16.1->glean-sdk==63.0.0) (0.20.0)
Downloading glean_sdk-63.0.0-py3-none-manylinux_2_34_x86_64.whl (861 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 861.6/861.6 kB 19.1 MB/s eta 0:00:00
Downloading semver-3.0.4-py3-none-any.whl (17 kB)
Installing collected packages: semver, glean-sdk
Successfully installed glean-sdk-63.0.0 semver-3.0.4
Collecting psutil<=5.9.4,>=5.4.2
  Downloading psutil-5.9.4-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (21 kB)
Downloading psutil-5.9.4-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (280 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 280.2/280.2 kB 16.0 MB/s eta 0:00:00
Installing collected packages: psutil
Successfully installed psutil-5.9.4
Collecting zstandard<=0.23.0,>=0.11.1
  Downloading zstandard-0.23.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (3.0 kB)
Downloading zstandard-0.23.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (5.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 25.9 MB/s eta 0:00:00
Installing collected packages: zstandard
Successfully installed zstandard-0.23.0
Mach and the build system store shared state in a common directory
on the filesystem. The following directory will be created:

  /home/runner/.mozbuild

If you would like to use a different directory, rename or move it to your
desired location, and set the MOZBUILD_STATE_PATH environment variable
accordingly.
Creating default state directory: /home/runner/.mozbuild
Creating local state directory: /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7
 0:00.80 W Clobber not needed.
 0:00.99 Using Python 3.11.15 from /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7/_virtualenvs/build/bin/python
 0:00.99 Adding configure options from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/mozconfig
 0:00.99   --enable-application=browser
 0:00.99   --allow-addon-sideload
 0:00.99   --disable-crashreporter
 0:00.99   --disable-backgroundtasks
 0:00.99   --disable-debug
 0:00.99   --disable-default-browser-agent
 0:00.99   --disable-tests
 0:00.99   --disable-updater
 0:00.99   --enable-release
 0:00.99   --disable-system-policies
 0:00.99   --without-wasm-sandboxed-libraries
 0:00.99   --with-app-name=camoufox
 0:00.99   --with-branding=browser/branding/camoufox
 0:00.99   --with-unsigned-addon-scopes=app,system
 0:00.99   --disable-bootstrap
 0:00.99   --with-libclang-path=/usr/lib/llvm-18/lib
 0:00.99   --target=i686-pc-mingw32
 0:00.99   --disable-maintenance-service
 0:00.99   --disable-update-agent
 0:00.99   --disable-accessibility
 0:00.99   WINDRES=i686-w64-mingw32-windres
 0:00.99   RC=i686-w64-mingw32-windres
 0:00.99   CC=clang --target=i686-w64-mingw32
 0:00.99   FXC=/usr/local/bin/fxc2.exe
 0:00.99   LLVM_DLLTOOL=llvm-dlltool-18
 0:00.99   CXX=clang++ --target=i686-w64-mingw32
 0:00.99   MOZ_REQUIRE_SIGNING=
 0:00.99   AR=i686-w64-mingw32-ar
 0:00.99   LIBCLANG_PATH=/usr/lib/llvm-18/lib
 0:00.99   RANLIB=i686-w64-mingw32-ranlib
 0:00.99   MINGW_TRIPLE=i686-w64-mingw32
 0:00.99 checking for vcs source checkout... no
 0:01.03 checking for a shell... /usr/bin/sh
 0:01.07 checking for host system type... x86_64-pc-linux-gnu
 0:01.07 checking for target system type... i686-pc-mingw32
 0:01.31 checking whether cross compiling... yes
 0:01.38 checking for Python 3... /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7/_virtualenvs/build/bin/python (3.11.15)
 0:01.38 checking for wget... /usr/bin/wget
 0:01.38 checking for ccache... not found
 0:01.38 checking for the target C compiler... /usr/bin/clang
 0:01.43 checking whether the target C compiler can be used... yes
 0:01.43 checking the target C compiler version... 18.1.8
 0:01.45 checking the target C compiler works... yes
 0:01.45 checking for the target C++ compiler... /usr/bin/clang++
 0:01.49 checking whether the target C++ compiler can be used... yes
 0:01.49 checking the target C++ compiler version... 18.1.8
 0:01.51 checking the target C++ compiler works... yes
 0:01.51 checking for the host C compiler... /usr/bin/clang
 0:01.54 checking whether the host C compiler can be used... yes
 0:01.54 checking the host C compiler version... 18.1.8
 0:01.56 checking the host C compiler works... yes
 0:01.56 checking for the host C++ compiler... /usr/bin/clang++
 0:01.59 checking whether the host C++ compiler can be used... yes
 0:01.59 checking the host C++ compiler version... 18.1.8
 0:01.61 checking the host C++ compiler works... yes
 0:01.64 checking for host linker... lld
 0:01.71 checking for 64-bit OS... no
 0:01.74 checking for new enough STL headers from libstdc++... yes
 0:01.80 checking for __thread keyword for TLS variables... yes
 0:01.80 checking for Windows SDK... no
 0:01.80 checking for Universal CRT SDK... no
 0:01.80 checking for linker... /usr/bin/lld-link
 0:01.83 checking for w32api version >= 3.14... yes
 0:01.83 checking for the assembler... /usr/bin/clang
 0:01.85 checking for llvm-objdump... /usr/bin/llvm-objdump
 0:01.85 checking for rc... /usr/bin/i686-w64-mingw32-windres
 0:01.87 checking for ar... /usr/bin/i686-w64-mingw32-ar
 0:01.90 checking whether ar supports response files... no
 0:01.92 checking for host_ar... /usr/bin/llvm-ar
 0:01.96 checking for -mavxvnni support... yes
 0:01.98 checking for -mavx512bw support... yes
 0:02.01 checking for -mavx512vnni support... yes
 0:02.04 checking for malloc.h... yes
 0:02.07 checking for stdint.h... yes
 0:02.10 checking for inttypes.h... yes
 0:02.12 checking for alloca.h... no
 0:02.14 checking for sys/byteorder.h... no
 0:02.16 checking for getopt.h... yes
 0:02.20 checking for unistd.h... yes
 0:02.22 checking for nl_types.h... no
 0:02.24 checking for cpuid.h... yes
 0:02.26 checking for fts.h... no
 0:02.29 checking for sys/statvfs.h... no
 0:02.31 checking for sys/statfs.h... no
 0:02.33 checking for sys/vfs.h... no
 0:02.35 checking for sys/mount.h... no
 0:02.37 checking for sys/quota.h... no
 0:02.40 checking for sys/queue.h... no
 0:02.42 checking for sys/types.h... yes
 0:02.44 checking for netinet/in.h... no
 0:02.47 checking for byteswap.h... no
 0:02.49 checking for memfd_create in sys/mman.h... no
 0:02.55 checking for clock_gettime(CLOCK_MONOTONIC)... no
 0:02.61 checking for clock_gettime(CLOCK_MONOTONIC) in rt... no
 0:02.65 checking for res_ninit()... no
 0:02.70 checking for dladdr... no
 0:02.76 checking for dladdr in -ldl... no
 0:02.78 checking for dlfcn.h... no
 0:02.83 checking for dlopen in -ldl... no
 0:02.89 checking for dlopen... no
 0:02.94 checking for gethostbyname_r in -lc_r... no
 0:02.99 checking for socket in -lsocket... no
 0:03.05 checking for pthread_create... no
 0:03.11 checking for pthread_create in -lpthread... yes
 0:03.15 checking for pthread.h... yes
 0:03.17 checking whether the C compiler supports -pthread... yes
 0:03.27 checking whether 64-bits std::atomic requires -latomic... no
 0:03.29 checking whether the C compiler supports -Wbitfield-enum-conversion... yes
 0:03.32 checking whether the C++ compiler supports -Wbitfield-enum-conversion... yes
 0:03.34 checking whether the C compiler supports -Wformat-type-confusion... yes
 0:03.36 checking whether the C++ compiler supports -Wformat-type-confusion... yes
 0:03.39 checking whether the C compiler supports -Wshadow-field-in-constructor-modified... yes
 0:03.41 checking whether the C++ compiler supports -Wshadow-field-in-constructor-modified... yes
 0:03.43 checking whether the C compiler supports -Wtautological-constant-in-range-compare... yes
 0:03.46 checking whether the C++ compiler supports -Wtautological-constant-in-range-compare... yes
 0:03.48 checking whether the C compiler supports -Wno-error=tautological-type-limit-compare... yes
 0:03.50 checking whether the C++ compiler supports -Wno-error=tautological-type-limit-compare... yes
 0:03.53 checking whether the C compiler supports -Wunreachable-code-return... yes
 0:03.55 checking whether the C++ compiler supports -Wunreachable-code-return... yes
 0:03.58 checking whether the C compiler supports -Wunused-but-set-parameter... yes
 0:03.60 checking whether the C++ compiler supports -Wunused-but-set-parameter... yes
 0:03.62 checking whether the C compiler supports -Wclass-varargs... yes
 0:03.65 checking whether the C++ compiler supports -Wclass-varargs... yes
 0:03.67 checking whether the C++ compiler supports -Wempty-init-stmt... yes
 0:03.70 checking whether the C compiler supports -Wfloat-overflow-conversion... yes
 0:03.72 checking whether the C++ compiler supports -Wfloat-overflow-conversion... yes
 0:03.74 checking whether the C compiler supports -Wfloat-zero-conversion... yes
 0:03.77 checking whether the C++ compiler supports -Wfloat-zero-conversion... yes
 0:03.79 checking whether the C compiler supports -Wloop-analysis... yes
 0:03.81 checking whether the C++ compiler supports -Wloop-analysis... yes
 0:03.84 checking whether the C compiler supports -Wno-range-loop-analysis... yes
 0:03.86 checking whether the C++ compiler supports -Wno-range-loop-analysis... yes
 0:03.88 checking whether the C++ compiler supports -Wcomma-subscript... no
 0:03.90 checking whether the C compiler supports -Wenum-compare-conditional... yes
 0:03.93 checking whether the C++ compiler supports -Wenum-compare-conditional... yes
 0:03.95 checking whether the C compiler supports -Wenum-float-conversion... yes
 0:03.97 checking whether the C++ compiler supports -Wenum-float-conversion... yes
 0:03.99 checking whether the C++ compiler supports -Wvolatile... no
 0:04.02 checking whether the C++ compiler supports -Wno-deprecated-anon-enum-enum-conversion... yes
 0:04.04 checking whether the C++ compiler supports -Wno-deprecated-enum-enum-conversion... yes
 0:04.07 checking whether the C++ compiler supports -Wno-deprecated-this-capture... yes
 0:04.09 checking whether the C++ compiler supports -Wcomma... yes
 0:04.11 checking whether the C compiler supports -Wduplicated-cond... no
 0:04.13 checking whether the C++ compiler supports -Wduplicated-cond... no
 0:04.15 checking whether the C++ compiler supports -Wimplicit-fallthrough... yes
 0:04.17 checking whether the C compiler supports -Wlogical-op... no
 0:04.19 checking whether the C++ compiler supports -Wlogical-op... no
 0:04.22 checking whether the C compiler supports -Wstring-conversion... yes
 0:04.24 checking whether the C++ compiler supports -Wstring-conversion... yes
 0:04.27 checking whether the C++ compiler supports -Wno-inline-new-delete... yes
 0:04.29 checking whether the C compiler supports -Wno-error=maybe-uninitialized... no
 0:04.31 checking whether the C++ compiler supports -Wno-error=maybe-uninitialized... no
 0:04.33 checking whether the C compiler supports -Wno-error=deprecated-declarations... yes
 0:04.35 checking whether the C++ compiler supports -Wno-error=deprecated-declarations... yes
 0:04.38 checking whether the C compiler supports -Wno-error=array-bounds... yes
 0:04.40 checking whether the C++ compiler supports -Wno-error=array-bounds... yes
 0:04.43 checking whether the C compiler supports -Wno-error=free-nonheap-object... yes
 0:04.45 checking whether the C++ compiler supports -Wno-error=free-nonheap-object... yes
 0:04.47 checking whether the C compiler supports -Wno-multistatement-macros... no
 0:04.49 checking whether the C++ compiler supports -Wno-multistatement-macros... no
 0:04.51 checking whether the C compiler supports -Wno-error=class-memaccess... no
 0:04.53 checking whether the C++ compiler supports -Wno-error=class-memaccess... no
 0:04.56 checking whether the C compiler supports -Wno-error=atomic-alignment... yes
 0:04.58 checking whether the C++ compiler supports -Wno-error=atomic-alignment... yes
 0:04.60 checking whether the C compiler supports -Wno-error=deprecated-builtins... yes
 0:04.63 checking whether the C++ compiler supports -Wno-error=deprecated-builtins... yes
 0:04.65 checking whether the C compiler supports -Wno-unknown-pragmas... yes
 0:04.68 checking whether the C++ compiler supports -Wno-unknown-pragmas... yes
 0:04.70 checking whether the C compiler supports -Wno-unused-function... yes
 0:04.73 checking whether the C++ compiler supports -Wno-unused-function... yes
 0:04.75 checking whether the C compiler supports -Wno-conversion-null... yes
 0:04.78 checking whether the C++ compiler supports -Wno-conversion-null... yes
 0:04.80 checking whether the C compiler supports -Wno-switch... yes
 0:04.83 checking whether the C++ compiler supports -Wno-switch... yes
 0:04.85 checking whether the C compiler supports -Wno-enum-compare... yes
 0:04.88 checking whether the C++ compiler supports -Wno-enum-compare... yes
 0:04.90 checking whether the C compiler supports -Werror=implicit-function-declaration... yes
 0:04.92 checking whether the C compiler supports -Wno-psabi... yes
 0:04.95 checking whether the C++ compiler supports -Wno-psabi... yes
 0:04.97 checking whether the C compiler supports -Wthread-safety... yes
 0:05.00 checking whether the C++ compiler supports -Wthread-safety... yes
 0:05.02 checking whether the C compiler supports -Wno-error=builtin-macro-redefined... yes
 0:05.05 checking whether the C++ compiler supports -Wno-error=builtin-macro-redefined... yes
 0:05.07 checking whether the C++ compiler supports -Wno-vla-cxx-extension... yes
 0:05.10 checking whether the C compiler supports -Wno-unknown-warning-option... yes
 0:05.12 checking whether the C++ compiler supports -Wno-unknown-warning-option... yes
 0:05.15 checking whether the C++ compiler supports -fno-sized-deallocation... yes
 0:05.17 checking whether the C++ compiler supports -fno-aligned-new... yes
 0:05.21 checking whether the linker supports Identical Code Folding... no
 0:05.27 checking whether the C linker supports -Wl,--build-id=sha1... yes
 0:05.30 checking whether the C assembler supports -Wa,--noexecstack... yes
 0:05.34 checking whether the C linker supports -Wl,-z,noexecstack... no
 0:05.38 checking whether the C linker supports -Wl,-z,text... no
 0:05.43 checking whether the C linker supports -Wl,-z,relro... no
 0:05.47 checking whether the C linker supports -Wl,-z,now... no
 0:05.51 checking whether the C linker supports -Wl,-z,nocopyreloc... no
 0:05.57 checking what kind of list files are supported by the linker... linkerlist
 0:05.57 checking for llvm_profdata... not found
 0:05.61 checking for readelf... /usr/bin/llvm-readelf
 0:05.64 checking for objcopy... /usr/bin/llvm-objcopy
 0:05.64 checking for rustc... /home/runner/.cargo/bin/rustc
 0:05.64 checking for cargo... /home/runner/.cargo/bin/cargo
 0:05.76 Actually using '/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc'
 0:06.32 Actually using '/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/cargo'
 0:06.33 checking rustc version... 1.94.1
 0:06.37 checking cargo version... 1.94.1
 0:09.41 checking for rust host triplet... x86_64-unknown-linux-gnu
 0:09.96 checking for rust target triplet... i686-pc-windows-gnu
 0:09.96 checking for rustdoc... /home/runner/.cargo/bin/rustdoc
 0:09.96 checking for cbindgen... /usr/bin/cbindgen
 0:09.96 checking for rustfmt... /home/runner/.cargo/bin/rustfmt
 0:09.96 checking for clang for bindgen... /usr/bin/clang++
 0:09.96 checking for libclang for bindgen... /usr/lib/llvm-18/lib/libclang.so
 0:09.98 checking that libclang is new enough... yes
 0:09.98 checking bindgen cflags... -x c++ -fno-sized-deallocation -fno-aligned-new -DTRACING=1 -DIMPL_LIBXUL -DMOZILLA_INTERNAL_API -DRUST_BINDGEN -DWIN32=1 --target=i686-w64-mingw32
 0:10.00 checking for tm_zone and tm_gmtoff in struct tm... no
 0:10.06 checking for _getc_nolock... yes
 0:10.12 checking for localeconv... yes
 0:10.22 checking for nodejs... /usr/local/bin/node (20.20.2)
 0:10.22 checking for tar... /usr/bin/tar
 0:10.22 checking for unzip... /usr/bin/unzip
 0:10.22 checking for the Mozilla API key... no
 0:10.22 checking for the Google Location Service API key... no
 0:10.22 checking for the Google Safebrowsing API key... no
 0:10.22 checking for the Bing API key... no
 0:10.22 checking for the Adjust SDK key... no
 0:10.22 checking for the Leanplum SDK key... no
 0:10.22 checking for the Pocket API key... no
 0:10.22 checking for midl... not found
 0:10.23 checking for llvm-dlltool... /usr/bin/llvm-dlltool-18
 0:10.23 checking for fxc... /usr/local/bin/fxc2.exe
 0:10.23 checking for nasm... /usr/bin/nasm
 0:10.23 checking nasm version... 2.16.01
 0:10.23 checking for dxcompiler.dll and dxil.dll... <ReadOnlyNamespace {'enabled': False}>
 0:10.23 checking for dump_syms... not found
 0:10.23 checking for pdbstr... not found
 0:10.23 checking for winchecksec... not found
 0:10.24 checking for wine... /usr/bin/wine
 0:10.26 checking for sin_len in struct sockaddr_in... no
 0:10.28 checking for sin_len6 in struct sockaddr_in6... no
 0:10.30 checking for sa_len in struct sockaddr... no
 0:10.33 checking for pthread_cond_timedwait_monotonic_np... no
 0:10.35 checking for the windows rust crate source... no
 0:10.35 ERROR: Cannot find the windows rust crate source.
 0:10.35 Try downloading it with `cargo download -x windows=0.58.0`
 0:10.35 (you may need to `cargo install cargo-download` first)
 0:10.35 and set `MOZ_WINDOWS_RS_DIR` to location of the `windows-0.58.0` directory
 0:10.43 W Exception when writing resource usage file: [Errno 2] No such file or directory: '/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-mingw32/.mozbuild/profile_build_resources.json'
 Config object not found by mach.
*** Fix above errors and then restart with "./mach build"
make: *** [Makefile:132: build] Error 1

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.

build (macos, x86_64, ubuntu-24.04)

Setup macos toolchain

……

[ 98%] Built target xray
[ 98%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_vector_clock.cpp.o
[ 98%] Built target fuzzer
[ 98%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_mac.cpp.o
[ 92%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_mutexset.cpp.o
[ 98%] Built target compiler-rt
[ 98%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_mach_vm.cpp.o
[ 92%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_report.cpp.o
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_platform_mac.cpp.o
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_platform_posix.cpp.o
[ 92%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl.cpp.o
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_libdispatch.cpp.o
[ 92%] Building CXX object lib/fuzzer/CMakeFiles/RTfuzzer.osx.dir/FuzzerUtil.cpp.o
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_new_delete.cpp.o
[100%] Building ASM object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_amd64.S.o
[100%] Building ASM object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_aarch64.S.o
[100%] Built target RTTsan_dynamic.osx
[ 92%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_access.cpp.o
[ 92%] Building CXX object lib/fuzzer/CMakeFiles/RTfuzzer.osx.dir/FuzzerUtilDarwin.cpp.o
[ 92%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_mutex.cpp.o
[ 92%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_proc.cpp.o
[ 93%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_report.cpp.o
[ 93%] Building CXX object lib/fuzzer/CMakeFiles/RTfuzzer.osx.dir/FuzzerUtilFuchsia.cpp.o
[ 93%] Building CXX object lib/fuzzer/CMakeFiles/RTfuzzer.osx.dir/FuzzerUtilLinux.cpp.o
[ 94%] Building CXX object lib/fuzzer/CMakeFiles/RTfuzzer.osx.dir/FuzzerUtilPosix.cpp.o
[ 94%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_thread.cpp.o
[ 94%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_stack_trace.cpp.o
[ 94%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_suppressions.cpp.o
[ 94%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_symbolize.cpp.o
[ 94%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_sync.cpp.o
[ 94%] Building CXX object lib/fuzzer/CMakeFiles/RTfuzzer.osx.dir/FuzzerUtilWindows.cpp.o
[ 94%] Built target RTfuzzer.osx
[ 94%] Linking CXX static library libRTOrc.test.osx.a
[ 94%] Built target RTOrc.test.osx
[ 94%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_vector_clock.cpp.o
[ 94%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_mac.cpp.o
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_mach_vm.cpp.o
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_platform_mac.cpp.o
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_platform_posix.cpp.o
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_libdispatch.cpp.o
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_new_delete.cpp.o
[ 95%] Building ASM object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_amd64.S.o
[ 95%] Building ASM object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_aarch64.S.o
[ 96%] Linking CXX static library ../darwin/liborc_rt_osx.a
[ 96%] Built target RTTsan_dynamic.osx
[ 96%] Generating ../darwin/libclang_rt.osx.a
[ 96%] Built target orc_rt_osx
[ 96%] Built target clang_rt.osx
[ 96%] Generating ../darwin/libclang_rt.cc_kext.a
[ 96%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan.cpp.o
[ 96%] Built target clang_rt.cc_kext
[ 97%] Linking CXX shared library ../darwin/libclang_rt.ubsan_osx_dynamic.dylib
[ 97%] Built target clang_rt.ubsan_osx_dynamic
[ 97%] Linking CXX shared library ../darwin/libclang_rt.asan_osx_dynamic.dylib
[ 97%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_allocator.cpp.o
[ 97%] Built target clang_rt.asan_osx_dynamic
[ 97%] Built target tsan
[ 97%] Built target cfi
[ 97%] Linking CXX shared library ../darwin/libclang_rt.ubsan_minimal_osx_dynamic.dylib
[ 97%] Built target clang_rt.ubsan_minimal_osx_dynamic
[ 97%] Linking CXX static library ../darwin/libclang_rt.ubsan_minimal_osx.a
[ 97%] Built target clang_rt.ubsan_minimal_osx
[ 97%] Linking CXX static library ../darwin/libclang_rt.asan_abi_osx.a
[ 97%] Built target clang_rt.asan_abi_osx
[ 97%] Built target profile
[ 97%] Linking CXX static library ../darwin/libclang_rt.xray-profiling_osx.a
[ 97%] Built target clang_rt.xray-profiling_osx
[ 97%] Linking CXX static library ../darwin/libclang_rt.xray_osx.a
[ 97%] Built target clang_rt.xray_osx
[ 97%] Linking CXX static library ../darwin/libclang_rt.xray-fdr_osx.a
[ 97%] Built target clang_rt.xray-fdr_osx
[ 97%] Linking CXX static library ../darwin/libclang_rt.xray-basic_osx.a
[ 97%] Built target clang_rt.xray-basic_osx
[ 97%] Linking CXX static library ../darwin/libclang_rt.fuzzer_interceptors_osx.a
warning: /home/runner/.mozbuild/osxcross/target/bin/arm64-apple-darwin23.4-libtool: archive library: ../darwin/libclang_rt.fuzzer_interceptors_osx.a the table of contents is empty (no object file members in the library define global symbols)
[ 97%] Built target clang_rt.fuzzer_interceptors_osx
[ 97%] Linking CXX static library ../darwin/libclang_rt.fuzzer_osx.a
[ 97%] Built target clang_rt.fuzzer_osx
[ 97%] Linking CXX static library ../darwin/libclang_rt.fuzzer_no_main_osx.a
[ 97%] Built target clang_rt.fuzzer_no_main_osx
[ 98%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_fuchsia.cpp.o
[ 98%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_interceptors.cpp.o
[ 98%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_linux.cpp.o
[ 98%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_mac.cpp.o
[ 98%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_malloc_mac.cpp.o
[ 98%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_posix.cpp.o
[ 98%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_preinit.cpp.o
[ 98%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_thread.cpp.o
[ 98%] Built target orc
[ 98%] Built target builtins
[ 98%] Built target ubsan
[ 98%] Built target asan
[ 98%] Built target ubsan-minimal
[ 98%] Built target asan_abi
[ 98%] Built target xray
[ 98%] Built target fuzzer
[100%] Linking CXX shared library ../darwin/libclang_rt.lsan_osx_dynamic.dylib
[100%] Built target clang_rt.lsan_osx_dynamic
[100%] Built target lsan
[100%] Built target compiler-rt



Installing compiler-rt headers and libraries to the following paths:
  /usr/lib/llvm-18/lib/clang/18/include
  /usr/lib/llvm-18/lib/clang/18/lib/darwin

mkdir: cannot create directory '/usr/lib/llvm-18/lib/clang/18/lib/darwin': Permission denied
+ '[' 5 -ge 5 ']'
+ return 1
Error: Process completed with exit code 1.

build (macos, arm64, ubuntu-24.04)

Setup macos toolchain

………

[ 93%] Built target RTfuzzer.osx
[ 97%] Linking CXX shared library ../darwin/libclang_rt.ubsan_osx_dynamic.dylib
[ 93%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_mutex.cpp.o
[ 93%] Linking CXX static library libRTOrc.test.osx.a
[ 93%] Built target RTOrc.test.osx
[ 94%] Linking CXX static library ../darwin/liborc_rt_osx.a
[ 97%] Built target clang_rt.ubsan_osx_dynamic
[ 97%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_mac.cpp.o
[ 94%] Built target orc_rt_osx
[ 94%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_proc.cpp.o
[ 94%] Generating ../darwin/libclang_rt.osx.a
[ 94%] Built target clang_rt.osx
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_report.cpp.o
[ 97%] Linking CXX shared library ../darwin/libclang_rt.asan_osx_dynamic.dylib
[ 97%] Built target clang_rt.asan_osx_dynamic
[ 97%] Built target tsan
[ 97%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_mach_vm.cpp.o
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_thread.cpp.o
[ 97%] Built target cfi
[ 98%] Linking CXX shared library ../darwin/libclang_rt.ubsan_minimal_osx_dynamic.dylib
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_platform_mac.cpp.o
[100%] Built target clang_rt.ubsan_minimal_osx_dynamic
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_platform_posix.cpp.o
[ 95%] Generating ../darwin/libclang_rt.cc_kext.a
[ 95%] Built target clang_rt.cc_kext
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_stack_trace.cpp.o
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_libdispatch.cpp.o
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_new_delete.cpp.o
[ 95%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan.cpp.o
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_suppressions.cpp.o
[ 95%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_allocator.cpp.o
[100%] Building ASM object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_amd64.S.o
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_symbolize.cpp.o
[100%] Linking CXX static library ../darwin/libclang_rt.ubsan_minimal_osx.a
[100%] Built target clang_rt.ubsan_minimal_osx
[100%] Linking CXX static library ../darwin/libclang_rt.asan_abi_osx.a
[100%] Built target clang_rt.asan_abi_osx
[100%] Building ASM object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_aarch64.S.o
[100%] Built target profile
[100%] Linking CXX static library ../darwin/libclang_rt.xray-profiling_osx.a
[100%] Built target clang_rt.xray-profiling_osx
[100%] Linking CXX static library ../darwin/libclang_rt.xray_osx.a
[100%] Built target RTTsan_dynamic.osx
[100%] Built target clang_rt.xray_osx
[100%] Linking CXX static library ../darwin/libclang_rt.xray-fdr_osx.a
[100%] Linking CXX static library ../darwin/libclang_rt.xray-basic_osx.a
[100%] Built target clang_rt.xray-fdr_osx
[100%] Built target clang_rt.xray-basic_osx
[100%] Linking CXX static library ../darwin/libclang_rt.fuzzer_interceptors_osx.a
warning: /home/runner/.mozbuild/osxcross/target/bin/arm64-apple-darwin23.4-libtool: archive library: ../darwin/libclang_rt.fuzzer_interceptors_osx.a the table of contents is empty (no object file members in the library define global symbols)
[100%] Linking CXX static library ../darwin/libclang_rt.fuzzer_osx.a
[100%] Built target clang_rt.fuzzer_interceptors_osx
[100%] Linking CXX static library ../darwin/libclang_rt.fuzzer_no_main_osx.a
[100%] Built target clang_rt.fuzzer_osx
[100%] Built target orc
[100%] Built target clang_rt.fuzzer_no_main_osx
[100%] Built target builtins
[100%] Built target lsan
[100%] Built target ubsan
[100%] Built target asan
[100%] Built target ubsan-minimal
[100%] Built target asan_abi
[100%] Built target xray
[100%] Built target fuzzer
[100%] Built target compiler-rt
[ 95%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_sync.cpp.o
[ 96%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_fuchsia.cpp.o
[ 96%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_interceptors.cpp.o
[ 96%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_vector_clock.cpp.o
[ 96%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_linux.cpp.o
[ 96%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_mac.cpp.o
[ 96%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_mac.cpp.o
[ 96%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_malloc_mac.cpp.o
[ 96%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_posix.cpp.o
[ 96%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_preinit.cpp.o
[ 96%] Building CXX object lib/lsan/CMakeFiles/clang_rt.lsan_osx_dynamic.dir/lsan_thread.cpp.o
[ 97%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_mach_vm.cpp.o
[ 98%] Linking CXX shared library ../darwin/libclang_rt.lsan_osx_dynamic.dylib
[ 98%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_platform_mac.cpp.o
[ 98%] Built target clang_rt.lsan_osx_dynamic
[100%] Linking CXX shared library ../darwin/libclang_rt.ubsan_osx_dynamic.dylib
[100%] Built target clang_rt.ubsan_osx_dynamic
[100%] Linking CXX shared library ../darwin/libclang_rt.asan_osx_dynamic.dylib
[100%] Built target clang_rt.asan_osx_dynamic
[100%] Built target tsan
[100%] Built target cfi
[100%] Linking CXX shared library ../darwin/libclang_rt.ubsan_minimal_osx_dynamic.dylib
[100%] Built target clang_rt.ubsan_minimal_osx_dynamic
[100%] Linking CXX static library ../darwin/libclang_rt.ubsan_minimal_osx.a
[100%] Built target clang_rt.ubsan_minimal_osx
[100%] Linking CXX static library ../darwin/libclang_rt.asan_abi_osx.a
[100%] Built target clang_rt.asan_abi_osx
[100%] Built target profile
[100%] Linking CXX static library ../darwin/libclang_rt.xray-profiling_osx.a
[100%] Built target clang_rt.xray-profiling_osx
[100%] Linking CXX static library ../darwin/libclang_rt.xray_osx.a
[100%] Built target clang_rt.xray_osx
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_platform_posix.cpp.o
[100%] Linking CXX static library ../darwin/libclang_rt.xray-fdr_osx.a
[100%] Built target clang_rt.xray-fdr_osx
[100%] Linking CXX static library ../darwin/libclang_rt.xray-basic_osx.a
[100%] Built target clang_rt.xray-basic_osx
[100%] Linking CXX static library ../darwin/libclang_rt.fuzzer_interceptors_osx.a
warning: /home/runner/.mozbuild/osxcross/target/bin/arm64-apple-darwin23.4-libtool: archive library: ../darwin/libclang_rt.fuzzer_interceptors_osx.a the table of contents is empty (no object file members in the library define global symbols)
[100%] Built target clang_rt.fuzzer_interceptors_osx
[100%] Linking CXX static library ../darwin/libclang_rt.fuzzer_osx.a
[100%] Built target clang_rt.fuzzer_osx
[100%] Linking CXX static library ../darwin/libclang_rt.fuzzer_no_main_osx.a
[100%] Built target clang_rt.fuzzer_no_main_osx
[100%] Built target orc
[100%] Built target builtins
[100%] Built target lsan
[100%] Built target ubsan
[100%] Built target asan
[100%] Built target ubsan-minimal
[100%] Built target asan_abi
[100%] Built target xray
[100%] Built target fuzzer
[100%] Built target compiler-rt
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_interceptors_libdispatch.cpp.o
[100%] Building CXX object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_new_delete.cpp.o
[100%] Building ASM object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_amd64.S.o
[100%] Building ASM object lib/tsan/rtl/CMakeFiles/RTTsan_dynamic.osx.dir/tsan_rtl_aarch64.S.o
[100%] Built target RTTsan_dynamic.osx



Installing compiler-rt headers and libraries to the following paths:
  /usr/lib/llvm-18/lib/clang/18/include
  /usr/lib/llvm-18/lib/clang/18/lib/darwin

mkdir: cannot create directory '/usr/lib/llvm-18/lib/clang/18/lib/darwin': Permission denied
+ '[' 5 -ge 5 ']'
+ return 1
Error: Process completed with exit code 1.