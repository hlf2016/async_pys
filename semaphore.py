import asyncio
import random

# Semaphore 信号量，原本是铁路交通系统中的一个术语，后被荷兰计算机科学家Dijkstra引入计算机科学领域。用于控制仅支持有限个用户同时操作的共享资源，在计算机系统中有着广泛的应用。
# 信号量对象的内部会维护一个计数值，取值范围是任意正整数，默认为1。当一个协程中对信号量进行一次acquire()，其计数值就减1，release()一次则加1。当计数值减至0时，后来的协程将阻塞在acquire()操作上，直到有其他协程release()该信号量。
# 当信号量对象内的计数值初始化为大于等于2的正整数，称其为一般信号量或计数信号量；计数器初始化为1时，则其变动范围只有{0,1}两种可能，又被称为二进制信号量，二进制信号量又被称为互斥锁。虽然asyncio中的Lock和Semaphore分别由两个不同的类实现，但其源代码十分相似。从原理上我们已经知道，互斥锁是信号量的一个特例。


async def worker(name, sema):
    async with sema:
        print(f'worker {name} acquired semaphore')
        await asyncio.sleep(random.randint(1, 5))
        print(f'worker {name} released semaphore')


async def main():
    sema = asyncio.Semaphore(3)
    await asyncio.wait([asyncio.create_task(worker(name, sema)) for name in 'abcde'])

if __name__ == '__main__':
    asyncio.run(main())
