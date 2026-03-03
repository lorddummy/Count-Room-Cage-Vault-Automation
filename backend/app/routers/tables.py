"""Table games inventory API: tables, fills/credits (via vault), win/loss."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/tables", tags=["tables"])


@router.post("/", response_model=schemas.TableResponse)
def create_table(t: schemas.TableCreate, db: Session = Depends(get_db)):
    table = models.Table(
        property_id=t.property_id,
        name=t.name,
        game_type=t.game_type,
        bank=t.bank,
    )
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


@router.get("/", response_model=List[schemas.TableResponse])
def list_tables(property_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    q = db.query(models.Table)
    if property_id is not None:
        q = q.filter(models.Table.property_id == property_id)
    return q.all()


@router.post("/inventory", response_model=schemas.TableInventoryResponse)
def create_table_inventory(inv: schemas.TableInventoryCreate, db: Session = Depends(get_db)):
    # win_loss = opening + fills - credits + drop - closing
    win_loss = (
        inv.opening_cents
        + inv.fills_cents
        - inv.credits_cents
        + inv.drop_cents
        - inv.closing_cents
    )
    row = models.TableInventory(
        table_id=inv.table_id,
        date=inv.date,
        shift=inv.shift,
        opening_cents=inv.opening_cents,
        closing_cents=inv.closing_cents,
        fills_cents=inv.fills_cents,
        credits_cents=inv.credits_cents,
        drop_cents=inv.drop_cents,
        win_loss_cents=win_loss,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/inventory", response_model=List[schemas.TableInventoryResponse])
def list_table_inventory(
    table_id: Optional[int] = Query(None),
    property_id: Optional[int] = Query(None),
    date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.TableInventory).join(models.Table)
    if table_id is not None:
        q = q.filter(models.TableInventory.table_id == table_id)
    if property_id is not None:
        q = q.filter(models.Table.property_id == property_id)
    if date is not None:
        q = q.filter(models.TableInventory.date == date)
    return q.order_by(models.TableInventory.date.desc(), models.TableInventory.table_id).all()
