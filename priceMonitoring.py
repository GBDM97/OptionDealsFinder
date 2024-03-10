import asyncio

async def start():
    n = 0
    while True:
        print('loop running...'+str(n))
        await asyncio.sleep(2)
        n += 1
