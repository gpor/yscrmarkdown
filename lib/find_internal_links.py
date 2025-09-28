import re
# import pprint
import urllib.parse
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
from lib.utils import basic_auth_header

async def find_internal_links(
    start_url: str,
    max_depth: int = 2,
    auth: tuple | None = None,
    exact_site: bool = True,
) -> set[str]:
    config = CrawlerRunConfig()
    browser_config = None
    if auth:
        user, pwd = auth
        browser_config = BrowserConfig(headers=basic_auth_header(user, pwd))
    
    visited = set()
    to_visit = [(start_url, 0)]
    discovered = set([start_url])

    # Set root_netloc to the netloc of start_url
    root_netloc = urllib.parse.urlparse(start_url).netloc

    async with AsyncWebCrawler(config=browser_config) as crawler:
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
            for link in links['internal']:
                if 'href' in link:
                    href = link['href']
                    parsed = urllib.parse.urlparse(href)
                    clean_link = parsed._replace(fragment="").geturl()

                    # Only allow exact netloc match (no subdomains)
                    if exact_site and parsed.netloc != root_netloc:
                        print(f"  - Skipping external or subdomain link: {href}")
                        continue
                    
                    # skip pdf
                    if re.search(r'\.pdf$', parsed.path, re.IGNORECASE):
                        print(f"  - Skipping PDF link: {href}")
                        continue

                    if clean_link not in visited:
                        to_visit.append((clean_link, depth + 1))
                else:
                    print('link missing href:', link)

    return sorted(discovered)


def write_internal_links_file(project_name: str, urls: list[str]):
    from lib.classes import Project
    project = Project(project_name)
    project.write_internal_links_file(urls)

