import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

# yield

selector = DefaultSelector()
stopped = False
url_todos = {'/'}


class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        print('set result', self._callbacks)
        for fn in self._callbacks:
            fn(self)


class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('www.baidu.com', 80))
        except BlockingIOError:
            pass
        f = Future()

        def on_connected():
            print('on_connected')
            f.set_result(None)
        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        print('第一次 yield 前')
        yield f
        print('第一次 yield 后')
        selector.unregister(sock.fileno())
        get = 'GET {0} HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'.format(
            self.url)
        sock.send(get.encode('ascii'))

        global stopped

        while True:
            f = Future()

            def on_readable():
                print('on_readable')
                f.set_result(sock.recv(4096))

            selector.register(sock.fileno(), EVENT_READ, on_readable)
            print('第二次 yield 前')
            chunk = yield f
            print('第二次 yield 后')
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                url_todos.remove(self.url)
                if not url_todos:
                    stopped = True
                break


class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        print('执行一次step')
        try:
            # send会进入到coro执行，即fetch，直到下次yield
            # next_future为yield返回的对象
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)


def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            print(event_key)
            callback()


if __name__ == '__main__':
    import time
    startTime = time.time()
    for url in url_todos:
        crawler = Crawler(url)
        Task(crawler.fetch())
    loop()
    print(time.time() - startTime)  # 0.15s
