from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Paper
from app.models import QAHistory
from app.services.qa import answer_question
from app.services.qa import get_relevant_context
from app.services.gemini_client import generate_answer

router = APIRouter()


class AskRequest(BaseModel):
    paper_id: int
    question: str


@router.post("/ask")
def ask_question(
    request: AskRequest,
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

    context = get_relevant_context(
        db,
        paper.id,
        request.question,
    )

    result = answer_question(
        request.question,
        context,
    )

    qa = QAHistory(
        paper_id=paper.id,
        question=request.question,
        answer=result["answer"],
    )

    db.add(qa)
    db.commit()

    return {
        "question": request.question,
        "context": context,
        "answer": result["answer"],
    }
