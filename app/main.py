from fastapi import FastAPI

import app.models
from app.database import Base
from app.database import engine
from app.routes import ask
from app.routes import papers
from app.routes import summarize
from app.routes import history

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Research Paper API")

app.include_router(
    papers.router,
    prefix="/api",
    tags=["papers"],
)

app.include_router(
    summarize.router,
    prefix="/api",
    tags=["summarize"],
)

app.include_router(
    ask.router,
    prefix="/api",
    tags=["ask"],
)

app.include_router(
    history.router,
    prefix="/api",
    tags=["history"],
)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
