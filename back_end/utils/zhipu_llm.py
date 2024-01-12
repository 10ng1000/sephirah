import zhipuai
from icecream import ic
from langchain.llms.base import LLM 
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema.output import GenerationChunk
from langchain.embeddings.base import Embeddings
from typing import Optional, List, Any, Mapping, Iterator, Callable
from http import HTTPStatus  
import re
import json
#import pretty_errors

zhipuai.api_key = "b1f62968c571a91d5cbf0deb26853e75.O8kJveyevNPTzpZo"

class ZhipuLLM(LLM):
    model: str = 'chatglm_turbo'

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
        response = zhipuai.model_api.sse_invoke(
            model=self.model,  
            prompt=prompt
        )
        for event in response.events():  
            if event.event == "add":
                yield GenerationChunk(
                    text=event.data
                )
            elif event.event == "finish":
                yield GenerationChunk(
                    text='\n',
                    #generation_info=event.meta
                )
            else:  
                yield GenerationChunk(  
                    text=f"响应失败,失败信息为: {event.event}",
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
        response = zhipuai.model_api.invoke(  
            model=self.model,  
            prompt=prompt  
        )
        if response['code'] != HTTPStatus.OK:  
            raise RuntimeError(  
                f"Zhipu API returned an error: {response['code']} {response['msg']}"  
            )
        content = response['data']['choices'][0]['content']
        r1 = re.sub(r'\\"', '"',content)
        r2 = r1.replace("\\n", "\n")
        r3 = r2.replace('"，', '",')
        return r3
    
    @property  
    def _identifying_params(self) -> Mapping[str, Any]:  
        """Get the identifying parameters."""  
        return {"model": self.model}  

    def get_response(self, messages):
        return zhipuai.model_api.invoke(model=self.model, prompt=messages)

class ZhipuEmbedding(Embeddings):
    model: str = 'text_embedding'

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = []
        for text in texts:
            response = zhipuai.model_api.invoke(model=self.model, prompt=text)
            if response['code'] != HTTPStatus.OK:  
                raise RuntimeError(  
                    f"Zhipu API returned an error: {response['code']} {response['msg']}"  
                )
            embeddings.append(response['data']['embedding'])
        if not isinstance(embeddings, list):
            return embeddings.tolist()
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        response = zhipuai.model_api.invoke(model=self.model, prompt=text)
        if response['code'] != HTTPStatus.OK:  
            raise RuntimeError(  
                f"Zhipu API returned an error: {response['code']} {response['msg']}"  
            )
        return response['data']['embedding']

# 测试
if __name__ == "__main__":
    ZhipuLLM = ZhipuLLM()
    # ic(Zhipu.invoke("你好"))
    for chunk in ZhipuLLM.stream("你好"):
        print(chunk, end="", flush=True)
    ZhipuEmbedding = ZhipuEmbedding()
    ic(ZhipuEmbedding.embed_documents(["你好", "你好吗"]))
    ic(ZhipuEmbedding.embed_query("你好"))