from sqlalchemy.orm import Session

from app.models import PaperChunk
from app.services.embeddings import embed_text


def get_relevant_context(
    db: Session,
    paper_id: int,
    question: str,
) -> str:
    q_vector = embed_text(
        question
    )

    chunks = (
        db.query(PaperChunk)
        .filter(
            PaperChunk.paper_id == paper_id,
        )
        .order_by(
            PaperChunk.embedding.cosine_distance(
                q_vector
            )
        )
        .limit(3)
        .all()
    )

    return "\n\n".join(
        chunk.chunk_text
        for chunk in chunks
    )


def answer_question(
    question: str,
    context: str,
) -> dict[str, str]:
    answer = (
        f"Question: {question}\n\n"
        f"Relevant context:\n{context}"
    )

    return {
        "context": context,
        "answer": answer,
    }
