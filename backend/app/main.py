from fastapi import FastAPI
from app.database import engine, Base
from app.routes import leads, interactions
from app.routes import reminders
from app.routes import reminders  
from app.routes import ai # ✅ correct import



# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Investor Outreach CRM")

# Register routes
app.include_router(leads.router, prefix="/leads", tags=["Leads"])
app.include_router(interactions.router, prefix="/interactions", tags=["Interactions"])

app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])