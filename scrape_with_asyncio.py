import asyncio
import concurrent.futures
import time
from math import floor
from multiprocessing import cpu_count
from turtle import title


import aiohttp
import aiofiles
from bs4 import BeautifulSoup


async def get_and_scrape(num_pages: int, output_file: str):
    async with aiohttp.ClientSession() as client, \
            aiofiles.open(output_file, "a+") as f:
        for _ in range(num_pages):
            async with client.get("https://en.wikipedia.org/wiki/Special:Random") as response:
                if response.status > 399:
                    response.raise_for_status()

                page = await response.text()
                soup = BeautifulSoup(page, features="html.parser")
                title = soup.find("h1").text
                await f.write(title + "\t")
        await f.write("\n")


def start_scraping(num_pages: int, output_file: str, i: int):
    print(f"Starting scrape {i}...")
    asyncio.run(get_and_scrape(num_pages, output_file))
    print(f"Finished scrape {i}.")


def main():
    NUM_PAGES = 100
    NUM_CORES = cpu_count()
    OUTPUT_FILE = "./wiki_titles.tsv"

    PAGES_PER_CORE = floor(NUM_PAGES / NUM_CORES)
    PAGES_FOR_FINAL_CORE = PAGES_PER_CORE + NUM_PAGES % NUM_CORES

    print('number of cores:', NUM_CORES)
    futures = []

    with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
        for i in range(NUM_CORES - 1):
            new_future = executor.submit(
                start_scraping,
                num_pages=PAGES_PER_CORE,
                output_file=OUTPUT_FILE, i=i
            )

            futures.append(new_future)

        futures.append(
            executor.submit(
                start_scraping,
                PAGES_FOR_FINAL_CORE,
                OUTPUT_FILE,
                NUM_CORES - 1
            )
        )
    concurrent.futures.wait(futures)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Time to complete: {round(time.time() - start, 2)} seconds.")
