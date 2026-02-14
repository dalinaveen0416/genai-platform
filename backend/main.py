from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os
import logging

import os ,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.rag_pipeline import RAGService
from backend.summarizer import Summarizer
from backend.sql_chat import SQLChat
from backend.agent_tools import AgentService

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)



UPLOAD_DIR = "data/uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Groq GenAI Platform")

rag = RAGService()
summarizer = Summarizer()
sql_chat = SQLChat()
agent = AgentService()


class ChatRequest(BaseModel):
    question: str


class TextRequest(BaseModel):
    text: str


@app.get("/")
def health():
    return {"status": "Groq GenAI API running"}


@app.post("/ingest")
def ingest(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        message = rag.ingest(file_path)

        return {"message": message}
    except Exception as e:
        logger.error(f"Ingest error: {e}")
        return {"error": str(e)}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        answer = rag.query(request.question)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {"error": str(e)}


@app.post("/summarize")
def summarize(request: TextRequest):
    try:
        summary = summarizer.summarize(request.text)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Summarize error: {e}")
        return {"error": str(e)}


@app.post("/sql-chat")
def sql_query(request: ChatRequest):
    try:
        result = sql_chat.ask(request.question)
        return {"result": result}
    except Exception as e:
        logger.error(f"SQL chat error: {e}")
        return {"error": str(e)}


@app.post("/agent")
def run_agent(request: ChatRequest):
    try:
        result = agent.run(request.question)
        return {"result": result}
    except Exception as e:
        logger.error(f"Agent error: {e}")
        return {"error": str(e)}
