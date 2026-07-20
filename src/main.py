import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from .sseClass import SemanticSearch


# ── Request / Response models ──────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=200, description="Search query")


class ResultItem(BaseModel):
    rank: int
    product: str
    score: float


class IndexResults(BaseModel):
    label: str
    results: list[ResultItem]


class SearchResponse(BaseModel):
    query: str
    indexes: dict[str, IndexResults]
    timing: list[str]


# ── Singleton lifecycle ────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing SemanticSearch singleton ...", flush=True)
    app.state.search_engine = SemanticSearch()
    print("SemanticSearch initialised.", flush=True)
    yield
    print("Shutting down.", flush=True)


app = FastAPI(title="Semantic Search Engine", lifespan=lifespan)
_HERE = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(_HERE, "templates"))


# ── Helpers ────────────────────────────────────────────────────────────────

def _map_results(indices, scores, products) -> list[ResultItem]:
    """Map index tensors to product names and return ranked result items."""
    return [
        ResultItem(rank=r + 1, product=products[idx], score=float(score))
        for r, (idx, score) in enumerate(zip(indices, scores))
    ]


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.get("/")
async def serve_ui(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/api/health")
async def health():
    """Return OK when the search engine singleton is ready."""
    engine: SemanticSearch = app.state.search_engine
    return {"status": "ok", "products": len(engine.products)}


@app.post("/api/search")
async def search(body: SearchRequest):
    engine: SemanticSearch = app.state.search_engine

    # Reset timings before each call (encode_query appends, run() normally does this)
    engine.time_measurements = []

    # Run the search
    engine.encode_query(body.query)

    # Map results
    ivfpq_results = _map_results(
        engine.ranked_indices.tolist(),
        engine.top_scores.tolist(),
        engine.products,
    )
    ivff_results = _map_results(
        engine.ranked_indicesivff.tolist(),
        engine.top_scoresivff.tolist(),
        engine.products,
    )

    return SearchResponse(
        query=body.query,
        indexes={
            "ivfpq": IndexResults(label="FAISS IVFPQ", results=ivfpq_results),
            "ivff": IndexResults(label="FAISS IVFF", results=ivff_results),
        },
        timing=engine.time_measurements,
    )