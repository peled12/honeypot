from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.deps import get_db
from app.db import models

router = APIRouter(prefix="/summary", tags=["Summary"])

# get total number of events
@router.get("/total-events")
def get_total_events(db: Session = Depends(get_db)):
    try:
        total = db.query(func.count(models.Event.id)).scalar()
        return {"total_events": total or 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting total events: {str(e)}")

# get number of unique source ips
@router.get("/unique-ips")
def get_unique_ips(db: Session = Depends(get_db)):
    try:
        unique_ips = db.query(func.count(distinct(models.Event.source_ip))).scalar()
        return {"unique_ips": unique_ips or 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting unique IPs: {str(e)}")

# get the most common http method
@router.get("/most-common-method")
def get_most_common_method(db: Session = Depends(get_db)):
    try:
        result = (
            db.query(models.Event.method, func.count(models.Event.method))
            .group_by(models.Event.method)
            .order_by(func.count(models.Event.method).desc())
            .first()
        )
        return {"most_common_method": result[0] if result else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting common method: {str(e)}")

# get the most common path
@router.get("/most-common-path")
def get_most_common_path(db: Session = Depends(get_db)):
    try:
        result = (
            db.query(models.Event.path, func.count(models.Event.path))
            .group_by(models.Event.path)
            .order_by(func.count(models.Event.path).desc())
            .first()
        )
        return {"most_common_path": result[0] if result else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting common path: {str(e)}")

# TODO: can add more summary endpoints here