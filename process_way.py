import socket
from concurrent import futures
import time
import multiprocessing

# 多进程形式请求百度首页10次


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


def process_way():
    workers = 10
    with futures.ProcessPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for i in range(10)}
    return len([fut.result() for fut in futs])


def main():
    start = time.time()
    # 这个问题通常出现在Mac OS和Linux系统上，因为它们在使用 multiprocessing 库时，Mac OS默认使用 "spawn" 启动方法，而Linux默认使用 "fork"。当使用 "spawn" 或 "forkserver" 方法启动子进程时，主模块会被重新导入，在该情况下，所有在模块级别的代码都会运行，但是只有在 `if __name__ == '__main__':` 保护块内的代码才会在主进程中运行。如果在模块级别直接尝试创建进程，可能会出现这个错误，因为子进程可能会尝试创建它们自己的子进程。为了避免这个问题，你应该总是在 `if __name__ == '__main__':` 保护块内创建进程。
    # linux 下不会出现这个问题
    print(process_way())
    print(time.time() - start)


if __name__ == '__main__':
    import time
    # 获取多进程的进程启动方式
    # 在MacOS或者Linux操作系统上，在Python 3.8及以后的版本中，默认的开启进程的方式从原本的fork变更为spawn。为了确认当前Python环境使用的是spawn还是fork，您可以检查multiprocessing模块的get_start_method()方法返回的值。
    # 使用fork方法在Multiprocessing中会更快，因为它不需要将程序状态全部序列化到子进程，但是fork可能会在某些特殊情况下与线程以及某些库产生冲突。在Python 3.8及以后版本中，默认改为了spawn，因为它在跨平台上更加安全和可靠，不过它的初始化开销可能会更大一些。
    # 当使用 spawn 方法在Mac上进行多进程编程时，确实可能观察到进程启动速度较慢，以及程序执行效率相对于 fork 并不会有明显提升。这是由于 spawn 方法的工作方式导致的。spawn 启动方法会新建一个Python解释器进程，并且通过序列化父进程中的信息来初始化这个新的进程。这个过程相对耗时，因为它需要将需要的资源和信息从父进程复制到子进程。在CPU密集型的任务时，这个初始化过程的开销会在之后的计算中得到弥补，然而对于简单或者执行时间很短的任务而言，进程的创建过程的开销可能会超过多进程带来的收益。相反，fork 方法会直接复制父进程和其全部资源，创建子进程时没有序列化的开销，所以它的启动速度要快得多。但 fork 方法带来的问题是，所有父进程的状态都被完整地复制到了子进程，包括文件描述符和锁等资源，这可能会导致难以预料的竞争条件和其他问题。如果在使用 spawn 方法时发现性能提升并不明显，可能需要调整程序的设计，比如：减少初始化开销： 在进程间尽量共享只读数据，而不是在每个子进程中重复创建相同的数据。增大工作量： 将更多的工作分配给每个子进程，这样子进程初始化的相对开销就会减小。减少上下文切换： 减少进程数量，合理配置进程池大小，避免过多的上下文切换。使用并发而非并行： 对于IO密集型任务，考虑使用线程（threading）或异步(asyncio)编程，这些不会受进程启动方法影响，并可能获得更好的性能提升。通过以上方法，通常可以在使用 spawn 方法时，改善程序的整体性能。在设计多进程程序时还是需要关注不同类型任务（CPU密集型或IO密集型）以及各种启动方式的最佳适用场景。
    print(multiprocessing.get_start_method())
    main()
