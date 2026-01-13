from langchain_core.tools import tool
from pydantic import Field
from src.agent.search_agent.workflow import build_workflow
from src.agent.search_agent.state import SearchState
@tool
def search_query(query: str=Field(...,description="query asked by user")) -> str:
    """
    searches internal documentation and returns relevant results
    """
    search_agent=build_workflow()
    state=SearchState(search_query=query)
    final_state=search_agent.invoke(state)
    final_state_obj=SearchState(**final_state)
    return final_state_obj.summary_draft