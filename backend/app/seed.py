"""Seed database with sample property, drop boxes, cashiers, tables if empty."""
from app.database import SessionLocal, init_db
from app import models


def seed_if_empty():
    init_db()
    db = SessionLocal()
    try:
        if db.query(models.Property).first() is not None:
            return  # already seeded
        # Property
        prop = models.Property(name="Demo Casino", code="DEMO")
        db.add(prop)
        db.commit()
        db.refresh(prop)
        pid = prop.id
        # Drop boxes (slot machines)
        for i in range(1, 6):
            db.add(models.DropBox(
                property_id=pid,
                machine_id=f"SLOT-{i:04d}",
                barcode=f"DB-{i:04d}",
                bank="A",
                expected_cents=100000 + i * 5000,  # $1000–$1200
            ))
        # Cashiers
        for name, eid in [("Alice Smith", "C001"), ("Bob Jones", "C002")]:
            db.add(models.Cashier(property_id=pid, name=name, employee_id=eid))
        # Tables
        for name, game in [("BJ-1", "blackjack"), ("BJ-2", "blackjack"), ("Roulette-1", "roulette")]:
            db.add(models.Table(property_id=pid, name=name, game_type=game, bank="Main"))
        db.commit()
        # Opening vault balance (one deposit)
        db.add(models.VaultTransaction(
            property_id=pid,
            type="deposit",
            amount_cents=10_000_000,  # $100k
        ))
        db.commit()
    finally:
        db.close()
