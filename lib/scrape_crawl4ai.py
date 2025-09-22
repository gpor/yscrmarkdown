from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from lib.utils import url_to_filename, basic_auth_header
import re

class Url_iterator:
    def __init__(self, urls, output_format, auth):
        self.urls = urls
        self.output_format = output_format
        self.config = CrawlerRunConfig()
        self.browser_config = None
        if auth:
            user, pwd = auth
            self.browser_config = BrowserConfig(headers=basic_auth_header(user, pwd))

    async def crawl(self):
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            for url in self.urls:
                result = await crawler.arun(
                    url=url,
                    config=self.config
                )
                if result.success:
                    if self.output_format == 'html':
                        if result.cleaned_html:
                            yield url, re.sub(r"[\u2028\u2029]", "\n", result.cleaned_html)
                        else:
                            print(f"  ! No cleaned HTML for {url}")
                    elif self.output_format == 'md':
                        if result.markdown:
                            yield url, result.markdown
                        else:
                            print(f"  ! No markdown for {url}")
                    else:
                        raise ValueError(f"Unsupported output format: {self.output_format}")
                else:
                    print(f"  ! Crawl failed for {url}: {result.status}")
                    yield url, None


# async def scrape_text(project, urls, chat_system_prompt, output_format, auth):
#     config = CrawlerRunConfig()
#     browser_config = None
#     if auth:
#         user, pwd = auth
#         browser_config = BrowserConfig(headers=basic_auth_header(user, pwd))

#     if not project.directory.exists():
#         project.directory.mkdir(parents=True, exist_ok=True)

#     project.write_config(chat_system_prompt=chat_system_prompt.strip(), output_format=output_format)
#     scrape = project.new_scrape()
    
#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         for url in urls:
#             print(f"→ Scraping {url}")
#             result = await crawler.arun(
#                 url=url,
#                 config=config
#             )

#             if result.success and result.cleaned_html:
#                 output_file = scrape.scraped_text_dir / url_to_filename(url, output_format)
#                 output_file.parent.mkdir(parents=True, exist_ok=True)
#                 if (output_format == 'html'):
#                     output_text = re.sub(r"[\u2028\u2029]", "\n", result.cleaned_html)
#                 elif (output_format == 'md'):
#                     output_text = result.markdown
#                 else:
#                     raise ValueError(f"Unsupported output format: {output_format}")
#                 with open(output_file, 'w', encoding='utf-8') as f:
#                     f.write(output_text)
#                 print(f"  • Text saved to {output_file}")
#             else:
#                 status = result.status if not result.success else "no cleaned HTML"
#                 print(f"  ! Crawl failed for {url}: {status}")
                
#         print(' ')
#         print(f"  Done. Data saved in {project.directory}/")
#         print(' ')


class SpacedTextExtraction(JsonCssExtractionStrategy):
    def _get_element_text(self, element) -> str:
        return element.get_text("\n", strip=True)

