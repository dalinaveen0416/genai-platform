import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


#Health Check Test

def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

#RAG Chat Test (Without Ingest)

def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={"question": "Test question"}
    )
    assert response.status_code == 200
    assert "answer" in response.json()

#Summarization Test

def test_summarize():
    response = client.post(
        "/summarize",
        json={"text": "Artificial Intelligence is transforming the world."}
    )
    assert response.status_code == 200
    assert "summary" in response.json()

#SQL Chat Test

def test_sql_chat():
    response = client.post(
        "/sql-chat",
        json={"question": "How many employees are there?"}
    )
    assert response.status_code == 200
    assert "result" in response.json()

#Agent Test (Math)

def test_agent_math():
    response = client.post(
        "/agent",
        json={"question": "What is 10 * 5?"}
    )
    assert response.status_code == 200
    assert "result" in response.json()

if __name__ == "__main__":
    pytest.main()