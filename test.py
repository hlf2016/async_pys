import asyncio


async def read_data():
    pass

# 需注意，确切讲async def 定义的是一个原生协程函数，而调用协程函数得到的返回值才是该函数对应的协程。不过在口头交流中，一般不会刻意区分这两者
print(type(read_data))  # function
print(type(asyncio.run(read_data())))  # coroutine


async def say_hello():
    print('in say_hello')
    return 'Hello'


async def say_world():
    print('in say_world')
    return 'World'


async def say_helloworld():
    print('in say_helloworld')
    value = await say_hello() + await say_world()
    return value


res = asyncio.run(say_helloworld())
print(res)

# 新写一个 run() 函数


def run(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value


result = run(say_helloworld())
print(result)
