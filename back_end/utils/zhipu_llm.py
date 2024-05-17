from zhipuai import ZhipuAI
from icecream import ic
from langchain.llms.base import LLM 
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema.output import GenerationChunk
from typing import Optional, List, Any, Mapping, Iterator, Callable, Dict
from utils.memory import RedisMemory
import json
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
            stream=True,
            tools=[{
                "type": "web_search",
                "web_search": {
	                "enable": False
	            }
            }],
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
            stream=True,
            tools=[{
                "type": "web_search",
                "web_search": {
	                "enable": False
	            }
            }],
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

class ZhipuLLMWithRetrieval(ZhipuLLM):
    similar_docs: List[str] = []
    #用来存储历史记录，实际上不发送
    memory: RedisMemory = None

    def __init__(self, docs: List[str], session_id: str, k = 3):
        super().__init__()
        self.similar_docs = docs[:k]
        self.memory = RedisMemory(session_id)

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        new_prompt = f'''
            从文档
            """
            {self.similar_docs}
            """
            中找问题
            """
            {prompt}
            """
            的答案，找到答案就仅使用文档语句回答问题，找不到答案就用自身知识回答并且告诉用户该信息不是来自文档。
            不要复述问题，直接开始回答
        '''
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": new_prompt}],
            stream=True,
            tools=[{
                "type": "web_search",
                "web_search": {
	                "enable": False
	            }
            }],
        )
        history = self.memory.get_history()
        content = ""
        for chunk in response:
            if chunk.choices[0].finish_reason == "stop":
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
        new_prompt = f'''
            从文档
            """
            {self.similar_docs}
            """
            中找问题
            """
            {prompt}
            """
            的答案，找到答案就仅使用文档语句回答问题，找不到答案就用自身知识回答并且告诉用户该信息不是来自文档。
            不要复述问题，直接开始回答
        '''
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": new_prompt}],
        )
        content = response.choices[0].message.content
        return content

class ZhipuLLMWithMemoryWebSearch(ZhipuLLMWithMemory):
    def __init__(self, session_id: str):
        super().__init__(session_id=session_id)

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
            tools=[{
                "type": "web_search",
                "web_search": {
	                "enable": True, # 禁用：False，启用：True，默认为 True。
                    "search_result": True
	            }
            }],
            stream=True
        )
        content = ""
        for chunk in response:
            if chunk.choices[0].finish_reason == "stop":
                # self.history.add_message(ChatMessage(role="user", content=prompt))
                # self.history.add_message(ChatMessage(role="assistant", content=content))
                self.memory.add_message(role="user", content=prompt)
                self.memory.add_message(role="assistant", content=content)
                if (hasattr(chunk, 'web_search')):
                    yield GenerationChunk(
                        text=str(chunk.web_search)
                    )
                else:
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
            tools=[{
                "type": "web_search",
                "web_search": {
	                "enable": True,
                    "search_result": True # 禁用：False，启用：True，默认为 True。
	            }
            }],
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

class ZhipuLLMWithWebSearch(ZhipuLLMWithMemory):
    def __init__(self, session_id: str):
        super().__init__(session_id=session_id)

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        # history = [{"role": msg.role, "content": msg.content} for msg in self.history.messages]
        # ic(history + [{"role": "user", "content": prompt}])
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            tools=[{
                "type": "web_search",
                "web_search": {
	                "enable": True, # 禁用：False，启用：True，默认为 True。
                    "search_result": True
	            }
            }],
            stream=True
        )
        content = ""
        for chunk in response:
            if chunk.choices[0].finish_reason == "stop":
                # self.history.add_message(ChatMessage(role="user", content=prompt))
                # self.history.add_message(ChatMessage(role="assistant", content=content))
                self.memory.add_message(role="user", content=prompt)
                self.memory.add_message(role="assistant", content=content)
                #如果chunk有web_search属性，就返回web_search的内容，否则返回空
                if (hasattr(chunk, 'web_search')):
                    yield GenerationChunk(
                        text=str(chunk.web_search)
                    )
                else:
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
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            tools=[{
                "type": "web_search",
                "web_search": {
	                "enable": True,
                    "search_result": True # 禁用：False，启用：True，默认为 True。
	            }
            }],
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

if __name__ == "__main__":
    ZhipuLLM = ZhipuLLMWithMemory(session_id="测试bot4")
    ic(ZhipuLLM.invoke("你好"))
    for chunk in ZhipuLLM.stream("你好，我上一句问了你什么"):
         print(chunk, end="", flush=True)