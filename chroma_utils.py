# chroma_utils.py

import chromadb
from gemini_utils import embed_texts_gemini

class GeminiEmbeddingFunction:
    def __call__(self, docs):
        return embed_texts_gemini(docs)

chroma_client = chromadb.PersistentClient(path="./chroma_store")

def get_or_create_collection(name: str):
    return chroma_client.get_or_create_collection(
        name=name,
        embedding_function=GeminiEmbeddingFunction()
    )

def add_documents(db, docs, ids, metas):
    db.add(
        documents=docs,
        ids=ids,
        metadatas=metas
    )
