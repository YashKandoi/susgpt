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

from PDFdata import getDataFromPDF
from WebisteDataQuery import GetWebsiteDataQueryEngine

import csv
from llama_index.core import PromptTemplate

def GetPromptTemplate():

    companies=""
    with open("company_data.csv", "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            companies += f"Company: {row[1]}, "

    qa_prompt_tmpl = (
        " Context information is below. \n"
        "---------------------\n"
        "{context_str}\\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the query. Please be brief, concise, and complete.\n"
        f"The information is about one of these companies in the Sustainability Sector in India:  {companies}. Answer for these companies only!\n"
        "If the context information does not contain an answer to the query, "
        "respond with \"No information\".\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt = PromptTemplate(qa_prompt_tmpl)

    return qa_prompt

#get the API keys from .txt files
# Hugging Face API Key [Free]
hf_inference_api_key = open("hf_inference_api_key.txt", "r").read()
# JINA Embeddings API Key [Free]
jina_emb_api_key = open("jina_emb_api_key.txt", "r").read()

# Get prompt Template
qa_prompt = GetPromptTemplate()

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

# Can take several pdfs
pdf_directory = 'RAG_Model/pdfs'
pdf_path= []

pdf_paths = []
for root, _, files in os.walk(pdf_directory):
    for file in files:
        if file.endswith('.pdf'):
            pdf_paths.append(os.path.join(root, file))

if pdf_paths == []:
    rag_docs = []
else:
    rag_docs = getDataFromPDF(pdf_paths)

print("Sustainability Chatbot is initialising....")

# getting vector store configured
import chromadb.utils.embedding_functions as embedding_functions
jinaai_ef = embedding_functions.JinaEmbeddingFunction(
                api_key=jina_emb_api_key,
                model_name="jina-embeddings-v2-base-en"
            )

db = chromadb.PersistentClient(path='chromadb', settings=Settings())
chroma_collection = db.get_or_create_collection("SusGPT", embedding_function=jinaai_ef)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# set up the service and storage contexts
service_context = ServiceContext.from_defaults(
    llm=mixtral_llm, embed_model=jina_embedding_model
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# create an index

index = VectorStoreIndex.from_documents(
    rag_docs, storage_context=storage_context, service_context=service_context
)

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

################# Website Data Processing Starts #################

query_engine_website = GetWebsiteDataQueryEngine(hf_inference_api_key, jina_emb_api_key)

################# Website Data Processing Ends #################

print("give 'q' to stop conversation")
question = str(input("User : "))
while question != "q":
    response = query_engine.query(f"""{question}""")
    response2 = query_engine_website.query(f"""{question}""")
    final_query = response.response + response2.response
    final_response = query_engine.query(f"""{final_query} Summarise them for this question : {question}""")
    print("AI : ", final_response.response)
    question = str(input("User : "))