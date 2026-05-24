/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// ESM wrapper around content/Runtime.js.
//
// Runtime.js itself must remain a classic script because the JS Debugger
// workers spawned by content/WorkerMain.js loadSubScript it into their
// global. Chrome-process ESM consumers (FrameTree, …) go through this
// wrapper which sandboxes the classic file and re-exports the class.

const sandbox = { ChromeUtils, Components };
Services.scriptloader.loadSubScript(
  'chrome://juggler/content/content/Runtime.js',
  sandbox
);

export const Runtime = sandbox.Runtime;
