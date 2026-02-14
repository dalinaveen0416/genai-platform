## GenAI Platform – RAG, SQL Chat & Agent (Groq Powered)

This project is my end-to-end Generative AI platform built using FastAPI, Groq LLMs, LangChain, FAISS, and SQLite.

The goal was simple — instead of building isolated demos, I wanted one clean system that supports:

1.Document-based Q&A (RAG)
2.Text summarization
3.Natural language to SQL
4.Agent-based reasoning (math & logic)

API-first architecture (production ready)

Everything runs through APIs, so it’s easy to deploy and integrate.

## What This Project Actually Does

This not just a chatbot
It’s a modular GenAI backend where:
* You upload a PDF -> it builds embeddings -> stores in FAISS -> answers questions from document.

* You ask a SQL question -> it generates query -> executes safely -> returns results.

* You give a reasoning problem -> agent decides how to solve it.

* You send text -> it summarizes clearly using Groq LLM.

All of this is exposed through FastAPI endpoints.

# Tech Stack
Backend

FastAPI
Python 3.10
LangChain (modular version)
Groq API (Llama 3.1 models)

Vector Store -> FAISS

Embeddings -> Sentence Transformers (all-MiniLM-L6-v2)

Database -> SQLite (for SQL chat module)

Testing -> Pytest


## Run this procject

step 1: create venv

step 2: pip install -r requirements.txt

next get your groq api key past it in .env file

step 3:first run the backedn by using this cammand 



command : uvicorn backend.main:app --reload

step 4: run ui.py using streamlit run frontend/app.py

and check it ...
...................................

# Eval :-

Rag_chat eval :

Final Accuracy: 8/9
Accuracy Percentage: 88.89%

