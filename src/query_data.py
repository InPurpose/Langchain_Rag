import argparse

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
import os
import dotenv
from typing import List 
from langchain_chroma import Chroma

from dataclasses import dataclass
from src.logging_config import setup_logging
import logging

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

@dataclass
class QueryResponse:
    query_text:str
    response_text:str
    sources:List[str]




def prepare_db():  

    embedding_function = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    return db

def get_question():

    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    return query_text

def get_prompt(query_text):
    db = prepare_db()

    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    if len(results) == 0 or results[0][1] < 0.6:
        print(f"Best match score : {results[0][1]}")
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    # print(context_text)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # print(prompt)
    return prompt

def generate_response(prompt):
    model = ChatGoogleGenerativeAI(model="gemini-3-pro-preview")
    response = model.invoke(prompt)
    return response

def init():
    dotenv.load_dotenv()


    if not os.getenv("GOOGLE_API_KEY"):
        logger = logging.getLogger(__name__)

        logger.error("Environment variable GOOGLE_API_KEY is not set")
        raise ValueError("GOOGLE_API_KEY is required but not provided")


def query_rag(query_text: str):
    init()
    db = prepare_db()

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)
    scores = []

    # for i in results:
    #     scores.append(results[0][1])
    # print(f"Result scores : {scores}")

    # if len(results) == 0 or results[0][1] < 0.6:
    #     print(f"Best match score : {results[0][1]}")
    #     print(f"Unable to find matching results.")
    #     return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Create prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    # Generate answer of the question from model
    model = ChatGoogleGenerativeAI(model="gemini-3-pro-preview")
    response = model.invoke(prompt)
    response_text = response.text

    # Record source of response
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(f"Response: {response_text}\nSources: {sources}")

    return QueryResponse(
        query_text=query_text, response_text=response_text, sources=sources
    )


    
if __name__ == "__main__":
    query_rag("What happens at the Mad Hatter's tea party?")