import asyncio
import itertools as it
import os
import time
import random

async def createitem(num: int = 5) -> str:
    return os.urandom(num).hex()

async def randsleep(caller=None) -> None:
    if caller is None:
        return
    delay = random.randint(0, 5)
    if caller:
        print(f"{caller} sleeping for {delay} seconds")
    await asyncio.sleep(delay)

async def produce(id: int, q: asyncio.Queue) -> None:
    for _ in it.repeat(None, random.randint(0, 5)):
        await randsleep(caller=f"Producer {id}")
        item = await createitem()
        ts = time.perf_counter()
        await q.put((item, ts))
        print(f"Producer {id} added <{item}> to queue")
    
async def consume(id: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Consumer {id}")
        item, ts = await q.get()
        q.task_done()
        print(f"Consumer {id} consumed <{item}> from queue at {time.perf_counter() - ts:.2f} seconds")

async def main() -> None:
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(i, q)) for i in range(3)]
    consumers = [asyncio.create_task(consume(i, q)) for i in range(3)]
    
    await asyncio.gather(*producers)
    await q.join()
    for c in consumers:
        c.cancel()

if __name__ == "__main__":
    asyncio.run(main())
