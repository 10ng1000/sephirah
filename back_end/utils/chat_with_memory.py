from langchain_community.chat_message_histories import RedisChatMessageHistory
from zhipu_llm import ZhipuLLM
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

def chat_sse(question: str, session_id: str) :
    LLM = ZhipuLLM()

    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="history"),
            ("user", "{question}"),
        ]
    )

    chain = prompt | LLM

    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: RedisChatMessageHistory(session_id, url="redis://localhost:6379/0"),
        input_messages_key="question",
        history_messages_key="history",
    )

    return    chain_with_history.stream(
        {"question": question},
        config={"configurable": {"session_id": session_id}},
    )