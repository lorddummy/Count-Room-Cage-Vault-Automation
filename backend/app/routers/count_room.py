"""Count room API: sessions, drop boxes, count results, variances."""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/count-room", tags=["count-room"])


@router.post("/properties", response_model=schemas.PropertyResponse)
def create_property(p: schemas.PropertyCreate, db: Session = Depends(get_db)):
    prop = models.Property(name=p.name, code=p.code)
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop


@router.get("/properties", response_model=List[schemas.PropertyResponse])
def list_properties(db: Session = Depends(get_db)):
    return db.query(models.Property).all()


@router.post("/drop-boxes", response_model=schemas.DropBoxResponse)
def create_drop_box(d: schemas.DropBoxCreate, db: Session = Depends(get_db)):
    box = models.DropBox(
        property_id=d.property_id,
        machine_id=d.machine_id,
        barcode=d.barcode,
        bank=d.bank,
        expected_cents=d.expected_cents,
    )
    db.add(box)
    db.commit()
    db.refresh(box)
    return box


@router.get("/drop-boxes", response_model=List[schemas.DropBoxResponse])
def list_drop_boxes(property_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    q = db.query(models.DropBox)
    if property_id is not None:
        q = q.filter(models.DropBox.property_id == property_id)
    return q.all()


@router.post("/sessions", response_model=schemas.SoftCountSessionResponse)
def start_count_session(s: schemas.SoftCountSessionCreate, db: Session = Depends(get_db)):
    session = models.SoftCountSession(
        property_id=s.property_id,
        notes=s.notes,
        status="open",
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions", response_model=List[schemas.SoftCountSessionResponse])
def list_sessions(
    property_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.SoftCountSession)
    if property_id is not None:
        q = q.filter(models.SoftCountSession.property_id == property_id)
    if status is not None:
        q = q.filter(models.SoftCountSession.status == status)
    return q.order_by(models.SoftCountSession.started_at.desc()).all()


@router.post("/sessions/{session_id}/close", response_model=schemas.SoftCountSessionResponse)
def close_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.SoftCountSession).filter(models.SoftCountSession.id == session_id).first()
    if not session:
        raise HTTPException(404, "Session not found")
    if session.status == "closed":
        raise HTTPException(400, "Session already closed")
    session.status = "closed"
    session.ended_at = datetime.utcnow()
    db.commit()
    db.refresh(session)
    return session


@router.post("/count-results", response_model=schemas.CountResultResponse)
def record_count_result(r: schemas.CountResultCreate, db: Session = Depends(get_db)):
    variance = None
    if r.expected_cents is not None:
        variance = r.counted_cents - r.expected_cents
    result = models.CountResult(
        session_id=r.session_id,
        drop_box_id=r.drop_box_id,
        counted_cents=r.counted_cents,
        expected_cents=r.expected_cents,
        variance_cents=variance,
        denomination_breakdown=r.denomination_breakdown,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.get("/count-results", response_model=List[schemas.CountResultResponse])
def list_count_results(
    session_id: Optional[int] = Query(None),
    variance_threshold_cents: Optional[int] = Query(None, description="Only results with |variance| >= this"),
    db: Session = Depends(get_db),
):
    q = db.query(models.CountResult)
    if session_id is not None:
        q = q.filter(models.CountResult.session_id == session_id)
    if variance_threshold_cents is not None:
        q = q.filter(
            models.CountResult.variance_cents != None,
            func.abs(models.CountResult.variance_cents) >= variance_threshold_cents,
        )
    return q.order_by(models.CountResult.created_at.desc()).all()


@router.get("/variances")
def list_variances(
    property_id: Optional[int] = Query(None),
    session_id: Optional[int] = Query(None),
    min_cents: Optional[int] = Query(50, description="Minimum |variance| to include"),
    db: Session = Depends(get_db),
):
    """List count results that have variance (for investigation workflow)."""
    q = (
        db.query(models.CountResult, models.DropBox)
        .join(models.DropBox, models.CountResult.drop_box_id == models.DropBox.id)
        .filter(models.CountResult.variance_cents != None)
        .filter(func.abs(models.CountResult.variance_cents) >= min_cents)
    )
    if session_id is not None:
        q = q.filter(models.CountResult.session_id == session_id)
    if property_id is not None:
        q = q.filter(models.DropBox.property_id == property_id)
    rows = q.order_by(models.CountResult.created_at.desc()).limit(100).all()
    return [
        {
            "count_result_id": r.id,
            "session_id": r.session_id,
            "drop_box_id": r.drop_box_id,
            "machine_id": d.machine_id,
            "barcode": d.barcode,
            "expected_cents": r.expected_cents,
            "counted_cents": r.counted_cents,
            "variance_cents": r.variance_cents,
            "created_at": r.created_at.isoformat(),
        }
        for r, d in rows
    ]
