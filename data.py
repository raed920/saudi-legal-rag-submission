"""Build the local Chroma index from the included legal articles."""
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def main():
    root = Path(__file__).resolve().parent
    load_dotenv(root / ".env")
    records = json.loads((root / "data" / "legal_articles.json").read_text(encoding="utf-8"))
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    store = Chroma(
        collection_name="Saudi_law",
        embedding_function=embeddings,
        persist_directory=str(Path(os.getenv("LEGAL_DB_PATH", str(root / "legal_db")))),
    )
    for start in range(0, len(records), 500):
        batch = records[start:start + 500]
        store.add_texts(
            texts=[record["text"] for record in batch],
            metadatas=[record["metadata"] for record in batch],
            ids=[record["id"] for record in batch],
        )
        print(f"Indexed {min(start + 500, len(records))}/{len(records)} articles")


if __name__ == "__main__":
    main()
