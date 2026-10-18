from datetime import datetime, date
from fastapi import APIRouter, Depends, Query 
from sqlmodel import Session, select, func
from models import Order, Orderstatus
from database import get_session


router = APIRouter(prefix='/stats', tags=["stats"])

@router.get('/daily')
def daily_summary(
    summary_date: date |None = Query(default=None, description="date for summary(YYYY-MM-DD)"),
    session = Session(get_session)
):
    if summary_date is None:
        summary_date = date.today()

    start = datetime.combine(summary_date, datetime.min.time())
    end = datetime.combine(summary_date, datetime.max.time())    

    summary = {}
    total = 0

    for status in Orderstatus:
        count = session.exec(
            select(func.count()).where(
                Order.status == status,
                Order.created_at >= start,
                Order.created_at <= end
            )
        ).one()
        summary[status.value] = count
        total += count
    return {
            "date": summary_date.isoformat(),
            "total_oders": total,
            "by_status": summary
        }
     