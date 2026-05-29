from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.sql import func

from app.database import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    filename = Column(String)

    title = Column(String)

    full_text = Column(Text)

    summary = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class PaperChunk(Base):
    __tablename__ = "paper_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    paper_id = Column(
        Integer,
        ForeignKey("papers.id"),
    )

    chunk_text = Column(Text)

    embedding = Column(
        Vector(384),
    )


class QAHistory(Base):
    __tablename__ = "qa_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    paper_id = Column(
        Integer,
        ForeignKey("papers.id"),
    )

    question = Column(Text)

    answer = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
