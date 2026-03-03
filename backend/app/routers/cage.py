"""Cage API: cashiers, drawers, transactions, shift balancing."""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/cage", tags=["cage"])


@router.post("/cashiers", response_model=schemas.CashierResponse)
def create_cashier(c: schemas.CashierCreate, db: Session = Depends(get_db)):
    cashier = models.Cashier(property_id=c.property_id, name=c.name, employee_id=c.employee_id)
    db.add(cashier)
    db.commit()
    db.refresh(cashier)
    return cashier


@router.get("/cashiers", response_model=List[schemas.CashierResponse])
def list_cashiers(property_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    q = db.query(models.Cashier)
    if property_id is not None:
        q = q.filter(models.Cashier.property_id == property_id)
    return q.all()


@router.post("/drawers", response_model=schemas.DrawerResponse)
def open_drawer(d: schemas.DrawerCreate, db: Session = Depends(get_db)):
    drawer = models.Drawer(
        cashier_id=d.cashier_id,
        property_id=d.property_id,
        opening_cents=d.opening_cents,
        status="open",
    )
    db.add(drawer)
    db.commit()
    db.refresh(drawer)
    return drawer


@router.post("/drawers/{drawer_id}/close", response_model=schemas.DrawerResponse)
def close_drawer(drawer_id: int, body: schemas.DrawerClose, db: Session = Depends(get_db)):
    drawer = db.query(models.Drawer).filter(models.Drawer.id == drawer_id).first()
    if not drawer:
        raise HTTPException(404, "Drawer not found")
    if drawer.status == "closed":
        raise HTTPException(400, "Drawer already closed")
    # Compute expected from opening + net transactions (chip_redemption/tito = cash out negative)
    sum_tx = (
        db.query(func.coalesce(func.sum(models.CageTransaction.amount_cents), 0))
        .filter(models.CageTransaction.drawer_id == drawer_id)
        .scalar()
    )
    # Convention: amount_cents positive when we give cash to player (redemption), so expected = opening - sum
    expected = drawer.opening_cents - sum_tx
    drawer.expected_cents = expected
    drawer.closing_cents = body.closing_cents
    drawer.status = "closed"
    drawer.closed_at = datetime.utcnow()
    db.commit()
    db.refresh(drawer)
    return drawer


@router.get("/drawers", response_model=List[schemas.DrawerResponse])
def list_drawers(
    property_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    cashier_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Drawer)
    if property_id is not None:
        q = q.filter(models.Drawer.property_id == property_id)
    if status is not None:
        q = q.filter(models.Drawer.status == status)
    if cashier_id is not None:
        q = q.filter(models.Drawer.cashier_id == cashier_id)
    return q.order_by(models.Drawer.opened_at.desc()).all()


@router.get("/drawers/{drawer_id}/balance")
def get_drawer_balance(drawer_id: int, db: Session = Depends(get_db)):
    """Current expected balance (opening - sum of transaction amounts)."""
    drawer = db.query(models.Drawer).filter(models.Drawer.id == drawer_id).first()
    if not drawer:
        raise HTTPException(404, "Drawer not found")
    sum_tx = (
        db.query(func.coalesce(func.sum(models.CageTransaction.amount_cents), 0))
        .filter(models.CageTransaction.drawer_id == drawer_id)
        .scalar()
    )
    expected_cents = drawer.opening_cents - sum_tx
    return {
        "drawer_id": drawer_id,
        "opening_cents": drawer.opening_cents,
        "expected_cents": expected_cents,
        "variance_cents": (drawer.closing_cents - expected_cents) if drawer.closing_cents is not None else None,
        "status": drawer.status,
    }


@router.post("/transactions", response_model=schemas.CageTransactionResponse)
def create_cage_transaction(t: schemas.CageTransactionCreate, db: Session = Depends(get_db)):
    drawer = db.query(models.Drawer).filter(models.Drawer.id == t.drawer_id).first()
    if not drawer:
        raise HTTPException(404, "Drawer not found")
    if drawer.status != "open":
        raise HTTPException(400, "Drawer is closed")
    tx = models.CageTransaction(
        drawer_id=t.drawer_id,
        type=t.type,
        amount_cents=t.amount_cents,
        reference_id=t.reference_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


@router.get("/drawers/{drawer_id}/transactions", response_model=List[schemas.CageTransactionResponse])
def list_drawer_transactions(drawer_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.CageTransaction)
        .filter(models.CageTransaction.drawer_id == drawer_id)
        .order_by(models.CageTransaction.created_at.desc())
        .all()
    )


@router.get("/reconciliation")
def cage_reconciliation(
    property_id: int,
    date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Aggregate drawer variances for the day (or all time if no date)."""
    q = (
        db.query(models.Drawer)
        .filter(models.Drawer.property_id == property_id)
        .filter(models.Drawer.status == "closed")
        .filter(models.Drawer.closing_cents != None)
        .filter(models.Drawer.expected_cents != None)
    )
    if date:
        q = q.filter(func.date(models.Drawer.closed_at) == date)
    drawers = q.all()
    total_variance = sum((d.closing_cents or 0) - (d.expected_cents or 0) for d in drawers)
    return {
        "property_id": property_id,
        "date": date,
        "drawers_closed": len(drawers),
        "total_variance_cents": total_variance,
        "drawers": [
            {
                "drawer_id": d.id,
                "cashier_id": d.cashier_id,
                "variance_cents": (d.closing_cents or 0) - (d.expected_cents or 0),
                "closed_at": d.closed_at.isoformat() if d.closed_at else None,
            }
            for d in drawers
        ],
    }
