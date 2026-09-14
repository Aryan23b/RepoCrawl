import re
from github import Github
from config.settings import GITHUB_TOKEN
from models.repository import RepositoryInfo

IGNORED_DIRECTORIES = {
    ".git", ".github", "node_modules", "__pycache__",
    ".venv", "venv", "dist", "build", "target", ".idea"
}

class GitHubService:
    def __init__(self):
        self.client = Github(GITHUB_TOKEN)

    def authenticate(self):
        return self.client.get_user()

    @staticmethod
    def extract_repo_name(repo_input: str):
        value = repo_input.strip().rstrip("/")

        pattern = r"^(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/#]+)"
        match = re.match(pattern, value, re.IGNORECASE)

        if match:
            owner = match.group(1)
            repository = match.group(2).removesuffix(".git")
            return f"{owner}/{repository}"

        if re.fullmatch(r"[^/\s]+/[^/\s]+", value):
            owner, repository = value.split("/", 1)
            return f"{owner}/{repository.removesuffix('.git')}"

        return None

    def get_repository(self, repo_name: str):
        return self.client.get_repo(repo_name)

    def get_repository_info(self, repo):
        return RepositoryInfo(
            name=repo.name,
            owner=repo.owner.login,
            full_name=repo.full_name,
            url=repo.html_url,
            default_branch=repo.default_branch,
        )

    def get_source_files(self, repo_name: str):
        repo = self.get_repository(repo_name)
        queue = list(repo.get_contents(""))
        files = []

        while queue:
            item = queue.pop(0)

            if item.type == "dir":
                if item.name.lower() in IGNORED_DIRECTORIES:
                    continue
                try:
                    queue.extend(repo.get_contents(item.path))
                except Exception:
                    continue
            elif item.type == "file":
                files.append(item)

        return repo, files
