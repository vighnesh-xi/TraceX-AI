import re
from loguru import logger


# Keyword sets per query type
NAVIGATE_KEYWORDS = [
    "where is", "where are", "which file", "find function",
    "locate", "in which file", "where does", "where can i find",
    "where is the", "present in", "defined in",
]

FLOW_KEYWORDS = [
    "how does", "how do", "flow", "trace", "step by step",
    "execution", "works", "walk me through", "explain how",
    "how is", "what happens when",
]

IMPACT_KEYWORDS = [
    "what breaks", "what happens if", "impact", "affect",
    "if i change", "if i modify", "if i remove", "if i delete",
    "dependency", "depends on", "side effect",
]

OVERVIEW_KEYWORDS = [
    "overview", "where should i start", "understand this project",
    "project structure", "explain this repo", "explain the repo",
    "what is this project", "what does this repo do",
    "how is the project", "project overview",
]

EXPLAIN_KEYWORDS = [
    "explain", "what is", "what does", "describe",
    "tell me about", "summarize", "what are",
]


class QueryClassifier:
    def classify(self, query: str) -> str:
        q = query.lower().strip()

        if self._matches(q, NAVIGATE_KEYWORDS):
            result = "NAVIGATE"
        elif self._matches(q, OVERVIEW_KEYWORDS):
            result = "OVERVIEW"
        elif self._matches(q, IMPACT_KEYWORDS):
            result = "IMPACT"
        elif self._matches(q, FLOW_KEYWORDS):
            result = "FLOW"
        elif self._matches(q, EXPLAIN_KEYWORDS):
            result = "EXPLAIN"
        else:
            # Default: if query looks like a "how" question → FLOW
            # otherwise → EXPLAIN
            result = "FLOW" if q.startswith("how") else "EXPLAIN"

        logger.info(f"Classified '{query}' → {result}")
        return result

    def _matches(self, query: str, keywords: list) -> bool:
        return any(kw in query for kw in keywords)