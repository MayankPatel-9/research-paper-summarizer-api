def generate_summary(text: str) -> dict[str, str]:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    title = lines[0] if lines else "Untitled"

    content = text[:3000]

    return {
        "title": title,
        "problem_statement": content[:400],
        "methodology": content[400:900],
        "dataset": content[900:1200],
        "results": content[1200:1800],
        "limitations": "To be extracted.",
        "future_work": "To be explored.",
    }
