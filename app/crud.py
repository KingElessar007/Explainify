from app.models import Prompt

def create_prompt(db, user_id: str, query: str, casual_response: str, formal_response: str):
    prompt = Prompt(
        user_id=user_id,
        query=query,
        casual_response=casual_response,
        formal_response=formal_response
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt

def get_history(db, user_id: str):
    return db.query(Prompt).filter(Prompt.user_id == user_id).order_by(Prompt.created_at.desc()).all()
