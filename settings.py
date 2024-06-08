from dataclasses import dataclass


@dataclass
class Settings:
    chapter_list_html_path: str
    chapters_per_file: int
