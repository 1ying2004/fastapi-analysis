from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

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
    labels: List[str] = None
    
    def __post_init__(self):
        if self.labels is None:
            self.labels = []

@dataclass
class Contributor:
    login: str
    contributions: int
    avatar_url: str = ''
    
@dataclass
class FileStats:
    extension: str
    count: int
    percentage: float = 0.0

@dataclass 
class AnalysisResult:
    functions: List[dict]
    classes: List[dict]
    imports: List[str]
    complexity: int = 0
