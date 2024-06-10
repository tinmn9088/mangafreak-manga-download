from dataclasses import dataclass


@dataclass
class Settings:
    chapter_list_html_path: str
    chapters_per_file: int
    author: str | None = None
    title: str | None = None
    verbose: bool = False
