from concurrent.futures import Future, ThreadPoolExecutor
from threading import Event

from camoufox import ip


def test_rotating_proxy_is_not_cached(monkeypatch):
    class Pool:
        calls = 0
        def submit(self, fn, url):
            self.calls += 1
            future = Future()
            future.set_result(f'192.0.2.{self.calls}')
            return future

    pool = Pool()
    monkeypatch.setattr(ip, '_IP_EXECUTOR', pool)
    a = ip.public_ip('http://rotating-proxy.invalid:8080')
    b = ip.public_ip('http://rotating-proxy.invalid:8080')
    assert a != b
    assert pool.calls == 12


def test_fast_provider_returns_while_another_is_still_running(monkeypatch):
    slow_started, release = Event(), Event()
    class Response:
        text = '192.0.2.8'
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def raise_for_status(self): pass

    def request(url, **kwargs):
        if 'ipify' in url:
            slow_started.set()
            release.wait(3)
        else:
            assert slow_started.wait(1)
        return Response()

    pool = ThreadPoolExecutor(max_workers=2)
    monkeypatch.setattr(ip, '_IP_EXECUTOR', pool)
    monkeypatch.setattr(ip.requests, 'get', request)
    try:
        assert ip.public_ip() == '192.0.2.8'
        assert not release.is_set()
    finally:
        release.set()
        pool.shutdown()
