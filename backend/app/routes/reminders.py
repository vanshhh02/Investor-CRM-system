from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import SessionLocal
from app import models, schemas

router = APIRouter()


# -------- DB DEPENDENCY --------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------- REMINDER LOGIC --------
def generate_reminders(db: Session):
    leads = db.query(models.Lead).all()

    for lead in leads:
        last_interaction = (
            db.query(models.Interaction)
            .filter(models.Interaction.lead_id == lead.id)
            .order_by(models.Interaction.date.desc())
            .first()
        )

        # -------- SAFE DATE --------
        if last_interaction and last_interaction.date:
            days_since = (datetime.utcnow() - last_interaction.date).days
        if not last_interaction:
            message = f"No interaction yet with {lead.name}"
            priority = "Low"
            continue

        days_since = max(days_since, 10)

        # -------- THRESHOLD --------
        if lead.stage == "Interested":
            threshold = 3
        elif lead.stage == "Contacted":
            threshold = 7
        else:
            threshold = 14

        if days_since >= threshold:

            # -------- PRIORITY --------
            if lead.stage == "Interested":
                priority = "High"
            elif lead.stage == "Contacted":
                priority = "Medium"
            else:
                priority = "Low"

            # -------- DUPLICATE CHECK --------
            existing = (
                db.query(models.Reminder)
                .filter(models.Reminder.lead_id == lead.id)
                .order_by(models.Reminder.due_date.desc())
                .first()
            )

            if existing and existing.due_date:
                time_diff = datetime.utcnow() - existing.due_date
                if time_diff < timedelta(hours=24):
                    continue

            # -------- MESSAGE --------
            message = f"Follow up with {lead.name}, last contacted {days_since} days ago"

            # -------- CREATE REMINDER --------
            reminder = models.Reminder(
                lead_id=lead.id,
                message=message,
                due_date=datetime.utcnow(),
                priority=priority
            )

            db.add(reminder)

    db.commit()


# -------- ROUTES --------
@router.post("/generate")
def run_reminder_engine(db: Session = Depends(get_db)):
    generate_reminders(db)
    return {"message": "Reminders generated"}


@router.get("/", response_model=list[schemas.ReminderResponse])
def get_reminders(db: Session = Depends(get_db)):
    return db.query(models.Reminder).all()