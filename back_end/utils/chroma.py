import os
import getpass
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from utils.zhipu_llm import ZhipuEmbedding
from icecream import ic
import pretty_errors

raw_doc = TextLoader('../data/降膜机组调试要点说明书v5.0_V2.txt').load()
text_spliter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0, separator='\n')
documents = text_spliter.split_documents(raw_doc)
embedding = ZhipuEmbedding()
#ic(documents)
db = Chroma.from_documents(documents, embedding)

query="用户设置参数包括哪些内容？"
docs = db.similarity_search(query)
ic(docs[0].page_content)