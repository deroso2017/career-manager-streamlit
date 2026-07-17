from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class Event:
    title: str
    desc: str
    date: str               # ISO format YYYY-MM-DD (Startdatum)
    end_date: Optional[str] # ISO format YYYY-MM-DD (optional)
    time: str               # HH:MM
    end_time: str           # HH:MM
    category: str
    color: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
