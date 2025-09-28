from lib.classes import Project, Scrape
import inquirer
import yaml
import pprint
import os

class FileProcessor:
    def __init__(self):
        self.chunks = []
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
            for i in range(1, 7):
                if self.current_headings[i]:
                    headings.append(self.current_headings[i])
            self.chunks.append({
                "headings": headings,
                "text": el['TEXT_']
            })
            
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
        with open(text_file, 'r', encoding='utf-8') as f:
            if scrape.project.config_data.output_format == 'yaml':
                data = yaml.safe_load(f)
            elif scrape.project.config_data.output_format == 'json':
                import json
                data = json.load(f)
            else:
                print(f"Unsupported format: {scrape.project.config_data.output_format}")
                continue
        file_processor = FileProcessor()
        file_processor.process_element(data['body'])
        chunks = file_processor.chunks
        # pprint.pprint(chunks)

        base_name = os.path.splitext(os.path.basename(text_file))[0]
        output_path = scrape.chunked_text_dir / f"{base_name}.txt"
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