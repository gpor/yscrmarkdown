from lib.scrape import scrape_and_write_to_file
from lib.find_internal_links import find_internal_links, write_internal_links_file


async def main():
    urls = await find_internal_links('http://localhost:3040/', max_depth=3)
    print(' ')
    print(f"\nDiscovered {len(urls)} URLs:")
    # import json
    # print(json.dumps(list(urls), indent=4))
    write_internal_links_file(__name__.split('.')[0], urls)
