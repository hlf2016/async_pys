import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

# 基于 epoll 实现 异步非阻塞 的爬虫

selector = DefaultSelector()
stopped = False
url_todos = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}

# 导入了selectors模块，并创建了一个DefaultSelector 实例。Python标准库提供的selectors模块是对底层select/poll/epoll/kqueue的封装。DefaultSelector类会根据 OS 环境自动选择最佳的模块，那在 Linux 2.5.44 及更新的版本上都是epoll了。


class Crawler:
    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('www.baidu.com', 80))
        except BlockingIOError:
            pass
        # self.connected 是连接之后触发的回调函数
        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        # 连接成功之后，取消注册事件
        selector.unregister(key.fd)
        request = 'GET {0} HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'.format(
            self.url)
        self.sock.send(request.encode('ascii'))
        # self.read_response 是读取响应的回调函数
        selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped
        # 如果响应大于4k，需要多次读取
        chunk = self.sock.recv(4096)
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)
            url_todos.remove(self.url)
            if not url_todos:
                stopped = True
        return self.response
# 上面的 Crawler 分别注册了socket可写事件(EVENT_WRITE)和可读事件(EVENT_READ)发生后应该采取的回调函数。 虽然代码结构清晰了，阻塞操作也交给OS去等待和通知了，但是，我们要抓取10个不同页面，就得创建10个Crawler实例，就有20个事件将要发生，那如何从selector里获取当前正发生的事件，并且得到对应的回调函数去执行呢？


def loop():
    while not stopped:
        # 阻塞，直到至少一个事件发生
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            res = callback(event_key, event_mask)
            print(res)


if __name__ == '__main__':
    import time
    startTime = time.time()
    for url in url_todos:
        crawler = Crawler(url)
        crawler.fetch()
    loop()
    print(time.time() - startTime)  # 0.07s
