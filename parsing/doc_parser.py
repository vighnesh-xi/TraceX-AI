import re
from typing import List, Dict

class DocParser:
    def parse(self, file_info: Dict) -> List[Dict]:
        content = file_info.get("content", "")
        path = file_info.get("relative_path", "")
        ext = file_info.get("extension", "")

        if ext == ".md":
            return self._parse_markdown(content, path)
        if ext == ".tex":
            return self._parse_latex(content, path)
        return self._parse_plain(content, path)

    def _parse_markdown(self, content: str, path: str) -> List[Dict]:
        chunks = []
        sections = re.split(r"(?m)^#{1,3} .+", content)
        headers = re.findall(r"(?m)^#{1,3} (.+)", content)
        for i, section in enumerate(sections[1:], 0):
            chunks.append({
                "chunk_id": f"{path}::section_{i}",
                "file_path": path,
                "name": headers[i] if i < len(headers) else f"section_{i}",
                "type": "doc_section",
                "content": section.strip()[:2000],
                "source": "markdown",
            })
        if not chunks:
            chunks.append({"chunk_id": f"{path}::doc", "file_path": path, "name": "doc", "type": "doc", "content": content[:2000], "source": "plain"})
        return chunks

    def _parse_latex(self, content: str, path: str) -> List[Dict]:
        clean = re.sub(r"\\[a-zA-Z]+\{.*?\}", " ", content)
        clean = re.sub(r"[{}$\\]", " ", clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        return [{"chunk_id": f"{path}::tex", "file_path": path, "name": "latex_doc", "type": "doc", "content": clean[:2000], "source": "latex"}]

    def _parse_plain(self, content: str, path: str) -> List[Dict]:
        return [{"chunk_id": f"{path}::plain", "file_path": path, "name": "plain_doc", "type": "doc", "content": content[:2000], "source": "plain"}]