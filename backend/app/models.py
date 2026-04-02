from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime


def generate_uuid():
    return str(uuid.uuid4())


# ---------------- LEAD ----------------
class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    linkedin = Column(String)
    net_worth_tier = Column(String)
    interest_areas = Column(String)
    stage = Column(String, default="Cold")

    created_at = Column(DateTime, default=datetime.utcnow)

    interactions = relationship("Interaction", back_populates="lead")
    stage_history = relationship("StageHistory", back_populates="lead")


# ---------------- STAGE HISTORY ----------------
class StageHistory(Base):
    __tablename__ = "stage_history"

    id = Column(String, primary_key=True, default=generate_uuid)
    lead_id = Column(String, ForeignKey("leads.id"))
    from_stage = Column(String)
    to_stage = Column(String)
    changed_at = Column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="stage_history")


# ---------------- INTERACTION ----------------
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(String, primary_key=True, default=generate_uuid)
    lead_id = Column(String, ForeignKey("leads.id"))
    type = Column(String)
    notes = Column(String)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)

    lead = relationship("Lead", back_populates="interactions")


# ---------------- REMINDER ----------------
class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(String, primary_key=True, default=generate_uuid)
    lead_id = Column(String, ForeignKey("leads.id"))
    message = Column(String)
    due_date = Column(DateTime)
    is_completed = Column(String, default="False")
    priority = Column(String, default="Medium")

    lead = relationship("Lead")