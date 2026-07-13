import json
import logging
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

import numpy as np

from backend.config import settings

logger = logging.getLogger(__name__)

try:
    import faiss
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("sentence-transformers or faiss not installed. Vector search disabled.")


class EmbeddingService:
    def __init__(self):
        self.model: Optional["SentenceTransformer"] = None
        self.index: Optional["faiss.Index"] = None
        self.node_ids: List[str] = []
        self._loaded = False

    @property
    def loaded(self) -> bool:
        return self._loaded

    def _make_text(self, node: Dict[str, Any]) -> str:
        parts = []
        label = node.get("label", "")
        nid = node.get("id", "")
        ntype = node.get("type", "")
        project = node.get("project", "")
        source_file = node.get("source_file", "")

        if label and label != nid:
            parts.append(str(label))
        if ntype:
            parts.append(f"({ntype})")
        if project and project != "unknown":
            parts.append(f"in {project}")
        if source_file:
            parts.append(f"file: {source_file}")
        description = node.get("description", node.get("heuristicLabel", ""))
        if description:
            parts.append(f": {description}")
        return " ".join(parts)

    def load_model(self) -> None:
        if not FAISS_AVAILABLE:
            logger.warning("FAISS not available, skipping embedding model load")
            return
        self.model = SentenceTransformer(settings.embed_model)
        logger.info(f"Loaded embedding model: {settings.embed_model}")

    def build_index(self, nodes: List[Dict[str, Any]]) -> None:
        if not FAISS_AVAILABLE or not self.model:
            logger.warning("Cannot build index: FAISS or model not available")
            return

        texts = [self._make_text(n) for n in nodes]
        logger.info(f"Encoding {len(texts)} nodes...")
        embeddings = self.model.encode(texts, show_progress_bar=True, batch_size=256)
        embeddings = np.array(embeddings).astype("float32")

        self.index = faiss.IndexFlatIP(settings.embed_dim)
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        self.node_ids = [n.get("id", "") for n in nodes]
        self._loaded = True
        logger.info(f"Built FAISS index with {len(embeddings)} vectors")

    def search(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        if not self._loaded or not self.model:
            return []

        q_vec = self.model.encode([query], show_progress_bar=False).astype("float32")
        faiss.normalize_L2(q_vec)

        scores, indices = self.index.search(q_vec, min(k, len(self.node_ids)))
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.node_ids):
                continue
            results.append({
                "node_id": self.node_ids[idx],
                "score": float(score),
                "rank": len(results) + 1
            })
        return results[:k]

    def save_index(self, path: Optional[str] = None) -> None:
        if not self._loaded:
            return
        save_path = Path(path) if path else settings.data_dir
        save_path.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(save_path / "faiss.index"))
        with open(save_path / "node_ids.json", "w") as f:
            json.dump(self.node_ids, f)

    def load_index(self, path: Optional[str] = None) -> None:
        load_path = Path(path) if path else settings.data_dir
        index_path = load_path / "faiss.index"
        ids_path = load_path / "node_ids.json"
        if index_path.exists() and ids_path.exists():
            self.index = faiss.read_index(str(index_path))
            with open(ids_path, "r") as f:
                self.node_ids = json.load(f)
            self._loaded = True
            logger.info(f"Loaded FAISS index with {len(self.node_ids)} entries")


embeddings = EmbeddingService()