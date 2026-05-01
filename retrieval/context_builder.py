from typing import Dict, List

SKIP_NAMES = {"__file__", "__init__"}

class ContextBuilder:
    def build(self, retrieval_result: Dict, config_chunks: List[Dict] = None, doc_chunks: List[Dict] = None) -> str:
        parts = []
        all_chunks = retrieval_result["base_chunks"]

        # Separate by type, skip weak __init__ chunks
        code_chunks = [c for c in all_chunks if c.get("file_type") == "code" and c.get("name") not in SKIP_NAMES]
        doc_hits = doc_chunks or [c for c in all_chunks if c.get("file_type") == "doc"]
        cfg_hits = config_chunks or [c for c in all_chunks if c.get("file_type") == "config"]

        # Fallback: if filtering removed everything, include all code
        if not code_chunks:
            code_chunks = [c for c in all_chunks if c.get("file_type") == "code"]

        if code_chunks:
            parts.append("[CODE CONTEXT]")
            for c in code_chunks[:6]:
                parts.append(f"\n# File: {c.get('file_path')} | Function/Class: {c.get('name')} | Tags: {c.get('tags', [])}")
                parts.append(c.get("content", "")[:1000])

        if cfg_hits:
            parts.append("\n[CONFIG CONTEXT]")
            for c in cfg_hits[:2]:
                parts.append(f"\n# File: {c.get('file_path')}")
                parts.append(c.get("content", "")[:500])

        if doc_hits:
            parts.append("\n[DOCUMENTATION CONTEXT]")
            for c in doc_hits[:2]:
                parts.append(f"\n# Doc: {c.get('name')}")
                parts.append(c.get("content", "")[:800])

        if retrieval_result.get("graph_nodes"):
            parts.append("\n[DEPENDENCY GRAPH]")
            for nid, attrs in list(retrieval_result["graph_nodes"].items())[:10]:
                parts.append(f"- {nid} | type={attrs.get('type')} | tags={attrs.get('tags')}")

        if retrieval_result.get("usages"):
            parts.append("\n[SYMBOL USAGES]")
            for u in retrieval_result["usages"][:10]:
                parts.append(f"- {u}")

        return "\n".join(parts)