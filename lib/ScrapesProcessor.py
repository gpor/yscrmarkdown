import yaml
import os
from lib.classes import Scrape

class FileProcessor:
    def __init__(self, text_file, scrape_format):
        self.text_file = text_file
        self.scrape_format = scrape_format
        self.base_name = os.path.splitext(os.path.basename(text_file))[0]
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
    
    def read_file(self):
        with open(self.text_file, 'r', encoding='utf-8') as f:
            if self.scrape_format == 'yaml':
                return yaml.safe_load(f)
            elif self.scrape_format == 'json':
                import json
                return json.load(f)
            # else:
            #     print(f"Unsupported format: {self.scrape_format}")
            #     return None

class ScrapesProcessor:
    def __init__(self, scrape: Scrape):
        self.scrape_format = scrape.project.config_data.output_format
        if self.scrape_format not in ['yaml', 'json']:
            raise ValueError(f"Unsupported scrape format: {self.scrape_format}")
        self.scrape = scrape
    
    def iterator(self):
        for text_file in self.scrape.scraped_text_dir.glob(f"*.{self.scrape_format}"):
            file_processor = FileProcessor(text_file, self.scrape_format)
            print(' ')
            print(' ')
            print(f"_ {file_processor.base_name}")
            yield file_processor
