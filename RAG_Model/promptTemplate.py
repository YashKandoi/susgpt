import csv
from llama_index.core import PromptTemplate

def GetPromptTemplate():

    companies=""
    with open("../company_data.csv", "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            companies += f"Company: {row[1]}, "

    qa_prompt_tmpl = (
        f"The information is about one of these companies in the Sustainability Sector in India:  {companies}.Context information is below. \n"
        "---------------------\n"
        "{context_str}\\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the query. Please be brief, concise, and complete.\n"
        "If the context information does not contain an answer to the query, "
        "respond with \"No information\".\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt = PromptTemplate(qa_prompt_tmpl)

    return qa_prompt