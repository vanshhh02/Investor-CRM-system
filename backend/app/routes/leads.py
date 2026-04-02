from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from fastapi import HTTPException

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------- CREATE LEAD --------
@router.post("/", response_model=schemas.LeadResponse)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):

    # 🔍 CHECK IF EMAIL EXISTS
    existing = db.query(models.Lead).filter(models.Lead.email == lead.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Lead with this email already exists")

    db_lead = models.Lead(
        name=lead.name,
        email=lead.email,
        linkedin=lead.linkedin,
        net_worth_tier=lead.net_worth_tier,
        interest_areas=",".join(lead.interest_areas or [])
    )

    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    return db_lead


# -------- GET ALL LEADS --------
@router.get("/", response_model=list[schemas.LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).all()


# -------- UPDATE STAGE --------
@router.patch("/{lead_id}/stage")
def update_stage(lead_id: str, data: schemas.StageUpdate, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    old_stage = lead.stage
    new_stage = data.new_stage

    # Update stage
    lead.stage = new_stage

    # Save history
    history = models.StageHistory(
        lead_id=lead_id,
        from_stage=old_stage,
        to_stage=new_stage
    )

    db.add(history)
    db.commit()

    return {"message": "Stage updated"}