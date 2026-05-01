from typing import Dict

CODE_EXTENSIONS = {".py", ".java", ".js", ".ts", ".cpp", ".c", ".go", ".rb", ".rs", ".php", ".cs"}
CONFIG_EXTENSIONS = {".yaml", ".yml", ".json", ".toml", ".ini", ".env", ".cfg", ".xml"}
DOC_EXTENSIONS = {".md", ".txt", ".rst", ".tex"}
BUILD_FILES = {"pom.xml", "package.json", "build.gradle", "Makefile", "Dockerfile", "requirements.txt"}

class FileClassifier:
    @staticmethod
    def classify(file_info: Dict) -> str:
        ext = file_info.get("extension", "")
        name = file_info.get("relative_path", "").split("/")[-1].split("\\")[-1]

        if name in BUILD_FILES:
            return "build"
        if ext in CODE_EXTENSIONS:
            return "code"
        if ext in CONFIG_EXTENSIONS:
            return "config"
        if ext in DOC_EXTENSIONS:
            return "doc"
        return "unknown"

    @staticmethod
    def enrich(file_info: Dict) -> Dict:
        file_info["file_type"] = FileClassifier.classify(file_info)
        return file_info