# Research Paper Summarizer API

AI-powered research paper summarizer and Q&A API built with FastAPI, PostgreSQL + pgvector, Docker, and Google Gemini.

## Features

- Upload research paper PDFs
- Extract paper text
- Generate structured summaries
- Ask questions using semantic retrieval
- Store Q&A history
- Docker support

## Tech Stack

- FastAPI
- PostgreSQL
- pgvector
- SQLAlchemy
- Google Gemini API
- Docker

## Run locally

pip install -r requirements.txt
docker compose up -d
uvicorn app.main:app --reload

## API docs

http://127.0.0.1:8000/docs