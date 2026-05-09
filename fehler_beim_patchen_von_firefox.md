build (Linux, x86_64), build (Linux, arm64), build (Linux, i686)
build
Run python3 ./multibuild.py --target linux --arch x86_64
python3 scripts/patch.py 135.0.1 beta.24 --mozconfig-only
~/.cargo/bin/rustup target add "aarch64-unknown-linux-gnu"
info: downloading component rust-std
~/.cargo/bin/rustup target add "i686-unknown-linux-gnu"
info: downloading component rust-std
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: x86_64-pc-linux-gnu
-> Updating mozconfig, target is x86_64-pc-linux-gnu
Complete!
rm -rf camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox-bin \
	camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox
make[1]: Entering directory '/home/runner/work/firefox/firefox'
python3 scripts/patch.py 135.0.1 beta.24
~/.cargo/bin/rustup target add "aarch64-unknown-linux-gnu"
info: component rust-std for target aarch64-unknown-linux-gnu is up to date
~/.cargo/bin/rustup target add "i686-unknown-linux-gnu"
info: component rust-std for target i686-unknown-linux-gnu is up to date
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: x86_64-pc-linux-gnu
-> Updating mozconfig, target is x86_64-pc-linux-gnu

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
Hunk #1 FAILED at 1641.
Hunk #2 FAILED at 51.
Hunk #3 FAILED at 193.
3 out of 3 hunks FAILED -- saving rejects to file browser/components/asrouter/content/asrouter-admin.bundle.js.rej
fatal error: command 'patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch' failed
make[1]: *** [Makefile:102: dir] Error 1
make[1]: Leaving directory '/home/runner/work/firefox/firefox'
make: *** [Makefile:131: build] Error 2

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.

build (windows, x86_64), build (windows, i686)
build

Run python3 ./multibuild.py --target windows --arch x86_64
python3 scripts/patch.py 135.0.1 beta.24 --mozconfig-only
~/.cargo/bin/rustup target add "x86_64-pc-windows-msvc"
info: downloading component rust-std
~/.cargo/bin/rustup target add "aarch64-pc-windows-msvc"
info: downloading component rust-std
~/.cargo/bin/rustup target add "i686-pc-windows-msvc"
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
~/.cargo/bin/rustup target add "x86_64-pc-windows-msvc"
info: component rust-std for target x86_64-pc-windows-msvc is up to date
~/.cargo/bin/rustup target add "aarch64-pc-windows-msvc"
info: component rust-std for target aarch64-pc-windows-msvc is up to date
~/.cargo/bin/rustup target add "i686-pc-windows-msvc"
info: component rust-std for target i686-pc-windows-msvc is up to date
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
Hunk #1 FAILED at 1641.
Hunk #2 FAILED at 51.
Hunk #3 FAILED at 193.
3 out of 3 hunks FAILED -- saving rejects to file browser/components/asrouter/content/asrouter-admin.bundle.js.rej
fatal error: command 'patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch' failed
make[1]: *** [Makefile:102: dir] Error 1
make[1]: Leaving directory '/home/runner/work/firefox/firefox'
make: *** [Makefile:131: build] Error 2

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.

Run python3 ./multibuild.py --target macos --arch x86_64
python3 scripts/patch.py 135.0.1 beta.24 --mozconfig-only
~/.cargo/bin/rustup target add "x86_64-apple-darwin"
info: downloading component rust-std
~/.cargo/bin/rustup target add "aarch64-apple-darwin"
info: downloading component rust-std
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: x86_64-apple-darwin
-> Updating mozconfig, target is x86_64-apple-darwin
Complete!
rm -rf camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox-bin \
	camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox
make[1]: Entering directory '/home/runner/work/firefox/firefox'
python3 scripts/patch.py 135.0.1 beta.24
~/.cargo/bin/rustup target add "x86_64-apple-darwin"
info: component rust-std for target x86_64-apple-darwin is up to date
~/.cargo/bin/rustup target add "aarch64-apple-darwin"
info: component rust-std for target aarch64-apple-darwin is up to date
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: x86_64-apple-darwin
-> Updating mozconfig, target is x86_64-apple-darwin

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
Hunk #1 FAILED at 1641.
Hunk #2 FAILED at 51.
Hunk #3 FAILED at 193.
3 out of 3 hunks FAILED -- saving rejects to file browser/components/asrouter/content/asrouter-admin.bundle.js.rej
fatal error: command 'patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch' failed
make[1]: *** [Makefile:102: dir] Error 1
make[1]: Leaving directory '/home/runner/work/firefox/firefox'
make: *** [Makefile:131: build] Error 2

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.