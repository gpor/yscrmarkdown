from lib.classes import Project, Scrape
import inquirer
import yaml
import pprint

class FileProcessor:
    def __init__(self):
        self.paragraphs = []
        self.current_headings = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None
        }

    def process_element(self, el):
        # print(el['el'])
        tag = el['el'].split('.')[0]
        heading_level = int(tag[1]) if tag.startswith('h') and len(tag) > 1 and tag[1].isdigit() else 0
        if heading_level != 0:
            if 'TEXT_' in el:
                self.current_headings[heading_level] = el['TEXT_']
                for i in range(heading_level + 1, 7):
                    self.current_headings[i] = None
            else:
                print(f"NO TEXT FOR HEADING {heading_level}")
        elif 'TEXT_' in el:
            headings = []
            # loop from 1 to 6 and append each text to headings
            for i in range(1, 7):
                if self.current_headings[i]:
                    headings.append(self.current_headings[i])
            print(' > '.join(headings))
            print('------')
            print(el['TEXT_'])
            print(' ')
            
        if 'ch' in el and el['ch']:
            for child in el['ch']:
                self.process_element(child)
        


def process_scraped_text(scrape: Scrape):
    print(f"Processing scraped text in directory: {scrape.scraped_text_dir}")
    for text_file in scrape.scraped_text_dir.glob(f"*.{scrape.project.config_data.output_format}"):
        print(' ')
        print(' ')
        print(f"Found text file: {text_file}")
        print(' ')
        # import yaml data
        with open(text_file, 'r', encoding='utf-8') as f:
            if scrape.project.config_data.output_format == 'yaml':
                data = yaml.safe_load(f)
            elif scrape.project.config_data.output_format == 'json':
                import json
                data = json.load(f)
            else:
                print(f"Unsupported format: {scrape.project.config_data.output_format}")
                continue
        # pprint.pprint(data)
        file_processor = FileProcessor()
        file_processor.process_element(data['body'])
        
        
        
        


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