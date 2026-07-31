/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const {Helper} = ChromeUtils.importESModule('chrome://juggler/content/Helper.js');
const {FrameTree} = ChromeUtils.importESModule('chrome://juggler/content/content/FrameTree.js');
const {SimpleChannel} = ChromeUtils.importESModule('chrome://juggler/content/SimpleChannel.sys.mjs');
const {PageAgent} = ChromeUtils.importESModule('chrome://juggler/content/content/PageAgent.js');

const helper = new Helper();

export function initialize(browsingContext, docShell) {
  const data = { channel: undefined, pageAgent: undefined, frameTree: undefined, failedToOverrideTimezone: false };

  const applySetting = {
    geolocation: (geolocation) => {
      if (geolocation) {
        // Both docShell.setGeolocationOverride and this one work on 152 (the
        // old path was verified applying correctly), but the BrowsingContext
        // API is the one documented in dom/chrome-webidl/BrowsingContext.webidl
        // and the one upstream moved to, so follow it rather than depend on
        // the older docshell entry point staying around.
        browsingContext.setGeolocationServiceOverride({
          coords: {
            latitude: geolocation.latitude,
            longitude: geolocation.longitude,
            accuracy: geolocation.accuracy,
            altitude: NaN,
            altitudeAccuracy: NaN,
            heading: NaN,
            speed: NaN,
          },
          timestamp: Date.now() + 24 * 60 * 60 * 1000,  // Make sure it does not expire for a day.
        });
      } else {
        browsingContext.setGeolocationServiceOverride();
      }
    },

    bypassCSP: (bypassCSP) => {
      docShell.bypassCSPEnabled = bypassCSP;
    },

    timezoneId: (timezoneId) => {
      data.failedToOverrideTimezone = !docShell.overrideTimezone(timezoneId);
    },

    locale: (locale) => {
      // Camoufox: also propagate to BrowsingContext so the LanguageOverride
      // synced field reaches Navigator.language consumers
      // (dom/base/Navigator.cpp reads bc->Top()->GetLanguageOverride()).
      // docShell.languageOverride alone only updates ICU + the JS default
      // locale, so new_context(locale=...) never moved navigator.language.
      try {
        if (browsingContext && browsingContext.top) {
          browsingContext.top.languageOverride = locale || "";
        }
      } catch (e) { /* fall through */ }
      docShell.languageOverride = locale;
    },

    javaScriptDisabled: (javaScriptDisabled) => {
      data.frameTree.setJavaScriptDisabled(javaScriptDisabled);
    },
  };

  const contextCrossProcessCookie = Services.cpmm.sharedData.get('juggler:context-cookie-' + browsingContext.originAttributes.userContextId) || { initScripts: [], bindings: [], settings: {} };
  const pageCrossProcessCookie = Services.cpmm.sharedData.get('juggler:page-cookie-' + browsingContext.browserId) || { initScripts: [], bindings: [], interceptFileChooserDialog: false };

  // Enforce focused state for all top level documents.
  docShell.overrideHasFocus = true;
  docShell.forceActiveState = true;
  docShell.disallowBFCache = true;
  data.frameTree = new FrameTree(browsingContext);
  for (const [name, value] of Object.entries(contextCrossProcessCookie.settings)) {
    if (value !== undefined)
      applySetting[name](value);
  }
  for (const { worldName, name, script } of [...contextCrossProcessCookie.bindings, ...pageCrossProcessCookie.bindings])
    data.frameTree.addBinding(worldName, name, script);
  data.frameTree.setInitScripts([...contextCrossProcessCookie.initScripts, ...pageCrossProcessCookie.initScripts]);
  data.channel = new SimpleChannel('', 'process-' + Services.appinfo.processID);
  data.pageAgent = new PageAgent(data.channel, data.frameTree);
  docShell.fileInputInterceptionEnabled = !!pageCrossProcessCookie.interceptFileChooserDialog;

  data.channel.register('', {
    setInitScripts(scripts) {
      data.frameTree.setInitScripts(scripts);
    },

    addBinding({worldName, name, script}) {
      data.frameTree.addBinding(worldName, name, script);
    },

    applyContextSetting({name, value}) {
      applySetting[name](value);
    },

    setInterceptFileChooserDialog(enabled) {
      docShell.fileInputInterceptionEnabled = !!enabled;
    },

    ensurePermissions() {
      // noop, just a rountrip.
    },

    hasFailedToOverrideTimezone() {
      return data.failedToOverrideTimezone;
    },

    async awaitViewportDimensions({width, height}) {
      await new Promise(resolve => {
        const listeners = [];
        const check = () => {
          helper.removeListeners(listeners);
          if (docShell.domWindow.innerWidth === width && docShell.domWindow.innerHeight === height) {
            resolve();
            return;
          }
          // Note: "domWindow" listeners are often removed upon navigation, as specced.
          // To survive viewport changes across navigations, re-install listeners upon commit.
          // The old code bound one resize listener to the window captured at call
          // time, so a navigation in between dropped it and the promise never
          // settled -- set_viewport_size() then hung for the whole timeout.
          listeners.push(helper.addEventListener(docShell.domWindow, 'resize', check));
          listeners.push(helper.addEventListener(data.frameTree, 'navigationcommitted', check));
        };
        check();
      });
    },

    dispose() {
    },
  });

  return data;
}

