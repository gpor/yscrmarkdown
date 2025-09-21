import asyncio
from lib.scrape import scrape_and_write_to_file

name = __name__




async def main():
    print(name)

if __name__ == "__main__":
    asyncio.run(main())
