import socket
import time

# 同步阻塞方式请求百度首页10次


def blocking_way():
    sock = socket.socket()
    # 阻塞
    sock.connect(('www.baidu.com', 80))
    request = 'GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        # 阻塞
        chunk = sock.recv(4096)
    return response


def sync_way():
    res = []
    for i in range(10):
        res.append(blocking_way())
    return len(res)


startTime = time.time()
print(sync_way())
endTime = time.time()
print(endTime - startTime)  # 0.45s
