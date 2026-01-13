from typing import Dict
from pydantic import BaseModel
class SearchState(BaseModel):
    search_query: str
    search_results: Dict[str,str]={}
    search_count: int = 0
    need_re_search: bool = False
    summary_draft: str = ""