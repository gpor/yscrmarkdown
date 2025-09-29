import inquirer
from lib.classes import Project, Scrape
from lib.ScrapesProcessor import ScrapesProcessor



def process_scraped_text(scrape: Scrape):
    print(f"Processing scraped text in directory: {scrape.scraped_text_dir}")
    files_processor = ScrapesProcessor(scrape)
    for file_processor in files_processor.iterator():
        
        data = file_processor.read_file()
        # if data is None:
        #     continue
        
        heading_processor = None
        if file_processor.base_name == 'home':
            def heading_processor(text):
                if text.strip() == "[Bright Labs](/)":
                    return "Bright Labs"
                return text
        
        file_processor.process_element(data['body'], heading_processor)
        chunks = file_processor.chunks
        # pprint.pprint(chunks)
        
        output_path = scrape.chunked_text_dir / f"{file_processor.base_name}.txt"
        if not scrape.chunked_text_dir.exists():
            scrape.chunked_text_dir.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as out_f:
            for chunk in chunks:
                headings = chunk.get("headings", [])
                text = chunk.get("text", "")
                out_f.write(' > '.join(headings) + '\n')
                out_f.write('------\n')
                out_f.write(text + '\n\n')
        print(f"Chunks written to {output_path}")


async def main():
    project_name = __name__.split('.')[0]
    project = Project(project_name)
    scrape_dirs = project.get_scrape_dirs()
    
    if not scrape_dirs:
        print(f"No scrape directories found in project '{project_name}'. Please run the scraping script first.")
        return
    
    user_selection = inquirer.prompt([
        inquirer.List('scrape_dir',
                      message="Select a scrape directory to process",
                      choices=[d.name for d in scrape_dirs],
                      carousel=True)
    ])
    print('Selected scrape directory:', user_selection['scrape_dir'])
    
    if user_selection and user_selection['scrape_dir']:
        scrape = project.find_selected_scrape(user_selection['scrape_dir'])
        process_scraped_text(scrape)
    else:
        print("No scrape directory selected. Exiting.")
        return