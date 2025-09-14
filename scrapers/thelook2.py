import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def main():
    config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://thelookortho.com.au", config=config)

        if result.success:
            # print(result.html)         # Raw HTML
            print(result.cleaned_html) # Cleaned HTML
            # print(result.markdown.raw_markdown) # Raw markdown from cleaned html
            # print(result.markdown.fit_markdown) # Most relevant content in markdown
        else:
            print("Crawl failed:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())
