from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app import models
from app.services.reminder_service import generate_reminders


def generate_reminders(db: Session):
    leads = db.query(models.Lead).all()

    for lead in leads:
        last_interaction = (
            db.query(models.Interaction)
            .filter(models.Interaction.lead_id == lead.id)
            .order_by(models.Interaction.date.desc())
            .first()
        )

        if last_interaction:
            days_since = (datetime.utcnow() - last_interaction.date).days
        if not last_interaction:
            message = f"No interaction yet with {lead.name}"
            priority = "Low"
            continue # no interaction yet

        # -------- SMART LOGIC --------
        if lead.stage == "Interested":
            threshold = 3
        elif lead.stage == "Contacted":
            threshold = 7
        else:
            threshold = 14

        if days_since >= threshold:
            message = f"Follow up with {lead.name}, last contacted {days_since} days ago"

            reminder = models.Reminder(
                lead_id=lead.id,
                message=message,
                due_date=datetime.utcnow()
            )

            db.add(reminder)

    db.commit()