# HuggingFace + JINA Embeddings + ChromaDB Model

import os
from urllib.parse import urlparse
import requests
import logging
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
from llama_index.core.readers import StringIterableReader
import regex as re
from io import BytesIO, StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from .WebisteDataQuery import GetWebsiteDataQueryEngine

import csv
from llama_index.core import PromptTemplate

pdf_names = []

def GetPromptTemplate():

    qa_prompt_tmpl = (
        " Context information is below. \n"
        "---------------------\n"
        "{context_str}\\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the query. Please be brief, concise, and complete.\n"
        f"The information is taken from a pdf and fetched to you!\n"
        "If the context information does not contain an answer to the query, "
        "respond with \"No information\".\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt = PromptTemplate(qa_prompt_tmpl)

    return qa_prompt


def getDataFromPDF(pdf_files):

    rag_docs = []
    for pdf_file in pdf_files:
        pdf_data = pdf_file.read()

        text_paras = []
        parser = PDFParser(BytesIO(pdf_data))
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        for page in PDFPage.create_pages(doc):
            output_string = StringIO()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            interpreter.process_page(page)
            page_text = output_string.getvalue()
            text_paras.extend(re.split(r'\n\s*\n', page_text))

        rag_docs_data = StringIterableReader().load_data(text_paras)
        rag_docs.extend(rag_docs_data)

    return rag_docs


def get_rag_docs():
    pdf_directory = 'RAG_Model/pdfs'
    pdf_paths = []
    for root, _, files in os.walk(pdf_directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_paths.append(os.path.join(root, file))

    if pdf_paths == []:
        rag_docs = []
    else:
        rag_docs = getDataFromPDF(pdf_paths)
    
    # return pdf name also
    global pdf_names
    pdf_names = [os.path.basename(pdf_path) for pdf_path in pdf_paths]
    return rag_docs, pdf_names

def initializeKnowledgeRepo(hf_inference_api_key, jina_emb_api_key, question, pdf_file):

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
    # Process the uploaded PDF file
    rag_docs = getDataFromPDF([pdf_file])
    pdf_name = pdf_file.name
    logger = logging.getLogger('django')
    logger.info("PDF Data Loaded Successfully")
    logger.info(f"Number of Documents: {len(rag_docs)}")
    

    # getting vector store configured
    import chromadb.utils.embedding_functions as embedding_functions
    jinaai_ef = embedding_functions.JinaEmbeddingFunction(
                    api_key=jina_emb_api_key,
                    model_name="jina-embeddings-v2-base-en"
                )

    db = chromadb.PersistentClient(path='RAG_Model/chromadb', settings=Settings())
    chroma_collection = db.get_or_create_collection("SusGPTpdf", embedding_function=jinaai_ef)
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

    logger.info("Data Indexed Successfully")

    # configure retriever
    retriever = VectorIndexRetriever(index=index, similarity_top_k=6)

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

    response = query_engine.query(f"""{question} The name of pdf added is {pdf_name}. Answer accordingly.""")
    
    return response.response



def knowledgeRepoChatbot( hf_inference_api_key, jina_emb_api_key, question ):

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

    # getting vector store configured
    import chromadb.utils.embedding_functions as embedding_functions
    jinaai_ef = embedding_functions.JinaEmbeddingFunction(
                    api_key=jina_emb_api_key,
                    model_name="jina-embeddings-v2-base-en"
                )

    db = chromadb.PersistentClient(path='RAG_Model/chromadb', settings=Settings())
    chroma_collection = db.get_or_create_collection("SusGPTpdf", embedding_function=jinaai_ef)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # set up the service and storage contexts
    service_context = ServiceContext.from_defaults(
        llm=mixtral_llm, embed_model=jina_embedding_model
    )

    # create an index
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store,service_context=service_context)
    logger = logging.getLogger('django')
    logger.info("Data Indexe Fetched Successfully")

    # configure retriever
    retriever = VectorIndexRetriever(index=index, similarity_top_k=6)

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
   
    response = query_engine.query(f"""{question} The name of pdf added is {pdf_names[0]}. Answer accordingly.""")
     
    return response.response