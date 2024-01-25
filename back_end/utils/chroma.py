from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from zhipu_llm import ZhipuEmbedding
from icecream import ic

# raw_doc = TextLoader('../data/降膜机组调试要点说明书v5.0_V2.txt').load()
# text_spliter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0, separator='\n')
# documents = text_spliter.split_documents(raw_doc)
# embedding = ZhipuEmbedding()
# #ic(documents)
# db = FAISS.from_documents(documents, embedding)
# query="用户设置参数包括哪些内容？"
# docs = db.similarity_search(query)

# ic(docs[0].page_content)

class Faiss():
    def __init__(self, doc_path):
        self.embedding = ZhipuEmbedding()
        self.text_spliter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0, separator='\n')
        self.raw_doc = TextLoader(doc_path).load()
        self.documents = self.text_spliter.split_documents(self.raw_doc)
        self.db = FAISS.from_documents(self.documents, self.embedding)

    def search(self, query: str) -> str:
        docs = self.db.similarity_search(query)
        return docs[0].page_content