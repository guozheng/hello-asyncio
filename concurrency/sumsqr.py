import asyncio
import concurrent.futures

def sum_squares(n: int) -> int:
    return sum(i * i for i in range(n))

async def main():
    loop = asyncio.get_event_loop()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, sum_squares, 100000)
    
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())