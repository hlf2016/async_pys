import asyncio
import time
import functools


def start_race(start_signal):
    print('start!')
    start_signal.set()


async def runner_one(start_signal):
    print('runner 1: I am ready')
    await start_signal.wait()
    print('runner 1: I am running', time.time())
    await asyncio.sleep(2)
    print('runner 1: I am done', time.time())


async def runner_two(start_signal):
    print('runner 2: I am ready')
    await start_signal.wait()
    print('runner 2: I am running', time.time())
    await asyncio.sleep(3)
    print('runner 2: I am done', time.time())


async def main():
    # Event的作用跟比赛用的信号弹类似，信号弹爆炸了大家都得按它行动。一颗信号弹也只能用一次。
    start_signal = asyncio.Event()
    # 获取当前运行的事件循环
    loop = asyncio.get_running_loop()
    #  `functools.partial(start_race, start_signal)` 是创建一个新的函数，这个新的函数在调用时会调用 `start_race` 函数，并将 `start_signal` 作为参数传入。这是因为 `loop.call_later()` 需要一个无参数的回调函数，但 `start_race` 函数需要一个参数 `start_signal`。通过使用 `functools.partial()`，你可以创建一个新的无参数函数，然后将这个新的函数传递给 `loop.call_later()`。总的来说，如果你直接调用 `start_race(start_signal)`，那么 `start_race` 函数会立即执行。如果你使用 `loop.call_later(0.2, functools.partial(start_race, start_signal))`，那么 `start_race` 函数会在 0.2 秒后执行。
    loop.call_later(
        0.2,
        # 这里不能用 start_race(start_signal) 因为会直接执行
        # functools.partial 则是封装一个新的函数 0.2s 后执行
        functools.partial(start_race, start_signal)
    )
    await asyncio.wait([asyncio.create_task(runner_one(start_signal)), asyncio.create_task(runner_two(start_signal))])

if __name__ == '__main__':
    asyncio.run(main())
