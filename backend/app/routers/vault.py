"""Vault API: balance, transactions (fill, credit, deposit, armored car, cage replenishment)."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/vault", tags=["vault"])


def _vault_balance(db: Session, property_id: int) -> int:
    """Sum of all vault transactions: + deposit/credit, - fill/withdrawal/armored_car/cage_replenishment."""
    rows = (
        db.query(models.VaultTransaction.type, func.sum(models.VaultTransaction.amount_cents).label("total"))
        .filter(models.VaultTransaction.property_id == property_id)
        .group_by(models.VaultTransaction.type)
        .all()
    )
    balance = 0
    for type_, total in rows:
        total = total or 0
        if type_ in ("deposit", "credit"):
            balance += total
        else:
            balance -= total
    return balance


@router.get("/balance/{property_id}")
def get_vault_balance(property_id: int, db: Session = Depends(get_db)):
    """Current vault balance (sum of all transactions). Convention: deposit/credit add, fill/withdrawal/armored_car/cage_replenishment subtract."""
    return {"property_id": property_id, "balance_cents": _vault_balance(db, property_id)}


@router.post("/transactions", response_model=schemas.VaultTransactionResponse)
def create_vault_transaction(t: schemas.VaultTransactionCreate, db: Session = Depends(get_db)):
    # For fill/withdrawal/armored_car/cage_replenishment, amount is positive but decreases vault
    tx = models.VaultTransaction(
        property_id=t.property_id,
        type=t.type,
        amount_cents=t.amount_cents,
        table_id=t.table_id,
        drawer_id=t.drawer_id,
        reference_id=t.reference_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


@router.get("/transactions", response_model=List[schemas.VaultTransactionResponse])
def list_vault_transactions(
    property_id: int,
    type_: Optional[str] = Query(None, alias="type"),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
):
    q = db.query(models.VaultTransaction).filter(models.VaultTransaction.property_id == property_id)
    if type_ is not None:
        q = q.filter(models.VaultTransaction.type == type_)
    return q.order_by(models.VaultTransaction.created_at.desc()).limit(limit).all()


@router.get("/reconciliation/{property_id}")
def vault_reconciliation(property_id: int, db: Session = Depends(get_db)):
    """Expected balance from sum of transactions (same as balance). For full reconciliation we'd compare to physical count."""
    balance = _vault_balance(db, property_id)
    return {
        "property_id": property_id,
        "expected_balance_cents": balance,
        "message": "Compare to physical count; variance = physical - expected_balance_cents",
    }
