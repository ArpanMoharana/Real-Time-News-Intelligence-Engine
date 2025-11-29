import os
import json
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss #Facebook AI Similarity Search – creates fast vector search index.
from pathlib import Path #modern & clean way to handle file paths.

PROJECT_ROOT = Path(__file__).resolve().parents[1] #.parents[1] = go one folder up → your project root (Real-Time News Intelligence Engine)
DATAFILE = PROJECT_ROOT/"data"/ "articles.json" #source file data
INDEX_DIR = PROJECT_ROOT/"models" / "faiss_index"
EMBED_MODEL = "all-MiniLM-L6-v2"

os.makedirs(INDEX_DIR, exist_ok=True) #If the folder doesn’t exist → create it.
                                       #If it exists → ignore (no error).

def load_articles(path):
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:                                  #Reads each line.Removes whitespace.Skip empty lines.
            line = line.strip()
            if not line:
                continue
            doc = json.loads(line) #Convert the JSON string → Python dictionary.
            docs.append({
                "title": doc.get("title", "")[:200], #Title is at most 200 characters
                "text": doc.get("text", "")[:2000], #Text is at most 2000 characters
                "url": doc.get("url", "") #URL stored as is
            })
    return docs

def build_index(docs, model_name=EMBED_MODEL):
    model = SentenceTransformer(model_name)
    texts = [d["title"] + ". " + d["text"] for d in docs] # d is for docs where it searches for They include context (text) and They include summary (title)
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    #save
    faiss.write_index(index, str(INDEX_DIR / "index.faiss"))
    np.save(str(INDEX_DIR/ "meta.npy"), np.array(docs, dtype=object), allow_pickle=True)
    print(f"Saced index with {len(docs)} documents to", INDEX_DIR)

if __name__ == "__main__":
    docs = load_articles(DATAFILE)
    if not docs:
        print("No documents found in ", DATAFILE)
    else:
        build_index(docs)