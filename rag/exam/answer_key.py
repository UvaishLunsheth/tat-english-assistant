import json
from pathlib import Path

# ==================================================
# PATHS
# ==================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

PAPER_DIR = (PROJECT_ROOT / "generated_papers")
ANSWER_KEY_DIR = (PROJECT_ROOT / "answer_keys")

ANSWER_KEY_DIR.mkdir(exist_ok=True)

# ==================================================
# INPUT
# ==================================================
topic = input("\nTopic file name (without .json): ").strip()

INPUT_FILE = (PAPER_DIR / f"{topic}.json")

if not INPUT_FILE.exists():
    print()
    print(f"File not found: {INPUT_FILE}")
    raise SystemExit

# ==================================================
# LOAD PAPER
# ==================================================
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    paper = json.load(f)

# ==================================================
# BUILD ANSWER KEY
# ==================================================
answer_key = {
    "topic": paper.get(
        "topic",
        topic
    ),
    "mcq": [],
    "fill_blank": [],
    "true_false": [],
    "short_answer": [],
    "medium_answer": [],
    "long_answer": []
}

# ==================================================
# MCQ
# ==================================================
for q in paper.get("mcq", []):
    answer_key["mcq"].append(
        q.get(
            "answer",
            "N/A"
        )
    )

# ==================================================
# FILL BLANK
# ==================================================
for q in paper.get("fill_blank", []):
    answer_key["fill_blank"].append(
        q.get(
            "answer",
            "N/A"
        )
    )

# ==================================================
# TRUE FALSE
# ==================================================
for q in paper.get("true_false", []):
    answer_key["true_false"].append(
        q.get(
            "answer",
            "N/A"
        )
    )

# ==================================================
# SHORT ANSWER
# ==================================================
for q in paper.get("short_answer", []):
    answer_key["short_answer"].append({
        "question": q.get(
            "question",
            ""
        ),
        "answer": q.get(
            "answer",
            ""
        )
    })

# ==================================================
# MEDIUM ANSWER
# ==================================================
for q in paper.get("medium_answer", []):
    answer_key["medium_answer"].append({
        "question": q.get(
            "question",
            ""
        ),
        "answer": q.get(
            "answer",
            ""
        )
    })

# ==================================================
# LONG ANSWER
# ==================================================
for q in paper.get("long_answer", []):
    answer_key["long_answer"].append({
        "question": q.get(
            "question",
            ""
        ),
        "answer": q.get(
            "answer",
            ""
        )
    })

# ==================================================
# SAVE
# ==================================================
OUTPUT_FILE = (ANSWER_KEY_DIR / f"{topic}_answers.json")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        answer_key,
        f,
        indent=2,
        ensure_ascii=False
    )

# ==================================================
# PRINT
# ==================================================
print()
print("=" * 60)
print(f"{paper['topic'].upper()} - ANSWER KEY")
print("=" * 60)

# -------------------
# MCQ
# -------------------
print("\nMCQ ANSWERS")
for i, ans in enumerate(answer_key["mcq"], start=1):
    print(f"{i}. {ans}")

# -------------------
# FILL BLANK
# -------------------
print("\nFILL IN THE BLANKS")
for i, ans in enumerate(answer_key["fill_blank"], start=1):
    print(f"{i}. {ans}")

# -------------------
# TRUE FALSE
# -------------------
print("\nTRUE / FALSE")
for i, ans in enumerate(answer_key["true_false"], start=1):
    print(f"{i}. {ans}")

print()
print("=" * 60)
print("Saved")
print("=" * 60)
print(OUTPUT_FILE)
print()