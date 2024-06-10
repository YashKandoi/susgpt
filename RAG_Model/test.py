# HuggingFace + JINA Embeddings + ChromaDB Model
# this is not used right now, will be changed to add new website embedding to the index
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.core.node_parser import JSONNodeParser
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.schema import TextNode
from llama_index.core.storage.storage_context import StorageContext
import chromadb
from chromadb.config import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import (
		VectorStoreIndex,
		ServiceContext,
		get_response_synthesizer,
)

import logging
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


def GetWebsiteDataQueryEngine(hf_inference_api_key, jina_emb_api_key):

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


    # print("Sustainability Chatbot is initialising....")

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
    import requests

    website_list = requests.get("http://127.0.0.1:8000/websites/")
    website_list = website_list.json()
    nodes=[]
    for website in website_list:
        if website['company_name'] != "SusMafia":
            continue
        print(website['company_name'])
        website_url=website['url']
        website_details = website['output']
        splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
        list = splitter.split_text(website_details)
        for i in range(len(list)):
            node = TextNode(text=list[i], id=hash(website_url+str(i)))
            nodes.append(node)

    index = VectorStoreIndex(
        nodes, 
        storage_context=storage_context, 
        service_context=service_context
    )
    print("Data Indexed Successfully")
    
    
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

    return query_engine



    # print("give 'q' to stop conversation")
    # question = str(input("User : "))
    # while question != "q":
    #     response = query_engine.query(f"""{question}""")
    #     print("AI : ", response.response)
    #     question = str(input("User : "))

hf_inference_api_key= "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"
jina_emb_api_key = "jina_be82bcff2cf54442908d71556ea0312b4BmmwdjqsxbkR6oq1YmFafwNuSXY"

query_engine = GetWebsiteDataQueryEngine(hf_inference_api_key, jina_emb_api_key)