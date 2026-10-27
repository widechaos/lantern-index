"""Semantic retrieval for an original fictional station archive."""
from pathlib import Path
import json, os
import numpy as np
from sentence_transformers import SentenceTransformer
ROOT = Path(__file__).resolve().parent
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
THRESHOLD = 0.28
REQUIRED = {"light", "letter", "bell"}
ENDING = "The bell cannot explain the light. Mara's letter can explain why she kept it. The archive never proves a ghost exists: it leaves a promise burning after the railway is gone. The final visitor's fresh letter is the part I cannot settle."

def load_records(path=ROOT / "archive.json"):
    records = json.loads(Path(path).read_text())
    if len({r["id"] for r in records}) != len(records):
        raise ValueError("Duplicate archive IDs")
    for r in records:
        if not all(isinstance(r.get(k), str) and r[k] for k in ("id", "title", "date", "text", "thread")):
            raise ValueError("Malformed archive record")
    return records

class Archive:
    def __init__(self):
        self.records = load_records()
        self.model = SentenceTransformer(MODEL, revision=REVISION, device="cpu", local_files_only=True)
        texts = [r["title"] + ". " + r["text"] for r in self.records]
        self.vectors = self.model.encode(texts, normalize_embeddings=True)

    def search(self, query):
        if not isinstance(query, str) or not query.strip() or len(query) > 512:
            raise ValueError("Enter a question of 1–512 characters.")
        if any(ord(c) < 32 and c not in "\n\t" for c in query):
            raise ValueError("Control characters are not supported.")
        if len(self.model.tokenizer.encode(query, add_special_tokens=True)) > 256:
            raise ValueError("Question exceeds the model token limit; shorten it.")
        vec = self.model.encode([query], normalize_embeddings=True)[0]
        scores = self.vectors @ vec
        ranked = sorted(range(len(scores)), key=lambda i: (-float(scores[i]), self.records[i]["id"]))[:3]
        hits = [{**self.records[i], "score": round(float(scores[i]), 4)} for i in ranked if scores[i] >= THRESHOLD]
        return {"query": query, "hits": hits, "abstained": not bool(hits), "threshold": THRESHOLD}

    def ending(self, ids):
        if not isinstance(ids, list) or len(ids) > len(self.records) or any(not isinstance(x, str) for x in ids):
            raise ValueError("Invalid evidence selection")
        known = {r["id"] for r in self.records}
        if not set(ids) <= known:
            raise ValueError("Unknown evidence ID")
        if not REQUIRED <= set(ids):
            return {"unlocked": False, "text": "Find and pin the bell register, the keeper's lamp and the unsent letter. Reading a related note is not the same as finding the source."}
        return {"unlocked": True, "text": ENDING, "sources": [r for r in self.records if r["id"] in REQUIRED]}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    args = parser.parse_args()
    print(json.dumps(Archive().search(args.question), indent=2))
