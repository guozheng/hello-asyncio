import aiohttp
import asyncio

async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, f"https://httpbin.org/get?name={i}") for i in range(3)]
        results = await asyncio.gather(*tasks)
        for i, result in enumerate(results):
            print(f"URL: https://httpbin.org/get?name={i}\nResponse: {result}") 

if __name__ == "__main__":
    asyncio.run(main())
    