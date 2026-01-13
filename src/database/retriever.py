from src.database.vector_store import VECTOR_STORE

def retrieve(query: str)->str:
    results= VECTOR_STORE.semantic_hybrid_search_with_score_and_rerank(
        query=query,
        k=3,
    )
    ctx=""
    for doc,_,_ in results:
        ctx+=f"""
    ---
    source: {doc.metadata['file_name']}
    ---
    content: 
    {doc.page_content}


        """  
    return ctx