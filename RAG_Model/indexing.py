import chromadb
from chromadb.config import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore

def indexing_page(jinaai_ef):

    db = chromadb.PersistentClient(path='chromadb', settings=Settings())
    chroma_collection = db.get_or_create_collection("NSTC", embedding_function=jinaai_ef)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    return vector_store