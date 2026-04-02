from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from datetime import datetime
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_interaction(data: schemas.InteractionCreate, db: Session = Depends(get_db)):
    
    # ✅ Ensure lead exists
    lead = db.query(models.Lead).filter(models.Lead.id == data.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # ✅ Create correct interaction
    interaction = models.Interaction(
        id=str(uuid.uuid4()),
        lead_id=data.lead_id,   # 🔥 THIS IS CRITICAL
        type=data.type,
        notes=data.notes,
        date=datetime.utcnow()  # 🔥 FORCE DATE
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return interaction