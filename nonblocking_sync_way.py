import socket
import time


def nonblocking_way():
    sock = socket.socket()
    # 设置非阻塞
    sock.setblocking(False)
    try:
        sock.connect(('www.baidu.com', 80))
    except BlockingIOError:
        # 非阻塞连接过程中会抛出异常
        pass
    request = 'GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'
    data = request.encode('ascii')
    # 不知道 socket 何时连接成功，所以不断尝试
    while True:
        try:
            sock.send(data)
            # 知道 send 不抛出异常 表示发送成功 直接 break
            break
        except OSError:
            pass
    response = b''
    while True:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            break
        except OSError:
            pass
    return response


def sync_way():
    res = []
    for i in range(10):
        res.append(nonblocking_way())
    return len(res)


startTime = time.time()
print(sync_way())
print(time.time() - startTime)  # 0.27s
