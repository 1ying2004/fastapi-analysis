from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Commit:
    hash: str
    author: str
    email: str
    date: datetime
    message: str

@dataclass
class Issue:
    number: int
    title: str
    state: str
    created_at: datetime
    closed_at: Optional[datetime] = None
