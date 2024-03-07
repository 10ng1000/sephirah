from langchain.embeddings.base import Embeddings
from typing import Optional, List, Any, Mapping, Iterator, Callable, Dict
from zhipuai import ZhipuAI
from icecream import ic

client = ZhipuAI(api_key="b1f62968c571a91d5cbf0deb26853e75.O8kJveyevNPTzpZo")

class ZhipuEmbedding(Embeddings):
    model: str = 'embedding-2'

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = []
        for text in texts:
            response = client.embeddings.create(model=self.model, input=text)
            embeddings.append(response.data[0].embedding)
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        response = client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding
    
if __name__ == '__main__':
    ZhipuEmbedding = ZhipuEmbedding()
    ic(ZhipuEmbedding.embed_documents(["你好", "你好吗"]))
    ic(ZhipuEmbedding.embed_query("你好"))