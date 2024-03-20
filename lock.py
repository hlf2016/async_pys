import asyncio
import time

#  注意，acquire()是一个协程，需按协程的方式调用。Lock对象还实现了上下文管理器，可以使用with语句。


async def coro1(lock):
    print('coro1 start')
    async with lock:
        print('coro1 acquired lock')
        await asyncio.sleep(2)
    print('coro1 end')


async def coro2(lock):
    print('coro2 start')
    # await lock 与 lock.acquire() 效果一样
    await lock.acquire()
    print('coro2 acquired lock')
    await asyncio.sleep(5)
    lock.release()
    print('coro2 end')


async def main():
    lock = asyncio.Lock()
    await asyncio.gather(coro1(lock), coro2(lock))

if __name__ == '__main__':
    lock = asyncio.Lock()
    asyncio.run(main())
