import chromadb
from sentence_transformers import SentenceTransformer


client = chromadb.PersistentClient(path="./app/vector_db/chroma_db")

collection = client.get_or_create_collection(name="information")

model = SentenceTransformer("all-MiniLM-L6-v2")


def save_text_to_vector_db(text: str, filename: str):

    embedding = model.encode(text).tolist()

    collection.add(
        ids=[filename],
        documents=[text],
        embeddings=[embedding],
        metadatas=[{"filename": filename}],
    )

    return True
