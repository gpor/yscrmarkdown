from dataclasses import dataclass, field
from lib.utils import get_dirs
import json
from typing import Optional
from pathlib import Path
from datetime import datetime

@dataclass
class ProjectConfig:
    chat_system_prompt: str
    output_format: str

@dataclass
class Project:
    name: str
    temp_directory: Path = field(init=False)
    canon_directory: Path = field(init=False)
    config_path: Path = field(init=False)
    config_data: Optional[ProjectConfig] = None
    internal_links_file: Path = field(init=False)
    def __post_init__(self):
        self.temp_directory = Path('storage/temp') / self.name
        self.canon_directory = Path('storage/canon') / self.name
        self.config_path = self.canon_directory / 'config.json'
        if self.config_path.exists():
            self.config_data = ProjectConfig(**json.loads(self.config_path.read_text(encoding="utf-8")))
        self.internal_links_file = self.canon_directory / 'internal_links.py'

    def get_scrape_dirs(self) -> list[Path]:
        return get_dirs(self.temp_directory, self.canon_directory / "scrape")

    def new_scrape(self) -> 'Scrape':
        scrape_name = 'scrape_' + datetime.now().strftime("%Y-%m-%d_%H%M")
        return Scrape(project=self, name=scrape_name, is_canon=False)

    def find_selected_scrape(self, name) -> 'Scrape':
        is_canon = name == 'scrape'
        return Scrape(project=self, name=name, is_canon=is_canon)

    def write_config(self, chat_system_prompt: str, output_format: str):
        self.config_data = ProjectConfig(
            chat_system_prompt=chat_system_prompt,
            output_format=output_format
        )
        if not self.canon_directory.exists():
            self.canon_directory.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(
            json.dumps(self.config_data.__dict__, indent=2),
            encoding="utf-8"
        )

    def write_internal_links_file(self, urls):
        if not self.canon_directory.exists():
            self.canon_directory.mkdir(parents=True, exist_ok=True)
        with open(self.internal_links_file, 'w', encoding='utf-8') as f:
            f.write(f"# Auto-generated internal links for project '{self.name}'\n")
            f.write("urls = [\n")
            for url in urls:
                f.write(f"    '{url}',\n")
            f.write("]\n")
        print(f" Internal links written to {self.internal_links_file}")

@dataclass
class Scrape:
    project: Project
    name: str
    directory: Path = field(init=False)
    csv_path: Path = field(init=False)
    scraped_text_dir: Path = field(init=False)
    chunked_text_dir: Path = field(init=False)
    embedding_model_flag_file_path: Path = field(init=False)
    is_canon: bool
    def __post_init__(self):
        parent_dir = self.project.canon_directory if self.is_canon else self.project.temp_directory
        self.directory = Path(parent_dir) / self.name
        self.csv_path = self.directory / 'scrape.csv'
        self.scraped_text_dir = self.directory / 'scraped_text'
        self.chunked_text_dir = self.directory / 'chunked_text'
        self.embedding_model_flag_file_path = self.directory / 'embedding_model_flag.txt'

