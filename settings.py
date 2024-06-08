from dataclasses import dataclass


@dataclass
class Settings:
    title: str
    chapters_per_file: int
