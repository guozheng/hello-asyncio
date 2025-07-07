import asyncio
import aiohttp
from codetiming import Timer

async def task(name: str, work_queue: asyncio.Queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.2f}} seconds")
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                url = await asyncio.wait_for(work_queue.get(), timeout=0.1)
                print(f"Task {name} running: url={url}")

                timer = Timer(text=f"Task {name} elapsed time: {{:.2f}} seconds")
                timer.start()
                async with session.get(url) as response:
                    content = await response.text()
                    print(f"Response: {content}")
                timer.stop()

                work_queue.task_done()

            except asyncio.TimeoutError:
                print(f"Task {name} found the queue to be empty")
                break

async def main():
    work_queue = asyncio.Queue()
    for url in [
        "https://httpbin.org/get?name=one",
        "https://httpbin.org/get?name=two",
        "https://httpbin.org/get?name=three",
        "https://httpbin.org/get?name=four",
    ]:
        work_queue.put_nowait(url)
    
    with Timer(text=f"Total elapsed time: {{:.2f}} seconds"):
        await asyncio.gather(
            task("One", work_queue),
            task("Two", work_queue),
        )

if __name__ == "__main__":
    asyncio.run(main())
