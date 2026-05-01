import os
from pathlib import Path
from typing import List, Dict
from loguru import logger

# ─── Files and directories to skip entirely ───────────────────────────────────
SKIP_FILENAMES = {
    "app.js", "app.min.js", "vendor.js", "bootstrap.js",
    "jquery.js", "jquery.min.js", "mix-manifest.json",
    "package-lock.json", "yarn.lock", "composer.lock",
    "adminer.php", "robots.txt", "file1.txt",
}

SKIP_EXTENSIONS = {
    ".min.js", ".min.css", ".map", ".lock",
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".zip", ".tar", ".gz", ".rar",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".mp4", ".mp3", ".avi", ".mov",
    ".bin", ".exe", ".dll", ".so",
}

SKIP_DIRS = {
    "node_modules", ".git", "vendor", "storage",
    "public/js", "public/css", "public/fonts", "public/images",
    "bootstrap/cache", ".idea", "__pycache__",
    ".vscode", "dist", "build", "coverage",
    "tests/fixtures",
}

# ─── File type classification ─────────────────────────────────────────────────
CODE_EXTENSIONS = {
    ".py", ".java", ".js", ".ts", ".php",
    ".rb", ".go", ".cs", ".cpp", ".c", ".h",
    ".swift", ".kt", ".rs", ".scala",
}

CONFIG_EXTENSIONS = {
    ".json", ".yaml", ".yml", ".env",
    ".ini", ".toml", ".xml", ".conf",
}

DOC_EXTENSIONS = {
    ".md", ".txt", ".rst", ".tex",
}

BUILD_FILES = {
    "pom.xml", "package.json", "composer.json",
    "build.gradle", "Makefile", "Dockerfile",
    "requirements.txt", "setup.py", "pyproject.toml",
}


class RepoLoader:
    def __init__(self):
        self.loaded_files: List[Dict] = []

    def load(self, repo_path: str) -> List[Dict]:
        """
        Traverse the repo, classify each file, and return a list of file info dicts.
        """
        self.loaded_files = []
        repo_root = Path(repo_path).resolve()

        if not repo_root.exists():
            logger.error(f"Repo path does not exist: {repo_root}")
            return []

        logger.info(f"Loading repository: {repo_root}")
        total = 0
        skipped = 0

        for file_path in repo_root.rglob("*"):
            if not file_path.is_file():
                continue

            relative = file_path.relative_to(repo_root)
            relative_str = str(relative)

            # Skip check
            if self._should_skip(file_path, relative_str):
                skipped += 1
                continue

            file_info = self._build_file_info(file_path, relative_str)
            if file_info:
                self.loaded_files.append(file_info)
                total += 1

        logger.info(f"Loaded {total} files | Skipped {skipped} files")
        return self.loaded_files

    def _should_skip(self, file_path: Path, relative_str: str) -> bool:
        filename = file_path.name
        ext = file_path.suffix.lower()

        # Skip by exact filename
        if filename in SKIP_FILENAMES:
            return True

        # Skip minified / compiled files
        if filename.endswith(".min.js") or filename.endswith(".min.css"):
            return True

        # Skip by extension
        if ext in SKIP_EXTENSIONS:
            return True

        # Skip by directory (check each part of relative path)
        parts = Path(relative_str).parts
        for skip_dir in SKIP_DIRS:
            # Handle both single-level and nested skip dirs
            skip_parts = Path(skip_dir).parts
            for i in range(len(parts) - len(skip_parts) + 1):
                if parts[i:i+len(skip_parts)] == skip_parts:
                    return True

        # Skip very large files (> 500KB)
        try:
            if file_path.stat().st_size > 500_000:
                logger.debug(f"Skipping large file: {relative_str}")
                return True
        except Exception:
            return True

        return False

    def _build_file_info(self, file_path: Path, relative_str: str) -> Dict:
        ext = file_path.suffix.lower()
        filename = file_path.name

        file_type = self._classify_file(ext, filename)
        if file_type is None:
            return None

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            logger.warning(f"Cannot read {relative_str}: {e}")
            return None

        # Skip empty files
        if not content.strip():
            return None

        return {
            "file_path":     str(file_path),
            "relative_path": relative_str,
            "filename":      filename,
            "extension":     ext,
            "file_type":     file_type,
            "content":       content,
            "size":          len(content),
        }

    def _classify_file(self, ext: str, filename: str) -> str:
        if filename in BUILD_FILES:
            return "build"
        if ext in CODE_EXTENSIONS:
            return "code"
        if ext in CONFIG_EXTENSIONS:
            return "config"
        if ext in DOC_EXTENSIONS:
            return "doc"
        return None  # Unknown type — skip