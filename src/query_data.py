import argparse

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
import os
import dotenv
import getpass 
from langchain_chroma import Chroma

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    init()
    prompt = get_prompt()
    response = generate_response(prompt)
    print(response)



def get_question():

    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    return query_text

def prepare_db():  

    embedding_function = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    return db

def get_prompt():
    db = prepare_db()
    query_text = get_question()

    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    DEBUG = False
    if DEBUG:
        print("=== DEBUG: 所有结果 ===")
        for i, (doc, score) in enumerate(results):
            print(f"  {i+1}: {score:.3f} | {doc.page_content[:100]}...")
        print(f"最佳: {results[1] if results else '无'}")

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

def init():
    dotenv.load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
      raise ValueError(" Please provide GEMINI_API_KEY as an environment variable")
    
    # if not os.getenv("GOOGLE_API_KEY"):
    #     os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")

def generate_response(prompt):
    model = ChatGoogleGenerativeAI(model="gemini-3-pro-preview")
    answer = model.invoke(prompt)
    return answer.text

if __name__ == "__main__":
    main()