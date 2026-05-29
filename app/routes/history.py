from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import QAHistory

router = APIRouter()

@router.get("/history")
def get_history(
    paper_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Return previous Q&A history.

    If `paper_id` is provided, filter by that paper; otherwise return all entries.
    The results are ordered by most recent first.
    """
    query = db.query(QAHistory).order_by(QAHistory.created_at.desc())
    if paper_id is not None:
        query = query.filter(QAHistory.paper_id == paper_id)
    records = query.all()
    return [
        {
            "paper_id": r.paper_id,
            "question": r.question,
            "answer": r.answer,
            "created_at": r.created_at.isoformat(),
        }
        for r in records
    ]
