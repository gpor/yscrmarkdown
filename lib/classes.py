from dataclasses import dataclass
from lib.utils import get_dirs
import json
from typing import Optional, Dict, Any, Union
from pathlib import Path
from datetime import datetime

@dataclass
class ProjectConfig:
    chat_system_prompt: str

@dataclass
class Project:
    name: str
    directory: Union[Path, None] = None
    config_path: Union[Path, None] = None
    config_data: Optional[ProjectConfig] = None
    def __post_init__(self):
        self.directory = Path('storage') / self.name
        self.config_path = self.directory / 'config.json'
        if self.config_path.exists():
            with open(self.config_path, "r") as file:
                self.config_data = json.load(file)

    def get_scrape_dirs(self) -> list[Path]:
        return get_dirs(self.directory)
    
    def new_scrape(self) -> 'Scrape':
        scrape_name = 'scrape_' + datetime.now().strftime("%Y-%m-%d_%H%M")
        return Scrape(project=self, name=scrape_name)

    def write_config(self, chat_system_prompt: str):
        self.config_data = ProjectConfig(chat_system_prompt=chat_system_prompt)
        if not self.directory.exists():
            self.directory.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config_data.__dict__, f, indent=2)

@dataclass
class Scrape:
    project: Project
    name: str
    directory: Union[Path, None] = None
    csv_path: Union[Path, None] = None
    scraped_text_dir: Union[Path, None] = None
    embedding_model_flag_file_path: Union[Path, None] = None
    def __post_init__(self):
        self.directory = Path(self.project.directory) / self.name
        self.csv_path = self.directory / 'scrape.csv'
        self.scraped_text_dir = self.directory / 'scraped_text'
        self.embedding_model_flag_file_path = self.directory / 'embedding_model_flag.txt'
