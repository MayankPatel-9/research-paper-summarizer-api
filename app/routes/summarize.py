from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Paper
from app.services.summarizer import generate_summary
from app.services.gemini_client import generate_response
import os

router = APIRouter()


class SummaryRequest(BaseModel):
    paper_id: int


@router.post("/summarize")
def summarize_paper(
    request: SummaryRequest,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    paper = db.query(Paper).filter(
        Paper.id == request.paper_id,
    ).first()

    if not paper:
        raise HTTPException(
            status_code=404,
            detail="Paper not found",
        )

    try:
        if os.getenv("GOOGLE_API_KEY"):
            summary = generate_response(paper.full_text)
        else:
            summary = generate_summary(paper.full_text)
    except Exception:
        summary = generate_summary(paper.full_text)

    paper.summary = str(summary)

    db.commit()

    return summary
