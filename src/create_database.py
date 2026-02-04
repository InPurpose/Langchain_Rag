import shutil
import getpass
import os
from dotenv import load_dotenv

from langchain_chroma import Chroma

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents(file_path:str):
    loader = TextLoader(file_path,encoding="utf8")

    # loader = TextLoader("data/books/alice.txt",encoding="utf8")
    documents = loader.load()

    # print(f"Type of Documents: {type(documents)}")
    # print(f"Type of Document in Documents: {type(documents[0])}")
    # print(f"Number of Documents: {len(documents)}")

    # print(f"Actual Data:\n{documents[0].page_content}\n")
    # print(f"Meta Data:\n{documents[0].metadata}\n")

    return documents

def chunks_splitter(file_path:str):
    documents = load_documents(file_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Documents: {len(documents)} into chunks {len(chunks)}")

    # document = chunks[10]
    # print("----------------------------------------------")
    # print(document.page_content)
    # print("----------------------------------------------")
    # print(document.metadata)

    
    return chunks

def save_to_chroma(chunks:list[Document]):

    CHROMA_PATH = "chroma"

    load_dotenv()


    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH) 

    if not os.getenv("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    db = Chroma.from_documents(
        chunks,embeddings,persist_directory=CHROMA_PATH
    )

    # db.persist()

    print(f"Save {len(chunks)} chunks to {CHROMA_PATH}.")


chunks = chunks_splitter("data/books/alice.txt")

save_to_chroma(chunks)