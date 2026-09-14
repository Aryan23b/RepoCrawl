from dataclasses import dataclass
from typing import List
from models.chunk import CodeChunk

@dataclass
class ChatMessage:
    role: str
    content: str

@dataclass
class SearchResult:
    score: float
    chunk: CodeChunk

@dataclass
class ChatResult:
    answer: str
    sources: List[SearchResult]
