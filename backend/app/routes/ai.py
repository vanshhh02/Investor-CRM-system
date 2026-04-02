from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.services.ai_service import (
    generate_followup_email,
    summarize_interactions,
    score_lead
)
from datetime import datetime
from app.services.ai_service import next_best_action
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------- FOLLOW-UP EMAIL --------
@router.get("/generate-email/{lead_id}")
def generate_email(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()

    interactions = db.query(models.Interaction).filter(
        models.Interaction.lead_id == lead_id
    ).all()

    last_interaction = interactions[-1] if interactions else None

    email = generate_followup_email(lead, last_interaction)

    return {"email": email}


# -------- SUMMARY --------
@router.get("/summary/{lead_id}")
def get_summary(lead_id: str, db: Session = Depends(get_db)):
    interactions = db.query(models.Interaction).filter(
        models.Interaction.lead_id == lead_id
    ).all()

    summary = summarize_interactions(interactions)

    return {"summary": summary}


# -------- SCORE --------
@router.get("/score/{lead_id}")
def get_score(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()

    interactions = db.query(models.Interaction).filter(
        models.Interaction.lead_id == lead_id
    ).all()

    score = score_lead(lead, len(interactions))

    return {"score": score}


@router.get("/next-action/{lead_id}")
def get_next_action(lead_id: str, db: Session = Depends(get_db)):
    
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()

    if not lead:
        return {"error": "Lead not found"}

    interactions = db.query(models.Interaction).filter(
        models.Interaction.lead_id == lead_id
    ).order_by(models.Interaction.date.desc()).all()

    last_interaction = interactions[0] if interactions else None

    if last_interaction and last_interaction.date:
        days_since = (datetime.utcnow() - last_interaction.date).days
    else:
        days_since = 999

    action = next_best_action(lead, last_interaction, days_since)

    return {"next_action": action}