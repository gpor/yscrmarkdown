from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from lib.classes import Project
from lib.utils import url_to_filename
import json
import yaml

class SpacedTextExtraction(JsonCssExtractionStrategy):
    def _get_element_text(self, element) -> str:
        return element.get_text("\n", strip=True)

async def scrape_to_yaml(name, urls, schema, chat_system_prompt, vector_content_process):
    config = CrawlerRunConfig(
        extraction_strategy=SpacedTextExtraction(schema)
    )
    project = Project(name)

    if not project.directory.exists():
        project.directory.mkdir(parents=True, exist_ok=True)

    config_data = {
        "chat_system_prompt": chat_system_prompt.strip(),
        "vector_content_process": vector_content_process,
    }
    with open(project.directory.config_path, 'w') as f:
        json.dump(config_data, f, indent=2)

    scrape_dir = project.create_new_scrape_dir()
    scrape_dir.mkdir(parents=True, exist_ok=True)

    async with AsyncWebCrawler() as crawler:
        for url in urls:
            print(f"→ Scraping {url}")
            result = await crawler.arun(
                url=url,
                config=config
            )

            if result.success and result.extracted_content:
                data = json.loads(result.extracted_content)
                output_file = scrape_dir / url_to_filename(url)
                with open(output_file, 'w') as f:
                    yaml.dump(data, f, allow_unicode=True, sort_keys=False)
                print(f"  • Found {len(data)} items → saved to {output_file}")
            else:
                status = result.status if not result.success else "no content"
                print(f"  ! Crawl failed for {url}: {status}")
                
        print(' ')
        print(f"  Done. Data saved in {scrape_dir}/")
        print(' ')

