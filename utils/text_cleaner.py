import re


def clean_text(text: str) -> str:

    if not text:
        return ""

    patterns = [
        r"English\s*\(.*?\)\s*,?\s*Std\.?\s*12",
        r"English\s*\(.*?\)\s*Std\.?\s*12",
        r"\n{2,}"
    ]

    for pattern in patterns:
        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE
        )

    # ---- ADDED PAGE NUMBER CLEANING REGEXES ----
    text = re.sub(
        r"\n\d+\n",
        "\n",
        text
    )

    text = re.sub(
        r"^\d+\s*$",
        "",
        text,
        flags=re.MULTILINE
    )
    # --------------------------------------------

    return text.strip()


def clean_pre_task(text: str):

    text = clean_text(text)

    text = re.sub(
        r"^UNIT\s*\d+\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^Pre-task\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


def clean_content(text: str):

    text = clean_text(text)

    text = re.sub(
        r"^Read\s*\d+\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


def clean_glossary(text: str):

    text = clean_text(text)

    text = re.sub(
        r"^Glossary\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


def clean_comprehension(text: str):

    text = clean_text(text)

    text = re.sub(
        r"^Comprehension\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


def clean_author(author):

    if not author:
        return None

    author = author.strip()

    author = re.sub(
        r"^A\s+",
        "",
        author
    )

    return author