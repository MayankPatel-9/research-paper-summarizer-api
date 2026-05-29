import os
import json
from typing import Dict


def generate_response(text: str) -> Dict[str, str]:
    """Generate a structured summary using Google Gemini.

    Returns a dictionary with keys:
      title, problem_statement, methodology, dataset, results, limitations, future_work.
    Raises RuntimeError if Gemini is unavailable or any error occurs.
    """
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("Missing GOOGLE_API_KEY environment variable")

    try:
        import google.generativeai as genai
    except Exception as exc:
        raise RuntimeError("google.generativeai library not available")

    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            "You are an AI summarizer. Summarize the following research paper text into the following sections: "
            "title, problem_statement, methodology, dataset, results, limitations, future_work. "
            "Return a JSON object with those keys and string values. Here is the paper text:\n"
            f"{text}"
        )
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"},
        )
        content = response.text
        # Extract JSON portion
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end == -1:
            raise RuntimeError("No JSON found in Gemini response")
        json_str = content[start : end + 1]
        data = json.loads(json_str)
        # Ensure all required keys are present
        required_keys = [
            "title",
            "problem_statement",
            "methodology",
            "dataset",
            "results",
            "limitations",
            "future_work",
        ]
        for k in required_keys:
            data.setdefault(k, "")
        return data
    except Exception as exc:
        raise RuntimeError(f"Gemini summarization failed: {exc}")


def generate_answer(question: str, context: str) -> str:
    """Ask Gemini to answer a question based on provided context.

    Returns the answer string. Raises RuntimeError on failure.
    """
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("Missing GOOGLE_API_KEY environment variable")

    try:
        import google.generativeai as genai
    except Exception as exc:
        raise RuntimeError("google.generativeai library not available")

    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            "Answer the following question based on the provided context.\n"
            f"Question: {question}\n"
            f"Context: {context}\n"
            "Answer:"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        raise RuntimeError(f"Gemini answer generation failed: {exc}")
