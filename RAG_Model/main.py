# HuggingFace + JINA Embeddings + ChromaDB Model
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core import (
		VectorStoreIndex,
		ServiceContext,
		get_response_synthesizer,
)

from PDFdata import getDataFromPDF
from indexing import indexing_page
from promptTemplate import GetPromptTemplate

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
pdf_path= []
pdf_path.append("/Users/yash/susgpt/RAG_Model/National-Artificial-Intelligence-Research-and-Development-Strategic-Plan-2023-Update.pdf")
rag_docs = getDataFromPDF(pdf_path)
# print total length of the documents
len_docs = 0
for doc in rag_docs:
   len_docs += (len(doc.text))
print(f"Total length of the documents is {len_docs}")
print(rag_docs[0].text)

print("Sustainability Chatbot is initialising....")

# getting vector store configured
import chromadb.utils.embedding_functions as embedding_functions
jinaai_ef = embedding_functions.JinaEmbeddingFunction(
                api_key=jina_emb_api_key,
                model_name="jina-embeddings-v2-base-en"
            )

vector_store = indexing_page(jinaai_ef)

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

print("give 'q' to stop conversation")
question = str(input("User : "))
while question != "q":
    response = query_engine.query(f"""{question}""")
    print("AI : ", response.response)
    question = str(input("User : "))
