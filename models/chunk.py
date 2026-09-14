from dataclasses import dataclass

@dataclass
class CodeChunk:
    path: str
    content: str
    start_line: int
    end_line: int
