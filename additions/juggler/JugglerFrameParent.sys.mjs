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

    // Only interested in main frames for now.
    if (this.browsingContext.parent)
      return;

    this._target = TargetRegistry.instance()?.targetForBrowserId(this.browsingContext.browserId);
    if (!this._target)
      return;

    this.actorName = `browser::page[${this._target.id()}]/${this.browsingContext.browserId}/${this.browsingContext.id}/${this._target.nextActorSequenceNumber()}`;
    this._target.setActor(this);
  }

  didDestroy() {
    if (!this._target)
      return;
    this._target.removeActor(this);
  }
}
