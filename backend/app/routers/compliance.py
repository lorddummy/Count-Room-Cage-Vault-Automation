"""Compliance and audit reporting API."""
from datetime import datetime, date, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/compliance", tags=["compliance"])


@router.get("/reports/daily-slot-drop")
def daily_slot_drop_report(
    property_id: int,
    report_date: str = Query(..., description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Generate daily slot drop report (count results for the date)."""
    sessions = (
        db.query(models.SoftCountSession)
        .filter(models.SoftCountSession.property_id == property_id)
        .filter(func.date(models.SoftCountSession.started_at) == report_date)
        .all()
    )
    session_ids = [s.id for s in sessions]
    if not session_ids:
        return {
            "property_id": property_id,
            "date": report_date,
            "total_drop_cents": 0,
            "total_variance_cents": 0,
            "machines": [],
            "generated_at": datetime.utcnow().isoformat(),
            "message": "No count sessions found for this date.",
        }
    results = (
        db.query(models.CountResult, models.DropBox)
        .join(models.DropBox, models.CountResult.drop_box_id == models.DropBox.id)
        .filter(models.CountResult.session_id.in_(session_ids))
        .all()
    )
    total_drop = sum(r.counted_cents for r, _ in results)
    total_variance = sum(r.variance_cents or 0 for r, _ in results)
    machines = [
        {
            "machine_id": d.machine_id,
            "barcode": d.barcode,
            "expected_cents": r.expected_cents,
            "counted_cents": r.counted_cents,
            "variance_cents": r.variance_cents,
        }
        for r, d in results
    ]
    return {
        "property_id": property_id,
        "date": report_date,
        "total_drop_cents": total_drop,
        "total_variance_cents": total_variance,
        "machines": machines,
        "generated_at": datetime.utcnow().isoformat(),
    }


@router.get("/reports/daily-table")
def daily_table_report(
    property_id: int,
    report_date: str = Query(..., description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Generate daily table games report (inventory by table)."""
    invs = (
        db.query(models.TableInventory, models.Table)
        .join(models.Table, models.TableInventory.table_id == models.Table.id)
        .filter(models.Table.property_id == property_id)
        .filter(models.TableInventory.date == report_date)
        .all()
    )
    tables = []
    total_win = 0
    for inv, t in invs:
        tables.append({
            "table_id": t.id,
            "name": t.name,
            "game_type": t.game_type,
            "opening_cents": inv.opening_cents,
            "closing_cents": inv.closing_cents,
            "fills_cents": inv.fills_cents,
            "credits_cents": inv.credits_cents,
            "drop_cents": inv.drop_cents,
            "win_loss_cents": inv.win_loss_cents,
        })
        total_win += inv.win_loss_cents
    return {
        "property_id": property_id,
        "date": report_date,
        "tables": tables,
        "total_win_cents": total_win,
        "generated_at": datetime.utcnow().isoformat(),
    }


@router.get("/reports/variances")
def variance_report(
    property_id: int,
    from_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    to_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    min_cents: int = Query(500, description="Minimum |variance|"),
    db: Session = Depends(get_db),
):
    """List variances above threshold for audit (e.g. annual variance report)."""
    q = (
        db.query(models.CountResult, models.DropBox, models.SoftCountSession)
        .join(models.DropBox, models.CountResult.drop_box_id == models.DropBox.id)
        .join(models.SoftCountSession, models.CountResult.session_id == models.SoftCountSession.id)
        .filter(models.DropBox.property_id == property_id)
        .filter(models.CountResult.variance_cents != None)
        .filter(func.abs(models.CountResult.variance_cents) >= min_cents)
    )
    if from_date:
        q = q.filter(func.date(models.CountResult.created_at) >= from_date)
    if to_date:
        q = q.filter(func.date(models.CountResult.created_at) <= to_date)
    rows = q.order_by(models.CountResult.created_at.desc()).limit(500).all()
    return {
        "property_id": property_id,
        "from_date": from_date,
        "to_date": to_date,
        "min_cents": min_cents,
        "count": len(rows),
        "variances": [
            {
                "count_result_id": r.id,
                "machine_id": d.machine_id,
                "session_date": s.started_at.date().isoformat() if s.started_at else None,
                "expected_cents": r.expected_cents,
                "counted_cents": r.counted_cents,
                "variance_cents": r.variance_cents,
                "created_at": r.created_at.isoformat(),
            }
            for r, d, s in rows
        ],
        "generated_at": datetime.utcnow().isoformat(),
    }
