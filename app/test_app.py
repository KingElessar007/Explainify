import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.ai_service import (
    generate_casual_response,
    generate_academic_response,
    polish_text,
    summarize_text,
    generate_both_summaries
)

client = TestClient(app)

# --- 1. Prompt Formatting Logic ---

def test_generate_casual_prompt_format():
    prompt = "What is AI?"
    result = generate_casual_response(prompt)
    assert isinstance(result, str)
    assert len(result) > 0

def test_generate_academic_prompt_format():
    prompt = "What is AI?"
    result = generate_academic_response(prompt)
    assert isinstance(result, str)
    assert len(result) > 0

# --- 2. AI Generation Logic (Mocked) ---

@patch('app.ai_service.generator')
def test_polish_text_mocked(mock_generator):
    mock_generator.return_value = [{'generated_text': 'Polished text.'}]
    result = polish_text("raw text")
    assert result == "Polished text."

@patch('app.ai_service.generator')
def test_summarize_text_mocked(mock_generator):
    mock_generator.return_value = [{'generated_text': 'Summary.'}]
    result = summarize_text("long text")
    assert result == "Summary."

# --- 3. API Route Validation ---

def test_generate_route_validation():
    # Missing user_id
    response = client.post("/generate", json={"query": "What is AI?"})
    assert response.status_code == 422  # Unprocessable Entity

    # Missing query
    response = client.post("/generate", json={"user_id": "test-user"})
    assert response.status_code == 422

def test_history_route_validation():
    # Missing user_id param
    response = client.get("/history")
    assert response.status_code == 422

# --- 4. Integration Test: Complete Flow (Mock AI) ---

@patch('app.main.generate_both_summaries')
def test_integration_generate_and_history(mock_generate):
    # Mock AI responses
    mock_generate.return_value = {
        "casual_summary": "Mock casual summary.",
        "formal_summary": "Mock academic summary."
    }
    user_id = "integration-test-user"
    query = "Explain the term A.I."
    # 1. Generate
    response = client.post("/generate", json={"user_id": user_id, "query": query})
    assert response.status_code == 200
    data = response.json()
    assert data["casual_summary"] == "Mock casual summary."
    assert data["formal_summary"] == "Mock academic summary."

    # 2. Check history (should include the entry)
    response = client.get("/history", params={"user_id": user_id})
    assert response.status_code == 200
    history = response.json()
    assert any(item["query"] == query for item in history)
    assert any(item["casual_response"] == "Mock casual summary." for item in history)
    assert any(item["formal_response"] == "Mock academic summary." or item.get("academic_response") == "Mock academic summary." for item in history)
