import asyncio
import aiohttp
import aiofiles
import re
import sys
import logging
from typing import IO
from aiohttp import ClientSession
import urllib.error
import urllib.parse

"""
- Read a sequence of URLs from a local file, urls.txt.
- Send GET requests for the URLs and decode the resulting content. If this fails, stop there for a URL.
- Search for the URLs within href tags in the HTML of the responses.
- Write the results to foundurls.txt.
- Do all of the above as asynchronously and concurrently as possible. (Use aiohttp for the requests, and aiofiles for the file-appends. These are two primary examples of IO that are well-suited for the async IO model.)
"""

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stderr
)
logger = logging.getLogger("crawler")
logging.getLogger("chardet.charsetprober").disabled = True

async def fetch(url: str, session: ClientSession, **kwargs) -> str:
    try:
        async with session.get(url, **kwargs) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching {url}: {e}")
        return ""

async def search(url: str, session: ClientSession, **kwargs) -> set[str]:
    result = set()
    try:
        html = await fetch(url, session, **kwargs)
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logger.error(f"Error searching {url}: {e}")
        return result
    except Exception as e:
        logger.exception("Non-aiohttp error: %s", e)
        return result
    else:
        for link in re.findall(r'href="(https?://[^"]*)"', html):
            try:
                final_link = urllib.parse.urljoin(url, link)
            except(urllib.error.URLError, ValueError) as e:
                logger.error(f"Error joining URL {url} and link {link}: {e}")
                continue
            result.add(final_link)
        logger.info("Found %d links in %s", len(result), url)
        return result

async def store(file_path: str, url: str, **kwargs) -> None:
    try:
        res = await search(url, **kwargs)
        if not res:
            return None
        async with aiofiles.open(file_path, "a") as f:
            for link in res:
                await f.write(f"{url}: {link}\n")
            logger.info("Stored %d links from %s", len(res), url)
    except Exception as e:
        logger.exception("Error storing %s: %s", url, e)

async def crawl_and_store(file_path: str, urls: set[str], **kwargs) -> None:
    async with ClientSession() as session:
        tasks = [store(file_path, url, session=session, **kwargs) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import pathlib
    import sys
    
    assert sys.version_info >= (3, 7), "Python 3.7+ required"
    parent_path = pathlib.Path(__file__).parent
    urls_file = parent_path / "urls.txt"
    foundurls_file = parent_path / "foundurls.txt"
    
    with urls_file.open() as f:
        urls = set(f.read().splitlines())
    
    # Create the output file (empty it if it exists)
    foundurls_file.touch()
    foundurls_file.write_text("")
    
    asyncio.run(crawl_and_store(str(foundurls_file), urls))