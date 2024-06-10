# HuggingFace + JINA Embeddings + ChromaDB Model
import os
from urllib.parse import urlparse
import requests
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.storage.storage_context import StorageContext
import chromadb
from chromadb.config import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import (
		VectorStoreIndex,
		ServiceContext,
		get_response_synthesizer,
)

from WebisteDataQuery import GetWebsiteDataQueryEngine


print("Sustainability Chatbot is initialising....")

################# Website Data Processing Starts #################

query_engine_website = GetWebsiteDataQueryEngine()

################# Website Data Processing Ends #################

print("give 'q' to stop conversation")
question = str(input("User : "))
while question != "q":
    response = query_engine_website.query(f"""{question}""")
    print("AI : ", response.response)
    question = str(input("User : "))