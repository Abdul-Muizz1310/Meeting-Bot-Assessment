from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

def get_vectorstore_from_transcript(transcript: str):
    docs = [Document(page_content=transcript)]
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore =  FAISS.from_documents(docs, embeddings)
    return vectorstore