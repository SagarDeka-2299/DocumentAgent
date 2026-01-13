from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from src.agent.chat_agent.state import ChatState
from src.agent.chat_agent.nodes import agent_node

def build_workflow():
    graph=StateGraph(ChatState)
    graph.add_node("agent",agent_node)
    graph.add_edge(START, "agent")
    graph.add_edge("agent",END)
    app=graph.compile(MemorySaver())
    return app