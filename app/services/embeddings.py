from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global model

    if model is None:
        model = SentenceTransformer(MODEL_NAME)

    return model


def embed_text(text: str) -> list[float]:
    return get_model().encode(text).tolist()


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    embedding_model = get_model()

    return [
        embedding_model.encode(chunk).tolist()
        for chunk in chunks
    ]
