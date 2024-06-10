# HuggingFace + JINA Embeddings + ChromaDB Model

from urllib.parse import urlparse
import requests
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode
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
from promptTemplate import GetJobPromptTemplate

################# Website Data Processing Starts #################

#get the API keys from .txt files
# Hugging Face API Key [Free]
hf_inference_api_key = open("hf_inference_api_key.txt", "r").read()
# JINA Embeddings API Key [Free]
jina_emb_api_key = open("jina_emb_api_key.txt", "r").read()

# Get prompt Template
qa_prompt = GetJobPromptTemplate()

# Set up the models to be used
mixtral_llm = HuggingFaceInferenceAPI(
    model_name="mistralai/Mixtral-8x7B-Instruct-v0.1", 
    token=hf_inference_api_key
)

# Set up the embedding model
jina_embedding_model = JinaEmbedding(
    api_key=jina_emb_api_key,
    model="jina-embeddings-v2-base-en",
)

# ask user to select the role which they are looking for
# role = input("Enter the role you are looking for: ")
# startup = input("Yes / No")
# skills = input("Enter the skills you are looking for: ")

role = 'Product Manager'
skills = 'Python, SQL, Machine Learning'

job_prompt = f"What are the jobs in Climate Change Sector in India for {role} with skills: {skills}. Only companies in Climate Change sector."

question = "What jobs are suitable for me?"
response = requests.get(urlparse("https://s.jina.ai/" + job_prompt).geturl())

nodes=[]
splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
list = splitter.split_text(response.text)
for i in range(len(list)):
    node = TextNode(text=list[i])
    nodes.append(node)


print("Sustainability Chatbot is initialising....")

# getting vector store configured
import chromadb.utils.embedding_functions as embedding_functions
jinaai_ef = embedding_functions.JinaEmbeddingFunction(
                api_key=jina_emb_api_key,
                model_name="jina-embeddings-v2-base-en"
            )

db = chromadb.PersistentClient(path='chromadb', settings=Settings())
chroma_collection = db.get_or_create_collection("Matchmaking", embedding_function=jinaai_ef)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# set up the service and storage contexts
service_context = ServiceContext.from_defaults(
    llm=mixtral_llm, embed_model=jina_embedding_model
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# create an index
index = VectorStoreIndex(
    nodes, 
    storage_context=storage_context, 
    service_context=service_context
)

# loading the created index
# index = VectorStoreIndex.from_vector_store(vector_store=vector_store,service_context=service_context)

# configure retriever
retriever = VectorIndexRetriever(index=index, similarity_top_k=3)

# configure response synthesizer
response_synthesizer = get_response_synthesizer(
    service_context=service_context,
    text_qa_template=qa_prompt,
    response_mode="compact",
)

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)


################# Website Data Processing Ends #################

response = query_engine.query(f"""{job_prompt}+{question}""")
print("AI : ", response.response)
print('Thank You!')