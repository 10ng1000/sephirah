from langchain_core.messages import ChatMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory

class RedisMemory():
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.chat_message_history = RedisChatMessageHistory(session_id=session_id, url="redis://localhost:6379")
    
    def get_history(self) -> list:
        return [{"role": msg.role, "content": msg.content} for msg in self.chat_message_history.messages]
    
    def add_message(self, role: str, content: str) -> None:
        self.chat_message_history.add_message(ChatMessage(role=role, content=content))