import socket
from concurrent import futures
import time

# 多线程形式请求百度首页10次


def blocking_way():
    sock = socket.socket()
    # blocking
    sock.connect(('www.baidu.com', 80))
    request = 'GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        # blocking
        chunk = sock.recv(4096)
    return response


def thread_way():
    workers = 10
    with futures.ThreadPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for i in range(10)}
    return len([fut.result() for fut in futs])


startTime = time.time()
print(thread_way())
print(time.time() - startTime)  # 0.05s
