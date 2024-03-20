import asyncio

# Condition是条件变量的实现，它可以让一个或多个协程一直等待某个条件达成以后再继续运行。Conditon和Event很像，都是通过一个信号让别的协程继续运行下去，但有不同点：
# Event是一次性通知所有阻塞在该事件上的协程，而Condition可以分别通知其中的一个或多个，而未被通知的继续等待。
# Condition底层实现使用了Lock对象，而Event没有。


async def task_should_wait(cond, n):
    async with cond:
        print(f'task {n} is waiting. [BLOCKING]')
        await cond.wait()
        print('n notify', n)
        print(f'task {n} received the notice. [RUNNING]')
    print(f'task {n} is done. [END]')


async def notify_the_tasks(cond):
    await asyncio.sleep(0.1)
    # 在你的代码中，`notify_the_tasks` 函数中的 `cond.notify(i)` 会按照任务等待的顺序来通知任务。这是因为 asyncio 的 Condition 对象使用 FIFO（先进先出）队列来管理等待的任务。所以，最早等待的任务会被最早通知。
    # 这就意味着，如果你的 `main` 函数按照 `i` 的顺序创建任务，那么 `notify_the_tasks` 函数的前两次通知会按照任务创建的顺序来通知任务。
    # 那么 `notify_the_tasks` 函数的前两次通知会通知任务 0 和任务 1，因为这两个任务是最早创建的。
    for i in range(1, 3):
        async with cond:
            print(f'notify {i} task. [NOTIFY]')
            cond.notify(i)
        await asyncio.sleep(0.1)
    async with cond:
        print('Remaining tasks will be notified. [NOTIFY]')
        cond.notify_all()


async def main():
    cond = asyncio.Condition()
    tasks = [asyncio.create_task(task_should_wait(cond, i)) for i in range(5)]
    asyncio.create_task(notify_the_tasks(cond))
    await asyncio.wait(tasks)

if __name__ == '__main__':
    asyncio.run(main())
