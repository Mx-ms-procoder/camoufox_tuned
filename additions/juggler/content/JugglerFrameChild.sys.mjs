/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

const { Helper } = ChromeUtils.importESModule('chrome://juggler/content/Helper.js');
const { initialize } = ChromeUtils.importESModule('chrome://juggler/content/content/main.js');

const helper = new Helper();

let sameProcessInstanceNumber = 0;

const topBrowingContextToAgents = new Map();

export class JugglerFrameChild extends JSWindowActorChild {
  constructor() {
    super();

    this._eventListeners = [];
  }

  handleEvent(aEvent) {
    const agents = this._agents();
    if (!agents)
      return;
    if (aEvent.type === 'DOMWillOpenModalDialog') {
      agents.channel.pause();
      return;
    }
    if (aEvent.type === 'DOMModalDialogClosed') {
      agents.channel.resumeSoon();
      return;
    }
    if (aEvent.target === this.document) {
      agents.pageAgent.onWindowEvent(aEvent);
      agents.frameTree.onWindowEvent(aEvent);
    }
  }

  _agents() {
    return topBrowingContextToAgents.get(this.browsingContext.top);
  }

  actorCreated() {
    this.actorName = `content::${this.browsingContext.browserId}/${this.browsingContext.id}/${++sameProcessInstanceNumber}`;

    this._eventListeners.push(helper.addEventListener(this.contentWindow, 'load', event => {
      this._agents()?.pageAgent.onWindowEvent(event);
    }));

    if (this.document.documentURI.startsWith('moz-extension://'))
      return;

    // Child frame events will be forwarded to related top-level agents.
    if (this.browsingContext.parent)
      return;

    let agents = topBrowingContextToAgents.get(this.browsingContext);
    if (!agents) {
      agents = initialize(this.browsingContext, this.docShell);
      topBrowingContextToAgents.set(this.browsingContext, agents);
    }
    agents.channel.bindToActor(this);
    agents.actor = this;
  }

  didDestroy() {
    helper.removeListeners(this._eventListeners);

    if (this.browsingContext.parent)
      return;

    const agents = topBrowingContextToAgents.get(this.browsingContext);
    // The agents are already re-bound to a new actor.
    if (agents?.actor !== this)
      return;

    topBrowingContextToAgents.delete(this.browsingContext);

    agents.channel.resetTransport();
    agents.pageAgent.dispose();
    agents.frameTree.dispose();
  }

  receiveMessage() { }
}
