import sys
import asyncio
import time

import aiohttp
import aiofiles


async def write_genre(file_name):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://binaryjazz.us/wp-json/genrenator/v1/genre/") as response:
            genre = await response.json()

    async with aiofiles.open(file_name, "w") as new_file:
        print(f'Writing "{genre}" to "{file_name}"...')
        await new_file.write(genre)


async def main():
    tasks = []

    print('starting...')
    start = time.time()

    for i in range(2):
        tasks.append(write_genre(f'./async/new_file{i}.txt'))

    await asyncio.gather(*tasks)

    end = time.time()
    print(f'finished in {end - start} seconds')


if __name__ == "__main__":
    asyncio.run(main())
