import re
import pprint
import urllib.parse
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
import asyncio

async def find_internal_links(
    start_url: str,
    max_depth: int = 2,
    same_domain_only: bool = True
) -> set[str]:
    """
    Crawl a site by following internal links.

    Args:
        start_url (str): The starting URL to crawl from.
        max_depth (int): Maximum depth to recurse into links.
        same_domain_only (bool): Restrict crawling to the same domain.

    Returns:
        set[str]: All discovered URLs up to the given depth.
    """
    config = CrawlerRunConfig()
    visited = set()
    to_visit = [(start_url, 0)]
    discovered = set()

    parsed_root = urllib.parse.urlparse(start_url)
    root_netloc = parsed_root.netloc

    async with AsyncWebCrawler() as crawler:
        while to_visit:
            url, depth = to_visit.pop(0)
            if url in visited or depth > max_depth:
                continue

            print(f"→ Crawling {url} (depth {depth})")
            visited.add(url)

            try:
                result = await crawler.arun(url=url, config=config)
            except Exception as e:
                print(f"⚠️ Error fetching {url}: {e}")
                continue

            if not result.success:
                print(f"⚠️ Failed: {url}")
                continue

            discovered.add(url)

            links = result.links or []
            # pprint.pprint(links['internal'])
            for link in links['internal']:
                if 'href' in link:
                    href = link['href']
                    parsed = urllib.parse.urlparse(href)

                    clean_link = parsed._replace(fragment="").geturl()

                    # if not parsed.scheme.startswith("http"):
                    #     print(f"  - Skipping non-http link: {href}")
                    #     continue

                    # if same_domain_only and parsed.netloc != root_netloc:
                    #     print(f"  - Skipping external link: {href}")
                    #     continue
                    
                    # skip pdf
                    if re.search(r'\.pdf$', parsed.path, re.IGNORECASE):
                        print(f"  - Skipping PDF link: {href}")
                        continue

                    if clean_link not in visited:
                        to_visit.append((clean_link, depth + 1))
                else:
                    print('link missing href:', link)

    return discovered

if __name__ == "__main__":
    urls = asyncio.run(find_internal_links("https://abetterculture.org.au/", max_depth=2))
    print(f"\nDiscovered {len(urls)} URLs:")
    for u in urls:
        print(u)
    exit()