const assert = require('node:assert/strict');
const { test } = require('node:test');
const { EventEmitter } = require('node:events');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '../additions/juggler/Helper.js'), 'utf8');
const sandbox = {
  setTimeout, clearTimeout, Date,
  Cc: new Proxy({}, { get: () => ({ getService: () => ({}) }) }),
  Ci: {},
  ChromeUtils: { importESModule: () => ({ setTimeout, clearTimeout }) },
};
vm.createContext(sandbox);
vm.runInContext(source.replaceAll('export class ', 'class ') +
  '\nglobalThis.TestWatcher = EventWatcher; globalThis.TestHelper = Helper;', sandbox);

test('missing ack expires and releases the pending waiter', async () => {
  const sink = new EventEmitter(), pending = new Set();
  const watcher = new sandbox.TestWatcher(sink, ['ack'], pending);
  await assert.rejects(watcher.ensureEvent('ack', undefined, 15), /Timed out/);
  assert.equal(watcher._pendingPromises.length, 0);
  watcher.dispose();
  assert.equal(sink.listenerCount('ack'), 0);
  assert.equal(pending.size, 0);
});

test('dispose rejects existing and future waits', async () => {
  const watcher = new sandbox.TestWatcher(new EventEmitter(), ['ack']);
  const waiting = watcher.ensureEvent('ack');
  watcher.dispose();
  await assert.rejects(waiting, /disposed/);
  await assert.rejects(watcher.ensureEvent('ack'), /disposed/);
});

test('unrelated acknowledgements do not satisfy an event ID', async () => {
  const sink = new EventEmitter();
  const watcher = new sandbox.TestWatcher(sink, ['ack']);
  const waiting = watcher.ensureEvent('ack', event => event.id === 2, 1000);
  sink.emit('ack', 'ack', { id: 1 });
  sink.emit('ack', 'ack', { id: 2 });
  assert.equal((await waiting).id, 2);
  watcher.dispose();
});

test('tab-switch timeout removes its DOM listener', async () => {
  const target = new EventTarget();
  let added = 0, removed = 0;
  const receiver = {
    addEventListener: (...args) => { added++; target.addEventListener(...args); },
    removeEventListener: (...args) => { removed++; target.removeEventListener(...args); },
  };
  await assert.rejects(new sandbox.TestHelper().awaitEvent(receiver, 'TabSwitchDone', 15), /Timed out/);
  assert.equal(added, removed);
});

test('Playwright-wrapped and bare main-world init scripts are recognized', () => {
  const frame = fs.readFileSync(path.join(__dirname, '../additions/juggler/content/FrameTree.js'), 'utf8');
  const begin = frame.indexOf('const INIT_SCRIPT_WRAPPER');
  const end = frame.indexOf('\n}', begin) + 2;
  vm.runInContext(frame.slice(begin, end), sandbox);
  assert.equal(sandbox.mainWorldInitScript('mw:window.ready = 1;'), 'window.ready = 1;');
  assert.equal(sandbox.mainWorldInitScript('(() => {\n mw:window.ready = 1;\n})();'), 'window.ready = 1;\n');
  assert.equal(sandbox.mainWorldInitScript('window.ready = 1;'), null);
});
