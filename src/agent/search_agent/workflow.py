from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from src.agent.search_agent.state import SearchState
from src.agent.search_agent.nodes import search_node,re_search_decider_node,re_search_router,summarizer_node

def build_workflow():
    graph=StateGraph(SearchState)

    graph.add_node("search", search_node)
    graph.add_node("relevancy", re_search_decider_node)
    graph.add_node("summarizer", summarizer_node)

    graph.add_edge(START, "search")
    graph.add_edge("search", "relevancy")
    graph.add_conditional_edges("relevancy", re_search_router)
    graph.add_edge("summarizer", END)

    app=graph.compile(MemorySaver())
    return app