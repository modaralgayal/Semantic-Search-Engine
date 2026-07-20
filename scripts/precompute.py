"""
Pre-compute embeddings and FAISS indexes, save to files.
Run this ONCE locally, then commit the files so Render loads them instantly.
"""
import json
import sys
from pathlib import Path

import numpy as np

# Make sure we can import from src/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.components.get_products import get_posts
from src.components.build_model import build_model
from src.components.embeddings import create_embeddings
from src.components.build_faiss_model import (
    faissInitL2,
    faissInitIVFF,
    faissInitIVFPQ,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "src" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 1. Generate products
print("Generating products...", flush=True)
products = get_posts()
print(f"  {len(products)} products generated", flush=True)

# Save products
with open(DATA_DIR / "products.json", "w") as f:
    json.dump(products, f)
print("  Saved to data/products.json", flush=True)

# 2. Load model and create embeddings
print("Loading model...", flush=True)
model = build_model()

print("Creating embeddings...", flush=True)
embeddings = create_embeddings(products, model)
print(f"  Embeddings shape: {embeddings.shape}", flush=True)

# Save embeddings
np.save(DATA_DIR / "embeddings.npy", embeddings)
print("  Saved to data/embeddings.npy", flush=True)

# 3. Build and save FAISS indexes
print("Building FAISS indexes...", flush=True)

print("  FlatL2...", flush=True)
index_l2 = faissInitL2(embeddings)
import faiss
faiss.write_index(index_l2, str(DATA_DIR / "faiss_l2.index"))
print("  Saved to data/faiss_l2.index", flush=True)

print("  IVFFlat...", flush=True)
index_ivff = faissInitIVFF(embeddings)
faiss.write_index(index_ivff, str(DATA_DIR / "faiss_ivff.index"))
print("  Saved to data/faiss_ivff.index", flush=True)

print("  IVFPQ...", flush=True)
index_ivfpq = faissInitIVFPQ(embeddings)
faiss.write_index(index_ivfpq, str(DATA_DIR / "faiss_ivfpq.index"))
print("  Saved to data/faiss_ivfpq.index", flush=True)

print("\n✅ All done! Files saved to:", DATA_DIR)
for f in sorted(DATA_DIR.iterdir()):
    size_mb = f.stat().st_size / (1024 * 1024)
    print(f"  {f.name}: {size_mb:.2f} MB")