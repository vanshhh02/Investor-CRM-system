from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
import requests
import json

import os

ai_router = APIRouter(prefix="/ai", tags=["ai"])

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_API_URL = f"{OLLAMA_HOST}/api/generate"
DEFAULT_MODEL = "phi3"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def query_ollama(prompt: str) -> str:
    """Helper to query the local Ollama instance."""
    try:
        payload = {
            "model": DEFAULT_MODEL,
            "prompt": prompt,
            "stream": False
        }
        res = requests.post(OLLAMA_API_URL, json=payload, timeout=600)
        res.raise_for_status()
        return res.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        return f"[Ollama Error] Ensure Ollama is running and model '{DEFAULT_MODEL}' is pulled. Details: {e}"


@ai_router.get("/generate-email/{lead_id}")
def generate_email(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    prompt = f"""
    You are an AI assistant for an Investor CRM. Write a short, professional introductory email to an investor.
    Lead Name: {lead.name}
    Interest Areas: {lead.interest_areas}
    Net Worth Tier: {lead.net_worth_tier}
    Stage: {lead.stage}
    
    Write ONLY the email content. Include a subject line. Be concise and persuasive.
    """
    
    email_content = query_ollama(prompt)
    return {"email": email_content}

@ai_router.get("/summary/{lead_id}")
def summarize_interactions(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    interactions = db.query(models.Interaction).filter(models.Interaction.lead_id == lead_id).order_by(models.Interaction.date.desc()).all()
    count = len(interactions)
    
    if count == 0:
        return {"summary": "No interactions logged yet to summarize."}
        
    log_text = "\n".join([f"- {i.date.strftime('%Y-%m-%d')} ({i.type}): {i.notes}" for i in interactions])
    
    prompt = f"""
    Summarize the following interaction history with investor '{lead.name}' ({count} total interactions).
    History:
    {log_text}
    
    Provide a brief, high-level summary of the relationship status and key takeaways.
    """
    
    summary = query_ollama(prompt)
    return {"summary": summary}

@ai_router.get("/score/{lead_id}")
def get_lead_score(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    interactions = db.query(models.Interaction).filter(models.Interaction.lead_id == lead_id).all()
    log_text = "\n".join([f"- {i.type}: {i.notes}" for i in interactions])
        
    prompt = f"""
    Evaluate the following investor and provide a Lead Score from 1 to 100 based on their likelihood to commit capital.
    Name: {lead.name}
    Tier: {lead.net_worth_tier}
    Current Stage: {lead.stage}
    Interactions: {log_text}
    
    Rules: Reply ONLY with an integer number between 1 and 100. Do not write anything else.
    """
    
    response = query_ollama(prompt)
    
    score_val = 50
    try:
        score_val = int("".join(filter(str.isdigit, response)))
        score_val = max(1, min(100, score_val))
    except:
        pass # fallback
        
    return {"score": score_val}

@ai_router.get("/next-action/{lead_id}")
def get_next_action(lead_id: str, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    interactions = db.query(models.Interaction).filter(models.Interaction.lead_id == lead_id).all()
    log_text = "\n".join([f"- {i.type}: {i.notes}" for i in interactions])
        
    prompt = f"""
    Based on the following investor lead profile and history, what is the single most effective NEXT ACTION the team should take right now?
    Name: {lead.name}
    Stage: {lead.stage}
    History: {log_text}
    
    Give ONLY the suggested action in 1 or 2 concise sentences. Be strategic.
    """
    
    action = query_ollama(prompt)
    return {"next_action": action}
