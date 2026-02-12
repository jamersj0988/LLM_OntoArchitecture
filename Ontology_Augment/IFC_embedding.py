import re
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def split_chunks(text: str) -> list[str]:
    pattern = re.compile(
        r"===== FILE START =====.*?===== FILE END =====",
        re.DOTALL
    )
    return [chunk.strip() for chunk in pattern.findall(text)]

with open("Building_Knowledge/IFC_Schema.txt", "r", encoding="utf-8") as f:
    schema = f.read()

chunks = split_chunks(schema)
schema_docs = [Document(page_content=chunk) for chunk in chunks]
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

db = FAISS.from_documents(
    documents=schema_docs,
    embedding=embeddings
)
db.save_local("IFC_CONCEPT")