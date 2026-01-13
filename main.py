from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from src.agent.chat_agent.workflow import build_workflow
from src.agent.chat_agent.schema import Answer
from src.agent.chat_agent.state import ChatState
from src.database.ingest import ingest_docs

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up: Ingesting documents...")
    try:
        ingest_docs()
    except Exception as e:
        print(f"⚠️ Warning: Ingestion failed (check configuration/data): {e}")
    yield
    print("🛑 Shutting down...")

app = FastAPI(lifespan=lifespan)
agent=build_workflow()

class AskRequest(BaseModel):
    query: str
    session_id: str = "default"

@app.post("/ask")
async def ask(request: AskRequest):  
    try:  
        inputs = ChatState(query=request.query)
        result = agent.invoke(inputs, config={"configurable": {"thread_id": request.session_id}})
        return {
            "answer": result.get("answer",""),
            "source": result.get("citations",[])
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
