from typing import List
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage,ToolMessage 
from pydantic import BaseModel

class ChatState(BaseModel):
    query:str
    answer:str=''
    messages: List[SystemMessage|HumanMessage|AIMessage|ToolMessage]=[
        SystemMessage(content="""
        You are a helpful assistant.
        You try to answer user asked question.
        If the question comes under your general knowledge then give straight answer.
        In case the question sounds like being asked from internal or proprietary documentation or knowledge base,
        you can use tools to search for the answer to user's question.
        """)
    ]
    citations: List[str] = []