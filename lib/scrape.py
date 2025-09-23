from lib.classes import Project
from lib.utils import url_to_filename

async def scrape_and_write_to_file(
        project_name: str,
        urls: list[str],
        chat_system_prompt: str,
        output_format: str,
        auth: tuple | None = None
    ):
    project = Project(project_name)

    if output_format == 'json' or output_format == 'yaml':
        from lib.scrape_dom_walk_pw import Url_iterator_pw
        url_iterator = Url_iterator_pw(urls, output_format)
    else:
        from lib.scrape_crawl4ai import Url_iterator
        url_iterator = Url_iterator(urls, output_format, auth)
        
    if not project.directory.exists():
        project.directory.mkdir(parents=True, exist_ok=True)

    project.write_config(chat_system_prompt=chat_system_prompt.strip(), output_format=output_format)
    scrape = project.new_scrape()

    async for url, output_text in url_iterator.crawl():
        if output_text is not None:
            output_file = scrape.scraped_text_dir / url_to_filename(url, output_format)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f" saved in {output_file}")
            print(' ')
    print(' ')
    print(f"  Done. Data saved in {scrape.directory}/")
    print(' ')

