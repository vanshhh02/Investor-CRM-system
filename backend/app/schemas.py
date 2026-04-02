from pydantic import BaseModel, Field
from typing import Optional, List ,Literal
from datetime import datetime


# -------- LEAD --------
class LeadCreate(BaseModel):
    name: str = Field(..., description="Full name of the investor", example="Alice Johnson")
    email: str = Field(..., description="Investor email address", example="alice@gmail.com")
    linkedin: Optional[str] = Field(
        None,
        description="LinkedIn profile URL",
        example="https://linkedin.com/in/alice"
    )
    net_worth_tier: Optional[str] = Field(
        None,
        description="Investor net worth category (e.g., High, Medium, Low)",
        example="High"
    )
    interest_areas: Optional[List[str]] = Field(
        None,
        description="List of sectors the investor is interested in",
        example=["AI", "Fintech"]
    )


class LeadResponse(BaseModel):
    id: str
    name: str
    email: str
    linkedin: Optional[str] = None
    net_worth_tier: Optional[str] = None
    interest_areas: Optional[str] = None
    stage: str

    model_config = {
        "from_attributes": True
    }


# -------- STAGE --------
class StageUpdate(BaseModel):
    new_stage: Literal["Cold", "Contacted", "Interested", "Committed"]


# -------- INTERACTION --------
class InteractionCreate(BaseModel):
    lead_id: str = Field(
        ...,
        description="ID of the lead you are interacting with",
        example="uuid-of-lead"
    )
    type: str = Field(
        ...,
        description="Type of interaction",
        example="call"
    )
    notes: str = Field(
        ...,
        description="Notes from the interaction",
        example="Investor showed strong interest in AI startup"
    )


class InteractionResponse(BaseModel):
    id: str
    lead_id: str
    type: str
    notes: str
    date: datetime

    model_config = {
        "from_attributes": True
    }


# -------- REMINDER --------
class ReminderResponse(BaseModel):
    id: str
    lead_id: str
    message: str
    due_date: datetime
    is_completed: str
    priority: str

    model_config = {
        "from_attributes": True
    }