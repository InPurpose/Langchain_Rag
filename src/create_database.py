import shutil
import logging
import os
from dotenv import load_dotenv

from langchain_chroma import Chroma

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_PATH = "chroma"

def load_documents(file_path:str):
    loader = TextLoader(file_path,encoding="utf8")
    documents = loader.load()
    return documents

def chunks_splitter(documents):
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,  # Smaller, coherent chunks
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?"],
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Documents: {len(documents)} into chunks {len(chunks)}")    

    return chunks


def save_to_chroma(chunks:list[Document]):

    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH) 

    if not os.getenv("GOOGLE_API_KEY"):
      raise ValueError(" Please provide GEMINI_API_KEY as an environment variable")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    db = Chroma.from_documents(
        chunks,embeddings,persist_directory=CHROMA_PATH
    )

    # db.persist()

    print(f"Save {len(chunks)} chunks to {CHROMA_PATH}.")


def main():
    load_dotenv()
    documents = load_documents("data/books/alice.txt")
    chunks = chunks_splitter(documents)

    save_to_chroma(chunks)

if __name__ == '__main__':
    main()