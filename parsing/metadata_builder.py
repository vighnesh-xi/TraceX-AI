import re
from typing import Dict, List

TAGS_MAP = {
    "auth": ["login", "token", "jwt", "auth", "password", "credential", "session"],
    "db": ["database", "query", "sql", "repository", "entity", "model", "migrate"],
    "api": ["route", "controller", "endpoint", "request", "response", "handler"],
    "test": ["test", "spec", "assert", "mock", "fixture"],
    "config": ["settings", "config", "env", "yaml", "properties"],
}

class MetadataBuilder:
    def enrich(self, chunk: Dict, file_type: str) -> Dict:
        content = chunk.get("content", "").lower()
        chunk["file_type"] = file_type
        chunk["tags"] = self._extract_tags(content)
        chunk["imports"] = self._extract_imports(chunk.get("content", ""))
        chunk["calls"] = self._extract_calls(chunk.get("content", ""))
        return chunk

    def _extract_tags(self, content: str) -> List[str]:
        found = []
        for tag, keywords in TAGS_MAP.items():
            if any(kw in content for kw in keywords):
                found.append(tag)
        return found

    def _extract_imports(self, content: str) -> List[str]:
        imports = re.findall(r"(?:import|from)\s+([\w\.]+)", content)
        return list(set(imports))

    def _extract_calls(self, content: str) -> List[str]:
        calls = re.findall(r"(\w+)\s*\(", content)
        return list(set(calls))