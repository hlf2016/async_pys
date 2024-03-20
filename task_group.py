import asyncio


async def my_task(i):
    print(f'Task {i} is start')
    await asyncio.sleep(i)
    print(f'Task {i} is done')
    return i


async def main():
    tasks = []  # 用于存储Task对象的列表
    results = []  # 用于存储所有任务的结果

    async with asyncio.TaskGroup() as tg:
        for i in range(3):
            task = tg.create_task(my_task(i))
            tasks.append(task)

    for task in tasks:
        results.append(task.result())  # 收集每个Task的结果

    print(results)  # 展示所有结果


if __name__ == '__main__':
    asyncio.run(main())
