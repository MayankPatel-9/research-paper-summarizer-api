# CLAUDE.md

## Project Overview

This project is an **AI Research Paper Summarizer + Q&A API** built with FastAPI, PostgreSQL, pgvector, and Docker.

The application allows users to:

* Upload research paper PDFs
* Extract text from PDFs
* Store papers in PostgreSQL
* Generate structured summaries
* Ask questions about uploaded papers
* Retrieve semantically relevant chunks using embeddings
* Return context-aware answers

Primary goal:

Build a practical **RAG-based backend API** for academic research papers.

---

## Tech Stack

### Backend

* FastAPI
* Python 3.11

### Database

* PostgreSQL 16
* pgvector

### ORM

* SQLAlchemy

### PDF Parsing

* PyMuPDF

### Embeddings

* sentence-transformers
* model: `all-MiniLM-L6-v2`

### Containerization

* Docker
* docker-compose

---

## Project Structure

```bash
research-paper-api/

app/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
│
├── routes/
│   ├── papers.py
│   ├── summarize.py
│   ├── ask.py
│   └── history.py
│
├── services/
│   ├── pdf_parser.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── summarizer.py
│   └── qa.py
│
uploads/

Dockerfile
docker-compose.yml
requirements.txt
CLAUDE.md
```

---

## API Endpoints

### POST /api/papers

Upload PDF.

Accept:

* multipart/form-data
* field: `file`

Workflow:

* validate PDF
* save to uploads/
* extract text
* store paper in database
* chunk text
* generate embeddings
* save paper chunks

Response:

```json
{
  "paper_id": 1,
  "filename": "paper.pdf",
  "title": "Paper title"
}
```

---

### POST /api/summarize

Input:

```json
{
  "paper_id": 1
}
```

Generate structured summary:

* title
* problem_statement
* methodology
* dataset
* results
* limitations
* future_work

Save summary to DB.

---

### POST /api/ask

Input:

```json
{
  "paper_id": 1,
  "question": "What methodology is used?"
}
```

Workflow:

* embed question
* semantic search using pgvector
* retrieve top chunks
* generate answer

Response:

```json
{
  "question": "...",
  "context": "...",
  "answer": "..."
}
```

---

### GET /api/history

Return previous questions + answers.

---

## Database Models

### Paper

Fields:

* id
* filename
* title
* full_text
* summary
* created_at

---

### PaperChunk

Fields:

* id
* paper_id
* chunk_text
* embedding VECTOR(384)

---

### QAHistory

Fields:

* id
* paper_id
* question
* answer
* created_at

---

## Embedding Rules

Use:

`all-MiniLM-L6-v2`

Dimension:

384

Chunk size:

500 words

Search:

Top 3 chunks using cosine similarity.

---

## Code Guidelines

When generating code:

* prefer small focused functions
* use type hints
* keep routes thin
* place business logic inside services/
* use SQLAlchemy ORM
* avoid duplicate logic
* keep imports explicit
* handle FastAPI errors clearly
* return JSON responses
* keep code beginner-friendly and readable

---

## FastAPI Guidelines

Use:

* APIRouter
* Depends(get_db)
* UploadFile
* File(...)
* HTTPException

Swagger docs should remain usable.

---

## PostgreSQL Guidelines

Use SQLAlchemy models.

Use pgvector:

```python
from pgvector.sqlalchemy import Vector
```

Vector dimension:

384

---

## Docker Guidelines

Database container:

`pgvector/pgvector:pg16`

App container:

Python 3.11

Prefer reproducible setup.

---

## Future Improvements

Planned upgrades:

* OpenAI integration
* citation extraction
* metadata extraction (authors/year)
* compare multiple papers
* export summaries
* authentication
* frontend UI

---

## Important

When modifying code:

* preserve existing endpoints
* avoid breaking DB schema unnecessarily
* do not remove working upload flow
* keep project MVP stable
* prioritize clean readable code over abstraction
