from dataclasses import dataclass

@dataclass
class RepositoryInfo:
    name: str
    owner: str
    full_name: str
    url: str
    default_branch: str
