"Homework 7. Async URL Fetcher"

import asyncio
import json
import re
from collections import Counter

import aiohttp
import aiofiles
from bs4 import BeautifulSoup


def get_top_k(html, k=5):
    "Counts top k words"

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    words = re.findall(r"\w+", text)
    word_count = Counter(words)
    top_words = dict(word_count.most_common(k))

    return json.dumps(top_words)


async def fetch_url(url):
    "Fetches url"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                return get_top_k(text)
            return f"HTTP Error: {response.status}"


async def fetch_worker(que):
    "Gets url from queue and fetches it"

    while True:
        url = await que.get()
        try:
            result = await fetch_url(url)
            print(f"URL: {url}    Result: {result}")
        except Exception:
            print(f"URL: {url}    Result: Something went wrong")
        finally:
            que.task_done()


async def url_producer(queue, file_path):
    "Puts urls in queue"

    async with aiofiles.open(file_path, "r") as file:
        async for line in file:
            await queue.put(line.strip())


async def main(n_workers, file):
    "Main corutine"

    queue = asyncio.Queue(maxsize=n_workers + 5)

    workers = [asyncio.create_task(fetch_worker(queue)) for _ in range(n_workers)]

    await url_producer(queue, file)

    await queue.join()

    for worker in workers:
        worker.cancel()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Async URL Fetcher")
    parser.add_argument("n_workers", type=int, help="Number of workers")
    parser.add_argument("file", type=str, help="File with a list of URLs")

    args = parser.parse_args()
    n = args.n_workers
    filename = args.file

    asyncio.run(main(n, filename))