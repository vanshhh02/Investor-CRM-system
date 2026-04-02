from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from app.database import engine, SessionLocal, Base
from app import models, schemas
import uuid
import datetime

# Create database tables
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

# ---------------- LEADS ---------------- #

@app.get("/leads", response_model=List[schemas.LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    leads = db.query(models.Lead).all()
    return leads

@app.post("/leads", response_model=schemas.LeadResponse)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.email == lead.email).first()
    if db_lead:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    interest_areas_str = ",".join(lead.interest_areas) if lead.interest_areas else ""
    
    new_lead = models.Lead(
        name=lead.name,
        email=lead.email,
        linkedin=lead.linkedin,
        net_worth_tier=lead.net_worth_tier,
        interest_areas=interest_areas_str,
        stage="Cold"
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

@app.put("/leads/{lead_id}/stage", response_model=schemas.LeadResponse)
def update_lead_stage(lead_id: str, stage_update: schemas.StageUpdate, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    old_stage = db_lead.stage
    db_lead.stage = stage_update.new_stage
    
    stage_history = models.StageHistory(
        lead_id=lead_id,
        from_stage=old_stage,
        to_stage=stage_update.new_stage
    )
    db.add(stage_history)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: str, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(db_lead)
    db.commit()
    return {"message": "Deleted"}

@app.get("/leads/{lead_id}", response_model=schemas.LeadResponse)
def get_lead(lead_id: str, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead


# ---------------- INTERACTIONS ---------------- #

@app.get("/interactions", response_model=List[schemas.InteractionResponse])
def get_interactions(lead_id: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Interaction)
    if lead_id:
        query = query.filter(models.Interaction.lead_id == lead_id)
    return query.order_by(models.Interaction.date.desc()).all()

@app.post("/interactions", response_model=schemas.InteractionResponse)
def add_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    new_int = models.Interaction(
        lead_id=interaction.lead_id,
        type=interaction.type,
        notes=interaction.notes,
        date=datetime.datetime.utcnow()
    )
    db.add(new_int)
    db.commit()
    db.refresh(new_int)
    return new_int


# ---------------- REMINDERS ---------------- #

@app.get("/reminders", response_model=List[schemas.ReminderResponse])
def get_reminders(db: Session = Depends(get_db)):
    return db.query(models.Reminder).all()

@app.post("/reminders/generate")
def generate_reminders(db: Session = Depends(get_db)):
    leads = db.query(models.Lead).all()
    created_count = 0
    now = datetime.datetime.utcnow()
    for lead in leads:
        last_interaction = db.query(models.Interaction).filter(models.Interaction.lead_id == lead.id).order_by(models.Interaction.date.desc()).first()
        
        days_since = 30
        if last_interaction:
            days_since = (now - last_interaction.date).days
        else:
            days_since = (now - lead.created_at).days

        if days_since >= 14:
            exists = db.query(models.Reminder).filter(
                models.Reminder.lead_id == lead.id,
                models.Reminder.is_completed == "False",
                models.Reminder.message.like(f"%{days_since}%")
            ).first()
            if not exists:
                new_reminder = models.Reminder(
                    lead_id=lead.id,
                    message=f"You haven't followed up with {lead.name} in {days_since} days.",
                    due_date=now + datetime.timedelta(days=1),
                    priority="High" if days_since > 30 else "Medium"
                )
                db.add(new_reminder)
                created_count += 1
    
    db.commit()
    return {"message": f"Generated {created_count} reminders"}

@app.put("/reminders/{reminder_id}/complete", response_model=schemas.ReminderResponse)
def complete_reminder(reminder_id: str, db: Session = Depends(get_db)):
    reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    reminder.is_completed = "True"
    db.commit()
    db.refresh(reminder)
    return reminder

# Include AI Router
from app.ai_services import ai_router
app.include_router(ai_router)