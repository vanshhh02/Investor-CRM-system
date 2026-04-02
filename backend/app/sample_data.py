from app.database import SessionLocal
from app import models

def seed_data():
    db = SessionLocal()

    if db.query(models.Lead).count() > 0:
        print("Data already exists")
        return

    leads = [
        models.Lead(name="Alice", email="alice@gmail.com", net_worth_tier="High", interest_areas="AI", stage="Interested"),
        models.Lead(name="Bob", email="bob@gmail.com", net_worth_tier="Medium", interest_areas="Fintech", stage="Contacted"),
        models.Lead(name="Charlie", email="charlie@gmail.com", net_worth_tier="Low", interest_areas="SaaS", stage="Cold"),
    ]

    for lead in leads:
        db.add(lead)

    db.commit()
    db.close()

    print("Sample data added")