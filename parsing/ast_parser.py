import re
from typing import List, Dict
from loguru import logger

# tree-sitter based AST parser for Python, Java, JavaScript
try:
    import tree_sitter_python as tspython
    import tree_sitter_java as tsjava
    import tree_sitter_javascript as tsjs
    from tree_sitter import Language, Parser
    LANGUAGES = {
        ".py":  Language(tspython.language()),
        ".java": Language(tsjava.language()),
        ".js":   Language(tsjs.language()),
    }
    TS_AVAILABLE = True
except Exception as e:
    logger.warning(f"tree-sitter not fully loaded: {e}. Falling back to regex.")
    TS_AVAILABLE = False


class ASTParser:
    def __init__(self):
        self.parsers: Dict = {}
        if TS_AVAILABLE:
            for ext, lang in LANGUAGES.items():
                p = Parser(lang)
                self.parsers[ext] = p

    def parse(self, file_info: Dict) -> List[Dict]:
        ext = file_info.get("extension", "")
        content = file_info.get("content", "")
        path = file_info.get("relative_path", "")

        if ext in self.parsers and TS_AVAILABLE:
            return self._ts_parse(self.parsers[ext], content, path, ext)
        return self._regex_parse(content, path, ext)

    # ─────────────────────────────────────────────
    # tree-sitter parsing (Python, Java, JS)
    # ─────────────────────────────────────────────
    def _ts_parse(self, parser, content: str, path: str, ext: str) -> List[Dict]:
        chunks = []
        try:
            tree = parser.parse(bytes(content, "utf8"))
            root = tree.root_node

            def visit(node):
                if node.type in (
                    "function_definition",
                    "method_declaration",
                    "function_declaration",
                    "class_definition",
                    "class_declaration",
                ):
                    name_node = node.child_by_field_name("name")
                    name = name_node.text.decode("utf8") if name_node else "unknown"
                    chunk_text = content[node.start_byte:node.end_byte]
                    chunks.append({
                        "chunk_id": f"{path}::{name}",
                        "file_path": path,
                        "name": name,
                        "type": node.type,
                        "content": chunk_text[:1500],
                        "start_line": node.start_point[0],
                        "end_line": node.end_point[0],
                        "source": "ast",
                    })
                for child in node.children:
                    visit(child)

            visit(root)
        except Exception as e:
            logger.warning(f"tree-sitter parse error for {path}: {e}")

        return chunks if chunks else [self._whole_file_chunk(content, path)]

    # ─────────────────────────────────────────────
    # Regex-based parsing (PHP, Python fallback, etc.)
    # ─────────────────────────────────────────────
    def _regex_parse(self, content: str, path: str, ext: str) -> List[Dict]:
        chunks = []

        if ext == ".php":
            chunks = self._parse_php(content, path)

        elif ext == ".py":
            for m in re.finditer(r"^(def |class )(\w+)", content, re.MULTILINE):
                block = self._extract_block(content, m.start())
                chunks.append({
                    "chunk_id": f"{path}::{m.group(2)}",
                    "file_path": path,
                    "name": m.group(2),
                    "type": "function" if m.group(1).strip() == "def" else "class",
                    "content": block,
                    "start_line": content[:m.start()].count("\n"),
                    "end_line": content[:m.end()].count("\n"),
                    "source": "regex",
                })

        elif ext in (".js", ".ts"):
            chunks = self._parse_js(content, path)

        elif ext == ".java":
            chunks = self._parse_java(content, path)

        elif ext in (".rb",):
            chunks = self._parse_ruby(content, path)

        elif ext in (".go",):
            chunks = self._parse_go(content, path)

        if not chunks:
            chunks.append(self._whole_file_chunk(content, path))

        return chunks

    # ─────────────────────────────────────────────
    # PHP parser
    # ─────────────────────────────────────────────
    def _parse_php(self, content: str, path: str) -> List[Dict]:
        chunks = []

        # Extract class definitions
        for m in re.finditer(
                r"class\s+(\w+)(?:\s+extends\s+\w+)?(?:\s+implements\s+[\w,\s]+)?\s*\{",
                content
        ):
            chunks.append({
                "chunk_id": f"{path}::class_{m.group(1)}",
                "file_path": path,
                "name": m.group(1),
                "type": "class",
                "content": content[m.start():m.start() + 600],
                "start_line": content[:m.start()].count("\n"),
                "end_line": content[:m.end()].count("\n"),
                "source": "regex_php",
            })

        method_pattern = re.compile(
            r"(?:(?:public|private|protected|static|abstract|final)\s+)*"
            r"function\s+(\w+)\s*\([^)]{0,200}\)\s*(?::\s*\??\w+)?\s*(?:\{|;)",
            re.MULTILINE,
        )
        for m in method_pattern.finditer(content):
            func_name = m.group(1)
            if func_name in ("__construct", "__destruct", "__toString"):
                continue  # skip magic methods unless you want them
            body = self._extract_php_block(content, m.start())
            chunks.append({
                "chunk_id": f"{path}::{func_name}",
                "file_path": path,
                "name": func_name,
                "type": "method",
                "content": body[:2000],
                "start_line": content[:m.start()].count("\n"),
                "end_line": content[:m.start() + len(body)].count("\n"),
                "source": "regex_php",
            })

        return chunks

    def _extract_php_block(self, content: str, start: int) -> str:
        """Extract a PHP function/method block by counting braces."""
        brace_start = content.find("{", start)
        if brace_start == -1:
            return content[start:start + 500]
        depth = 0
        i = brace_start
        while i < len(content):
            if content[i] == "{":
                depth += 1
            elif content[i] == "}":
                depth -= 1
                if depth == 0:
                    return content[start:i + 1]
            i += 1
        return content[start:start + 1000]

    # ─────────────────────────────────────────────
    # JavaScript / TypeScript parser
    # ─────────────────────────────────────────────
    def _parse_js(self, content: str, path: str) -> List[Dict]:
        chunks = []
        patterns = [
            # function declarations
            r"(?:async\s+)?function\s+(\w+)\s*\(",
            # arrow functions assigned to const/let/var
            r"(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(",
            # class declarations
            r"class\s+(\w+)",
            # method shorthand in objects/classes
            r"^\s*(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{",
        ]
        for pattern in patterns:
            for m in re.finditer(pattern, content, re.MULTILINE):
                name = m.group(1)
                block = self._extract_block(content, m.start())
                chunks.append({
                    "chunk_id": f"{path}::{name}",
                    "file_path": path,
                    "name": name,
                    "type": "function",
                    "content": block,
                    "start_line": content[:m.start()].count("\n"),
                    "end_line": content[:m.end()].count("\n"),
                    "source": "regex_js",
                })
        return chunks

    # ─────────────────────────────────────────────
    # Java parser
    # ─────────────────────────────────────────────
    def _parse_java(self, content: str, path: str) -> List[Dict]:
        chunks = []

        # Class declarations
        for m in re.finditer(
            r"(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)",
            content
        ):
            chunks.append({
                "chunk_id": f"{path}::class_{m.group(1)}",
                "file_path": path,
                "name": m.group(1),
                "type": "class",
                "content": content[m.start():m.start() + 600],
                "start_line": content[:m.start()].count("\n"),
                "end_line": content[:m.end()].count("\n"),
                "source": "regex_java",
            })

        # Method declarations
        method_pattern = re.compile(
            r"(?:public|private|protected)\s+(?:static\s+)?(?:\w+\s+)+(\w+)\s*\([^)]*\)\s*(?:throws\s+[\w,\s]+)?\s*\{",
            re.MULTILINE,
        )
        for m in method_pattern.finditer(content):
            name = m.group(1)
            block = self._extract_php_block(content, m.start())  # brace matching works for Java too
            chunks.append({
                "chunk_id": f"{path}::{name}",
                "file_path": path,
                "name": name,
                "type": "method",
                "content": block[:1500],
                "start_line": content[:m.start()].count("\n"),
                "end_line": content[:m.start() + len(block)].count("\n"),
                "source": "regex_java",
            })

        return chunks

    # ─────────────────────────────────────────────
    # Ruby parser
    # ─────────────────────────────────────────────
    def _parse_ruby(self, content: str, path: str) -> List[Dict]:
        chunks = []
        for m in re.finditer(r"^\s*def\s+(\w+)", content, re.MULTILINE):
            block = self._extract_block(content, m.start())
            chunks.append({
                "chunk_id": f"{path}::{m.group(1)}",
                "file_path": path,
                "name": m.group(1),
                "type": "function",
                "content": block,
                "start_line": content[:m.start()].count("\n"),
                "end_line": content[:m.end()].count("\n"),
                "source": "regex_ruby",
            })
        return chunks

    # ─────────────────────────────────────────────
    # Go parser
    # ─────────────────────────────────────────────
    def _parse_go(self, content: str, path: str) -> List[Dict]:
        chunks = []
        for m in re.finditer(r"^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(", content, re.MULTILINE):
            block = self._extract_php_block(content, m.start())
            chunks.append({
                "chunk_id": f"{path}::{m.group(1)}",
                "file_path": path,
                "name": m.group(1),
                "type": "function",
                "content": block[:1500],
                "start_line": content[:m.start()].count("\n"),
                "end_line": content[:m.start() + len(block)].count("\n"),
                "source": "regex_go",
            })
        return chunks

    # ─────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────
    def _extract_block(self, content: str, start: int, max_lines: int = 40) -> str:
        """Extract up to max_lines lines from start position."""
        lines = content[start:].split("\n")
        return "\n".join(lines[:max_lines])

    def _whole_file_chunk(self, content: str, path: str) -> Dict:
        """Fallback: treat entire file as one chunk."""
        return {
            "chunk_id": f"{path}::__file__",
            "file_path": path,
            "name": "__file__",
            "type": "file",
            "content": content[:3000],
            "start_line": 0,
            "end_line": content.count("\n"),
            "source": "fallback",
        }