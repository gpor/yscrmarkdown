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
    directory: Path = field(init=False)
    config_path: Path = field(init=False)
    config_data: Optional[ProjectConfig] = None
    def __post_init__(self):
        self.directory = Path('storage') / self.name
        self.config_path = self.directory / 'config.json'
        if self.config_path.exists():
            self.config_data = ProjectConfig(**json.loads(self.config_path.read_text(encoding="utf-8")))

    def get_scrape_dirs(self) -> list[Path]:
        return get_dirs(self.directory)
    
    def new_scrape(self) -> 'Scrape':
        scrape_name = 'scrape_' + datetime.now().strftime("%Y-%m-%d_%H%M")
        return Scrape(project=self, name=scrape_name)

    def write_config(self, chat_system_prompt: str, output_format: str):
        self.config_data = ProjectConfig(
            chat_system_prompt=chat_system_prompt,
            output_format=output_format
        )
        if not self.directory.exists():
            self.directory.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(
            json.dumps(self.config_data.__dict__, indent=2),
            encoding="utf-8"
        )

@dataclass
class Scrape:
    project: Project
    name: str
    directory: Path = field(init=False)
    csv_path: Path = field(init=False)
    scraped_text_dir: Path = field(init=False)
    embedding_model_flag_file_path: Path = field(init=False)
    def __post_init__(self):
        self.directory = Path(self.project.directory) / self.name
        self.csv_path = self.directory / 'scrape.csv'
        self.scraped_text_dir = self.directory / 'scraped_text'
        self.embedding_model_flag_file_path = self.directory / 'embedding_model_flag.txt'

