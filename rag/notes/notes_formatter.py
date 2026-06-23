import json
from pathlib import Path

# ==================================================
# PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

INPUT_DIR = (
    PROJECT_ROOT
    / "generated_notes"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "formatted_notes"
)

OUTPUT_DIR.mkdir(
    exist_ok=True
)

# ==================================================
# PROCESS FILES
# ==================================================

files = list(
    INPUT_DIR.glob("*.json")
)

print()
print("=" * 70)
print(f"Files found : {len(files)}")
print("=" * 70)

for file_path in files:

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    topic = data.get(
        "topic",
        "Unknown Topic"
    )

    source = data.get(
        "source",
        ""
    )

    author = data.get(
        "author",
        ""
    )

    theme = data.get(
        "theme",
        ""
    )

    lines = []

    # ==================================================
    # HEADER
    # ==================================================

    lines.append("=" * 70)
    lines.append(topic.upper())
    lines.append("=" * 70)

    if author:
        lines.append(
            f"Author : {author}"
        )

    if source:
        lines.append(
            f"Source : {source}"
        )

    if theme:
        lines.append(
            f"Theme  : {theme}"
        )

    lines.append("")

    # ==================================================
    # DEFINITION
    # ==================================================

    if data.get("definition"):

        lines.append("DEFINITION")
        lines.append("-" * 70)

        lines.append(
            data["definition"]
        )

        lines.append("")

    # ==================================================
    # CHARACTERISTICS
    # ==================================================

    if data.get("characteristics"):

        lines.append("CHARACTERISTICS")
        lines.append("-" * 70)

        for i, item in enumerate(
            data["characteristics"],
            start=1
        ):
            lines.append(
                f"{i}. {item}"
            )

        lines.append("")

    # ==================================================
    # PRINCIPLES
    # ==================================================

    if data.get("principles"):

        lines.append("PRINCIPLES")
        lines.append("-" * 70)

        for i, item in enumerate(
            data["principles"],
            start=1
        ):
            lines.append(
                f"{i}. {item}"
            )

        lines.append("")

    # ==================================================
    # MERITS
    # ==================================================

    if data.get("merits"):

        lines.append("MERITS")
        lines.append("-" * 70)

        for i, item in enumerate(
            data["merits"],
            start=1
        ):
            lines.append(
                f"{i}. {item}"
            )

        lines.append("")

    # ==================================================
    # DEMERITS
    # ==================================================

    if data.get("demerits"):

        if len(data["demerits"]) > 0:

            lines.append("DEMERITS")
            lines.append("-" * 70)

            for i, item in enumerate(
                data["demerits"],
                start=1
            ):
                lines.append(
                    f"{i}. {item}"
                )

            lines.append("")

    # ==================================================
    # SUMMARY
    # ==================================================

    if data.get("summary"):

        lines.append("SUMMARY")
        lines.append("-" * 70)

        lines.append(
            data["summary"]
        )

        lines.append("")

    # ==================================================
    # IMPORTANT POINTS
    # ==================================================

    if data.get("important_points"):

        lines.append("IMPORTANT POINTS")
        lines.append("-" * 70)

        for i, point in enumerate(
            data["important_points"],
            start=1
        ):
            lines.append(
                f"{i}. {point}"
            )

        lines.append("")

    # ==================================================
    # IMPORTANT WORDS
    # ==================================================

    if data.get("important_words"):

        lines.append("IMPORTANT WORDS")
        lines.append("-" * 70)

        for row in data["important_words"]:

            word = row.get(
                "word",
                ""
            )

            meaning = row.get(
                "meaning",
                ""
            )

            lines.append(
                f"{word} : {meaning}"
            )

        lines.append("")

    # ==================================================
    # ONE MARK QUESTIONS
    # ==================================================

    if data.get("one_mark"):

        lines.append("ONE MARK QUESTIONS")
        lines.append("-" * 70)

        for i, row in enumerate(
            data["one_mark"],
            start=1
        ):

            lines.append(
                f"{i}. {row['question']}"
            )

            lines.append(
                f"Answer : {row['answer']}"
            )

            lines.append("")

    # ==================================================
    # SHORT ANSWER QUESTIONS
    # ==================================================

    if data.get("short_answer"):

        lines.append("SHORT ANSWER QUESTIONS")
        lines.append("-" * 70)

        for i, row in enumerate(
            data["short_answer"],
            start=1
        ):

            lines.append(
                f"{i}. {row['question']}"
            )

            lines.append(
                f"Answer : {row['answer']}"
            )

            lines.append("")

    # ==================================================
    # LONG ANSWER QUESTIONS
    # ==================================================

    if data.get("long_answer"):

        lines.append("LONG ANSWER QUESTIONS")
        lines.append("-" * 70)

        for i, row in enumerate(
            data["long_answer"],
            start=1
        ):

            lines.append(
                f"{i}. {row['question']}"
            )

            lines.append(
                "Answer :"
            )

            lines.append(
                row["answer"]
            )

            lines.append("")

    # ==================================================
    # SAVE
    # ==================================================

    output_file = (
        OUTPUT_DIR
        / f"{file_path.stem}.txt"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(lines)
        )

    print(
        f"Created : {output_file.name}"
    )

# ==================================================
# SUMMARY
# ==================================================

print()
print("=" * 70)
print("NOTES FORMATTING COMPLETE")
print("=" * 70)
print(f"Files created : {len(files)}")
print(f"Saved in      : {OUTPUT_DIR}")
print("=" * 70)