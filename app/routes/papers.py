from pathlib import Path

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Paper
from app.models import PaperChunk
from app.services.chunking import chunk_text
from app.services.embeddings import embed_chunks
from app.services.pdf_parser import extract_text

router = APIRouter()

UPLOAD_DIR = Path("uploads")


@router.post("/papers")
async def create_paper(
    file: UploadFile,
    db: Session = Depends(get_db),
) -> dict[str, int | str | None]:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / Path(file.filename).name

    contents = await file.read()
    file_path.write_bytes(contents)

    extracted = extract_text(str(file_path))

    paper = Paper(
        filename=file.filename,
        title=extracted["title"],
        full_text=extracted["full_text"],
    )

    db.add(paper)
    db.commit()
    db.refresh(paper)

    chunks = chunk_text(
        extracted["full_text"]
    )

    vectors = embed_chunks(
        chunks
    )

    for chunk, vector in zip(
        chunks,
        vectors,
    ):
        db.add(
            PaperChunk(
                paper_id=paper.id,
                chunk_text=chunk,
                embedding=vector,
            )
        )

    db.commit()

    return {
        "paper_id": paper.id,
        "filename": paper.filename,
        "title": paper.title,
        "preview": paper.full_text[:500],
    }
