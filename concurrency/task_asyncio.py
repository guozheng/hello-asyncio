import asyncio
from codetiming import Timer

async def task(name: str, work_queue: asyncio.Queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.2f}} seconds")
    while not work_queue.empty():
        delay = await work_queue.get()
        print(f"Task {name} running")
        timer.start()
        await asyncio.sleep(delay)
        timer.stop()

async def main():
    work_queue = asyncio.Queue()
    for work in [1, 2, 3, 4]:
        # compare with the alternative await work_queue.put(work)
        work_queue.put_nowait(work)
    
    with Timer(text=f"Total elapsed time: {{:.2f}} seconds"):
        await asyncio.gather(
            task("One", work_queue),
            task("Two", work_queue),
        )

if __name__ == "__main__":
    asyncio.run(main())

    
    