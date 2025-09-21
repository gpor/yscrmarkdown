from lib.classes import Project, Scrape
import inquirer


def process_scraped_text(scrape: Scrape):
    print(f"Processing scraped text in directory: {scrape.scraped_text_dir}")
    for text_file in scrape.scraped_text_dir.glob(f"*.{scrape.project.config_data.output_format}"):
        print(f"Found text file: {text_file}")
        # todo read text from text file
        text = text_file.read_text(encoding="utf-8")
        print(f"Text content (first 100 chars): {text[:100]}...")
        # convert text into nested elements
        """
        dom = [
            {
                "el": "html",
                "children": [
                    {"el": "body", "children": [ ... ]
                ]
            }
        ]
        """
        
        
        


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
        scrape = Scrape(project=project, name=user_selection['scrape_dir'])
        # print('scrape.scraped_text_dir:', scrape.scraped_text_dir)
        process_scraped_text(scrape)
    else:
        print("No scrape directory selected. Exiting.")
        return