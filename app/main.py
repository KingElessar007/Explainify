from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine, Base
from .models import Prompt
from .crud import create_prompt, get_history
from .ai_service import generate_both_summaries

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GenerateRequest(BaseModel):
    user_id: str
    query: str

class GenerateResponse(BaseModel):
    casual_summary: str
    formal_summary: str

@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest, db: Session = Depends(get_db)):
    summaries = generate_both_summaries(req.query)
    # Saving both summaries in one row
    create_prompt(db, req.user_id, req.query, summaries["casual_summary"], summaries["formal_summary"])
    return summaries

@app.get("/history")
def history(user_id: str, db: Session = Depends(get_db)):
    prompts = get_history(db, user_id)
    return [
        {
            "id": str(p.id),
            "query": p.query,
            "casual_response": p.casual_response,
            "formal_response": p.formal_response,
            "created_at": p.created_at.isoformat()
        }
        for p in prompts
    ]
