from src.agent.search_agent.state import SearchState
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Literal, cast
from langchain_openai import AzureChatOpenAI
from src.database.retriever import retrieve
from src.agent.search_agent.schema import ContextRelevancyJudgeReply
   



def search_node(state:SearchState)->SearchState:
    """
    search for the query and add the results to messages
    """
    search_respone=retrieve(state.search_query)
    state.search_results[state.search_query]=search_respone
    state.search_count+=1
    return state
    
def re_search_decider_node(state:SearchState)->SearchState:
    """
    checks relevancy of the results and returns structured output of
    {
        need_re_search: bool,
        query: str (optional) #re written query for searching again for more information
    }
    """
    llm=AzureChatOpenAI(azure_deployment="gpt-4o-mini").with_structured_output(ContextRelevancyJudgeReply)
    search_history_text=""
    for i, (query,ans) in enumerate(state.search_results.items()):
        search_history_text+=f"""
        ---
        Search query no.{i+1}:
        {query}

        context received:
        {ans}
        ---
        """
    
    messages=[
        SystemMessage(
            """
            You are an expert in judging whether the context extracted from search results are enough to answer user's question.
            No need to search again if all relevant data present
            If search results are not enough to answer user query then generate new search query so that more relevant information can be searched.
            """
        ),
        HumanMessage(
            f"""
            User query (starting search query):
            {state.search_query}
            ===
            {search_history_text}
            """
        )
    ]
    response=llm.invoke(messages)
    structured_response=cast(ContextRelevancyJudgeReply,response)
    state.search_query=structured_response.query
    state.need_re_search=structured_response.need_re_search
    return state

def re_search_router(state:SearchState)->Literal["summarizer","search"]:
    if state.need_re_search and state.search_count <3:
        return "search"
    return "summarizer"
def summarizer_node(state:SearchState)->SearchState:
    """
    summarizes the findings (conversation style) into draft of relevant information
    """
    llm=AzureChatOpenAI(azure_deployment="gpt-4o-mini")
    search_history_text=""
    for i, (query,ans) in enumerate(state.search_results.items()):
        search_history_text+=f"""
        ---
        Search query no.{i+1}:
        {query}

        context received:
        {ans}
        ---
        """
    
    messages=[
        SystemMessage(
            """
            You are an expert in drafting descriptive summary all the relevant search results given in the search history.
            You only write the draft based on the user query (generally the first search query)
            Your description should contain relevant answer to that given user query,
            if the search results do not contain any relevant information then just tell that no relevant information available
            If relevant information is available, mention all the file names from which those informations are found.
            Strictly maintain exact file names as citation.
            Do not made up answer if no relevant information there.
            """
        ),
        HumanMessage(
            f"""
            User query (starting search query):
            {state.search_query}
            ===
            {search_history_text}
            """
        )
    ]
    response=llm.invoke(messages)
    if isinstance(response.content, str):
        state.summary_draft=response.content
    return state
