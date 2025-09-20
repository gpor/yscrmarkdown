from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from lib.classes import Project
from lib.utils import url_to_filename
import re
import base64

def _basic_auth_header(user: str, pwd: str) -> dict:
    token = base64.b64encode(f"{user}:{pwd}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

async def scrape_and_write_to_file(
        name,
        urls,
        chat_system_prompt,
        output_format='md',
        auth: tuple | None = None
    ):
    config = CrawlerRunConfig()
    project = Project(name)
    browser_config = None
    if auth:
        user, pwd = auth
        browser_config = BrowserConfig(headers=_basic_auth_header(user, pwd))

    if not project.directory.exists():
        project.directory.mkdir(parents=True, exist_ok=True)

    project.write_config(chat_system_prompt=chat_system_prompt.strip())
    scrape = project.new_scrape()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for url in urls:
            print(f"→ Scraping {url}")
            result = await crawler.arun(
                url=url,
                config=config
            )

            if result.success and result.cleaned_html:
                output_file = scrape.scraped_text_dir / url_to_filename(url, output_format)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                if (output_format == 'html'):
                    output_text = re.sub(r"[\u2028\u2029]", "\n", result.cleaned_html)
                elif (output_format == 'md'):
                    output_text = result.markdown
                else:
                    raise ValueError(f"Unsupported output format: {output_format}")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                print(f"  • Cleaned HTML saved to {output_file}")
            else:
                status = result.status if not result.success else "no cleaned HTML"
                print(f"  ! Crawl failed for {url}: {status}")
                
        print(' ')
        print(f"  Done. Data saved in {project.directory}/")
        print(' ')

class SpacedTextExtraction(JsonCssExtractionStrategy):
    def _get_element_text(self, element) -> str:
        return element.get_text("\n", strip=True)

