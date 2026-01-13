from pydantic import BaseModel, Field
from typing import List

class Answer(BaseModel):
    reply:str=Field(default='',description="Reply to user query")
    citations:List[str]=Field(default=[],description="list of local file names if the context have mention of any relevant files")