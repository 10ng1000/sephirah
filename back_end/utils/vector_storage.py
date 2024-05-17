from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from icecream import ic
from utils.embeddings import ZhipuEmbedding

FOLDER_PATH = 'data/faiss/'

class FaissVectorStore():
    def __init__(self, index: str, embeddings = ZhipuEmbedding()):
        self.embeddings = embeddings
        self.index = index
        if index == None:
            raise ValueError("index is needed.")
        try:
            self.db = FAISS.load_local(FOLDER_PATH + index, self.embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            print(e)
            self.db = None

    def search(self, query: str):
        docs = self.db.similarity_search(query)
        return docs
    
    def search_with_score(self, query: str):
        docs = self.db.similarity_search_with_score(query)
        return docs

    def delete(self):
        # todo 无法删除
        '''删除数据库中的所有数据'''
        if self.db == None:
            return
        uuids = [self.db.index_to_docstore_id[id] for id in self.db.index_to_docstore_id]
        if len(uuids) == 0:
            return
        self.db.delete(uuids)
        self.db.save_local(FOLDER_PATH + self.index)

        
    def load_document(self, doc_path : str, chunk_size: int = 200, chunk_overlap: int = 0, separator: str = '\n'):
        '''从文档中加载数据覆盖到数据库中，并保存到本地'''
        if doc_path == None:
            raise ValueError("doc_path is needed.")
        text_spliter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0, separator='\n')
        raw_doc = TextLoader(doc_path).load()
        #如果为空
        if raw_doc == None:
            return
        documents = text_spliter.split_documents(raw_doc)
        self.db = FAISS.from_documents(documents, self.embeddings)
        self.db.save_local(FOLDER_PATH + self.index)



if __name__ == '__main__':
    faiss = FaissVectorStore(index = 'test', embeddings = ZhipuEmbedding())
    faiss.load_document(doc_path = '../data/降膜机组调试要点说明书v5.0_V2.txt')
    query="机组调试前要干什么？"
    # query="今天天气怎么 样？"
    ic(faiss.search_with_score(query))
    faiss.delete()