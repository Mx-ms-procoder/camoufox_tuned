/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// ESM wrapper around SimpleChannel.js.
//
// SimpleChannel.js itself must remain a classic script because the JS
// Debugger workers spawned by content/WorkerMain.js loadSubScript it into
// their own global, and `export` syntax would be a parse error there.
// All chrome-process consumers should import the class from this module.

const sandbox = { ChromeUtils };
Services.scriptloader.loadSubScript(
  'chrome://juggler/content/SimpleChannel.js',
  sandbox
);

export const SimpleChannel = sandbox.SimpleChannel;
