from dataclasses import dataclass
from datetime import date
from typing import Literal

@dataclass
class Activity:
    """
    Represents a activity entry.
    """
    title: str
    desc: str
    start_date: date
    end_date: date
    
