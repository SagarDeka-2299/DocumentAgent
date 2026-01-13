from pydantic import BaseModel, Field

class ContextRelevancyJudgeReply(BaseModel):
    need_re_search: bool = Field(default=False, description="Whether a re-search is needed for more relevant information")
    query: str = Field(default='', description="Rewritten query for searching again for more information")