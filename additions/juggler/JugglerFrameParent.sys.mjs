/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const { TargetRegistry } = ChromeUtils.importESModule('chrome://juggler/content/TargetRegistry.js');
const { Helper } = ChromeUtils.importESModule('chrome://juggler/content/Helper.js');

const helper = new Helper();

export class JugglerFrameParent extends JSWindowActorParent {
  constructor() {
    super();
  }

  receiveMessage() { }

  async actorCreated() {
    // Actors are registered per the WindowGlobalParent / WindowGlobalChild pair. We are only
    // interested in those WindowGlobalParent actors that are matching current browsingContext
    // window global.
    if (!this.manager?.isCurrentGlobal)
      return;

    // Firefox 152+: the actor may be created BEFORE the chrome-side PageTarget
    // exists (notably for window.open popups, where the content WindowGlobal is
    // created before the `TabOpen` event fires). Delegate to the registry, which
    // tracks the actor and binds it whenever the target appears — in either
    // order. The previous implementation looked up the target here and bailed
    // with no retry when it was missing, leaving the page channel permanently
    // unbound (Page.ready never sent -> newPage hung / no `popup` event).
    TargetRegistry.instance()?.onActorCreated(this);
  }

  didDestroy() {
    TargetRegistry.instance()?.onActorDestroyed(this);
  }
}
