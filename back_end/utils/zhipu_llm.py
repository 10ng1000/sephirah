from zhipuai import ZhipuAI
from icecream import ic
from langchain.llms.base import LLM 
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema.output import GenerationChunk
from langchain.embeddings.base import Embeddings
from typing import Optional, List, Any, Mapping, Iterator, Callable, Dict
from langchain_community.chat_message_histories import RedisChatMessageHistory, SQLChatMessageHistory
from langchain_core.messages import ChatMessage
from utils.memory import RedisMemory
import re
#import pretty_errors

#todo 以后改成secret
client = ZhipuAI(api_key="b1f62968c571a91d5cbf0deb26853e75.O8kJveyevNPTzpZo")

class ZhipuLLM(LLM):
    '''不带记忆功能的LLMS'''
    model: str = 'glm-4'

    @property
    def _llm_type(self) -> str:
        return 'zhipu-api'
    
    def _stream(  
            self,  
            prompt: str,  
            stop: Optional[List[str]] = None,  
            run_manager: Optional[CallbackManagerForLLMRun] = None,  
            **kwargs: Any,  
    ) -> Iterator[GenerationChunk]:  
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in response:  
            if chunk.choices[0].finish_reason == "stop":
                yield GenerationChunk(
                    text=''
                )
            else:
                yield GenerationChunk(
                    text=chunk.choices[0].delta.content
                )

    def _call(
        self,  
        prompt: str,  
        stop: Optional[List[str]] = None,  
        run_manager: Optional[CallbackManagerForLLMRun] = None,  
        **kwargs: Any,  
    ) -> str:
        if stop is not None:  
            raise ValueError("stop kwargs are not permitted.")  
        response = client.chat.completions.create( 
            model=self.model,  
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        r1 = re.sub(r'\\"', '"',content)
        r2 = r1.replace("\\n", "\n")
        r3 = r2.replace('"，', '",')
        return r3
    
    @property  
    def _identifying_params(self) -> Mapping[str, Any]:  
        """Get the identifying parameters."""  
        return {"model": self.model}  

class ZhipuLLMWithMemory(ZhipuLLM):
    '''带记忆功能的LLM，redis数据库存储记忆'''
    session_id: str = "default"
    memory: RedisMemory = None

    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id
        #todo 以后改成环境变量
        # self.history = RedisChatMessageHistory(session_id, url="redis://localhost:6379")
        self.memory = RedisMemory(session_id)

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        # history = [{"role": msg.role, "content": msg.content} for msg in self.history.messages]
        # ic(history + [{"role": "user", "content": prompt}])
        history = self.memory.get_history()
        response = client.chat.completions.create(
            model=self.model,
            messages=history + [{"role": "user", "content": prompt}],
            stream=True
        )
        content = ""
        for chunk in response:
            if chunk.choices[0].finish_reason == "stop":
                # self.history.add_message(ChatMessage(role="user", content=prompt))
                # self.history.add_message(ChatMessage(role="assistant", content=content))
                self.memory.add_message(role="user", content=prompt)
                self.memory.add_message(role="assistant", content=content)
                yield GenerationChunk(
                    text=''
                )
            else:
                content += chunk.choices[0].delta.content
                yield GenerationChunk(
                    text=chunk.choices[0].delta.content
                )
        

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        # history = [{"role": msg.role, "content": msg.content} for msg in self.history.messages]
        #ic(history + [{"role": "user", "content": prompt}])
        history = self.memory.get_history()
        response = client.chat.completions.create(
            model=self.model,
            messages=history + [{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        # self.history.add_message(ChatMessage(role="user", content=prompt))
        # self.history.add_message(ChatMessage(role="assistant", content=content))
        self.memory.add_message(role="user", content=prompt)
        return content

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": self.model}

# class ZhipuLLMWithMemoryAndRetrieval(ZhipuLLMWithMemory):


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



if __name__ == "__main__":
    ZhipuLLM = ZhipuLLMWithMemory(session_id="测试bot4")
    ic(ZhipuLLM.invoke("你好"))
    for chunk in ZhipuLLM.stream("你好，我上一句问了你什么"):
         print(chunk, end="", flush=True)
    ZhipuEmbedding = ZhipuEmbedding()
    ic(ZhipuEmbedding.embed_documents(["你好", "你好吗"]))
    ic(ZhipuEmbedding.embed_query("你好"))