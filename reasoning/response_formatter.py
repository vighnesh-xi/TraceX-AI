import re
from typing import Dict, List

class ResponseFormatter:
    def format(self, raw_answer: str, retrieval_result: Dict) -> Dict:
        sections = self._extract_sections(raw_answer)
        refs = self._extract_references(retrieval_result)
        return {
            "answer": raw_answer,
            "sections": sections,
            "query_type": retrieval_result.get("query_type"),
            "references": refs,
            "navigation_hints": self._navigation_hints(retrieval_result),
        }

    def _extract_sections(self, text: str) -> Dict[str, str]:
        patterns = {
            "Overview":                 r"\*\*Overview\*\*(.*?)(?=\*\*Location\*\*|\*\*Step-by-step|\*\*Related|\*\*Notes\*\*|$)",
            "Location":                 r"\*\*Location\*\*(.*?)(?=\*\*Step-by-step|\*\*Related|\*\*Notes\*\*|$)",
            "Step-by-step explanation": r"\*\*Step-by-step explanation\*\*(.*?)(?=\*\*Related|\*\*Notes\*\*|$)",
            "Related components":       r"\*\*Related components\*\*(.*?)(?=\*\*Notes\*\*|$)",
            "Notes":                    r"\*\*Notes\*\*(.*?)$",
        }
        result = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            result[key] = match.group(1).strip() if match else ""
        return result

    def _extract_references(self, result: Dict) -> List[str]:
        refs = set()
        for chunk in result.get("base_chunks", []):
            refs.add(chunk.get("file_path", ""))
        for nid in result.get("graph_nodes", {}).keys():
            refs.add(nid.split("::")[0])
        return list(filter(None, refs))

    def _navigation_hints(self, result: Dict) -> List[str]:
        hints = []
        for chunk in result.get("base_chunks", [])[:3]:
            name = chunk.get("name")
            path = chunk.get("file_path")
            if name and path and name not in ("__file__", "__init__"):
                hints.append(f"Open {path} → {name}()")
        return hints