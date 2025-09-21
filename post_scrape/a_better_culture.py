import asyncio
from lib.scrape import scrape_and_write_to_file

name = 'a_better_culture' # /storage/{name}/scrape_{timestamp}




async def main():
    print(name)

if __name__ == "__main__":
    asyncio.run(main())
