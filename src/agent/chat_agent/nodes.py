from src.agent.chat_agent.state import ChatState
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from src.agent.chat_agent.tools import search_query
from src.agent.chat_agent.schema import Answer
from langchain.agents import create_agent
from typing import cast

def agent_node(state: ChatState):
    """
    Answer user query using LLM, decide whether to use tools or answer directly.
    """
    llm=AzureChatOpenAI(azure_deployment="gpt-4o-mini")
    agent=create_agent(model=llm, tools=[search_query], response_format=Answer)
    state.messages.append(HumanMessage(content=state.query))
    response=agent.invoke({'messages':[*state.messages]})
    state.messages=[*response["messages"]]
    print(response["structured_response"])
    structured_response=cast(Answer,response["structured_response"])#Answer(**response["structured_response"])
    state.answer=structured_response.reply
    state.citations=[*structured_response.citations]
    return state
