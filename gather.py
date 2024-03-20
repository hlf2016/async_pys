import asyncio


async def my_task(i):
    print(f'Task {i} is start')
    await asyncio.sleep(i)
    print(f'Task {i} is done')
    return i


async def main():
    tasks = [my_task(i) for i in range(3)]
    # list 形式拿到所有的结果
    res = await asyncio.gather(*tasks)
    print(res)

if __name__ == '__main__':
    asyncio.run(main())

# Task 0 is start
# Task 1 is start
# Task 2 is start
# Task 0 is done
# Task 1 is done
# Task 2 is done
# [0, 1, 2]
