from dataclasses import dataclass
from datetime import date
from typing import Literal

@dataclass
class Application:
    """
    Represents a job application entry.
    """
    company: str
    date: date
    status: Literal["Übermittelt", "Abgesagt"]
    platform: Literal["LinkedIn", "Arbeitsagentur", "Join", "Instaffo", "Stepstone", "Initiative"]
    link: str
