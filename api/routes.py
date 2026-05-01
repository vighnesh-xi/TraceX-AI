import os
import tempfile
import subprocess
from fastapi import APIRouter, HTTPException
from loguru import logger
from api.schemas import IndexRequest, QueryRequest, QueryResponse
from ingestion.repo_loader import RepoLoader
from ingestion.file_classifier import FileClassifier
from parsing.ast_parser import ASTParser
from parsing.doc_parser import DocParser
from parsing.config_parser import ConfigParser
from parsing.metadata_builder import MetadataBuilder
from indexing.embedder import Embedder
from indexing.faiss_store import FAISSStore
from indexing.bm25_index import BM25Index
from indexing.hybrid_retriever import HybridRetriever
from graph.dependency_graph import DependencyGraph
from retrieval.retrieval_orchestrator import RetrievalOrchestrator
from retrieval.context_builder import ContextBuilder
from reasoning.llm_client import LLMClient
from reasoning.prompt_builder import PromptBuilder
from reasoning.response_formatter import ResponseFormatter

router = APIRouter()

_state = {}


def get_state():
    if not _state:
        raise HTTPException(
            status_code=400,
            detail="Repository not indexed yet. Call /index first."
        )
    return _state


def ensure_list(value):
    """Coerce any value to a list safely."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        # Convert dict to list of {key, value} items for frontend rendering
        return [{"label": k, "content": v} for k, v in value.items()]
    return [value]


@router.post("/index")
def index_repository(req: IndexRequest):
    try:
        repo_path = req.repo_path
        tmp_dir = None

        if req.github_url:
            if not req.github_url.startswith("https://github.com/"):
                raise HTTPException(
                    status_code=400,
                    detail="Only public GitHub URLs starting with https://github.com/ are supported."
                )
            tmp_dir = tempfile.mkdtemp()
            logger.info(f"Cloning {req.github_url} into {tmp_dir}")
            result = subprocess.run(
                ["git", "clone", "--depth=1", req.github_url, tmp_dir],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Git clone failed: {result.stderr.strip() or result.stdout.strip()}"
                )
            repo_path = tmp_dir

        if not repo_path:
            raise HTTPException(
                status_code=400,
                detail="Provide either repo_path (local path) or github_url."
            )

        if not os.path.exists(repo_path):
            raise HTTPException(
                status_code=400,
                detail=f"Path does not exist: {repo_path}"
            )

        logger.info(f"Indexing: {repo_path}")

        loader = RepoLoader()
        files = loader.load(repo_path)

        if not files:
            raise HTTPException(
                status_code=400,
                detail=f"No supported files found in: {repo_path}"
            )

        classifier = FileClassifier()
        ast_parser = ASTParser()
        doc_parser = DocParser()
        cfg_parser = ConfigParser()
        meta_builder = MetadataBuilder()
        embedder = Embedder()
        faiss_store = FAISSStore()
        bm25_index = BM25Index()
        dep_graph = DependencyGraph()

        all_chunks = []
        for f in files:
            enriched = classifier.enrich(f)
            ftype = enriched.get("file_type", "code")

            if ftype == "code":
                chunks = ast_parser.parse(enriched)
            elif ftype == "doc":
                chunks = doc_parser.parse(enriched)
            elif ftype == "config":
                chunks = cfg_parser.parse(enriched)
            elif ftype == "build":
                chunks = cfg_parser.parse(enriched)
            else:
                continue

            for chunk in chunks:
                chunk = meta_builder.enrich(chunk, ftype)
                all_chunks.append(chunk)

        logger.info(f"Total chunks before embedding: {len(all_chunks)}")

        if not all_chunks:
            raise HTTPException(
                status_code=400,
                detail="Files found but no chunks extracted. Check your parsers."
            )

        texts = [c["content"] for c in all_chunks]
        embeddings = embedder.embed(texts)
        faiss_store.add(embeddings, all_chunks)
        bm25_index.build(all_chunks)
        dep_graph.build(all_chunks)

        _state["retriever"] = HybridRetriever(faiss_store, bm25_index, embedder)
        _state["dep_graph"] = dep_graph
        _state["all_chunks"] = all_chunks

        logger.info(f"Indexing complete: {len(files)} files -> {len(all_chunks)} chunks")

        return {
            "status": "indexed",
            "total_files": len(files),
            "total_chunks": len(all_chunks),
            "source": req.github_url or repo_path,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Indexing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
def query_repo(req: QueryRequest):
    state = get_state()
    try:
        orchestrator = RetrievalOrchestrator(state["retriever"], state["dep_graph"])
        context_builder = ContextBuilder()
        prompt_builder = PromptBuilder()
        llm = LLMClient()
        formatter = ResponseFormatter()

        retrieval_result = orchestrator.run(req.query, req.top_k)
        context = context_builder.build(retrieval_result)
        system_prompt, user_prompt = prompt_builder.build(
            req.query,
            context,
            retrieval_result["query_type"]
        )
        raw_answer = llm.generate(system_prompt, user_prompt)
        formatted = formatter.format(raw_answer, retrieval_result)

        return QueryResponse(
            query_type=formatted.get("query_type", req.query_type),
            answer=formatted.get("answer", ""),
            sections=ensure_list(formatted.get("sections")),
            references=ensure_list(formatted.get("references")),
            navigation_hints=ensure_list(formatted.get("navigation_hints")),
            usages=ensure_list(retrieval_result.get("usages")),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))