import json
import random
from pathlib import Path

# ==================================================
# PATHS
# ==================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PAPER_DIR = ( PROJECT_ROOT / "generated_papers" )
OUTPUT_DIR = ( PROJECT_ROOT / "formatted_papers" )
OUTPUT_DIR.mkdir( exist_ok=True )

# ==================================================
# INPUT FILE
# ==================================================
topic = input( "\nTopic file name (without .json): " ).strip()
INPUT_FILE = ( PAPER_DIR / f"{topic}.json" )

if not INPUT_FILE.exists():
    print()
    print("Paper not found")
    print(INPUT_FILE)
    raise SystemExit

# ==================================================
# LOAD PAPER
# ==================================================
with open( INPUT_FILE, "r", encoding="utf-8" ) as f:
    paper = json.load(f)

# ==================================================
# AUTOMATIC TOTAL MARKS
# ==================================================
total_marks = 0
total_marks += len(paper.get("mcq", []))
total_marks += len(paper.get("fill_blank", []))
total_marks += len(paper.get("true_false", []))
total_marks += len(paper.get("match", []))
total_marks += (len(paper.get("short_answer", [])) * 2)
total_marks += (len(paper.get("medium_answer", [])) * 4)
total_marks += (len(paper.get("long_answer", [])) * 6)

# ==================================================
# BUILD PAPER
# ==================================================
lines = []

# ==================================================
# HEADER
# ==================================================
lines.append("=" * 70)
lines.append(f"{paper['topic'].upper()} PRACTICE TEST")
lines.append("=" * 70)
lines.append("")
lines.append("Name : __________________________")
lines.append("Date : __________________________")
lines.append("")
lines.append("Time : 45 Minutes")
lines.append(f"Total Marks : {total_marks}")
lines.append("")

# ==================================================
# SECTION A
# ==================================================
lines.append( "SECTION A - MULTIPLE CHOICE QUESTIONS" )
lines.append( "(1 Mark Each)" )
lines.append( f"Total Marks: {len(paper.get('mcq', []))}" )
lines.append("")
for i, q in enumerate( paper.get("mcq", []), start=1 ):
    lines.append( f"{i}. {q ['question'] }" )
    
    options = q ["options"]
    labels = [ "A", "B", "C", "D" ]
    
    for label, option in zip( labels, options ):
        lines.append( f"   {label}. {option}" )
        
    lines.append("")

# ==================================================
# SECTION B
# ==================================================
lines.append( "SECTION B - FILL IN THE BLANKS" )
lines.append( "(1 Mark Each)" )
lines.append( f"Total Marks: {len(paper.get('fill_blank', []))}" )
lines.append("")
for i, q in enumerate( paper.get("fill_blank", []), start=1 ):
    lines.append( f"{i}. {q ['question'] }" )
    lines.append("")

# ==================================================
# SECTION C
# ==================================================
lines.append( "SECTION C - TRUE / FALSE" )
lines.append( "(1 Mark Each)" )
lines.append( f"Total Marks: {len(paper.get('true_false', []))}" )
lines.append("")
for i, q in enumerate( paper.get("true_false", []), start=1 ):
    lines.append( f"{i}. {q ['statement'] }" )
    lines.append("")

# ==================================================
# SECTION D
# ==================================================
match_items = paper.get("match", [])
right_items = [item["right"] for item in match_items]
random.shuffle(right_items)

lines.append("SECTION D - MATCH THE FOLLOWING")
lines.append("(1 Mark Each)")
lines.append(f"Total Marks: {len(match_items)}")
lines.append("")
lines.append("COLUMN A")
lines.append("")

for idx, item in enumerate(match_items, start=1):
    lines.append(f"{idx}. {item['left']}")

lines.append("")
lines.append("COLUMN B")
lines.append("")

for idx, item in enumerate(right_items, start=1):
    lines.append(f"{chr(64 + idx)}. {item}")

lines.append("")

# ==================================================
# SECTION E
# ==================================================
lines.append( "SECTION E - SHORT ANSWER QUESTIONS" )
lines.append( "(2 Marks Each)" )
lines.append( f"Total Marks: {len(paper.get('short_answer', [])) * 2}" )
lines.append("")
for i, q in enumerate( paper.get("short_answer", []), start=1 ):
    lines.append(f"{i}. {q['question']}")
    lines.append("")
    lines.append("________________________________________________")
    lines.append("________________________________________________")
    lines.append("")

# ==================================================
# SECTION F
# ==================================================
lines.append( "SECTION F - MEDIUM ANSWER QUESTIONS" )
lines.append( "(4 Marks Each)" )
lines.append( f"Total Marks: {len(paper.get('medium_answer', [])) * 4}" )
lines.append("")
for i, q in enumerate( paper.get("medium_answer", []), start=1 ):
    lines.append( f"{i}. {q ['question'] }" )
    lines.append("")
    lines.append("________________________________________________")
    lines.append("________________________________________________")
    lines.append("________________________________________________")
    lines.append("________________________________________________")
    lines.append("")

# ==================================================
# SECTION G
# ==================================================
lines.append( "SECTION G - LONG ANSWER QUESTIONS" )
lines.append( "(6 Marks Each)" )
lines.append( f"Total Marks: {len(paper.get('long_answer', [])) * 6}" )
lines.append("")
for i, q in enumerate( paper.get("long_answer", []), start=1 ):
    lines.append( f"{i}. {q ['question'] }" )
    lines.append("")
    for _ in range(8):
        lines.append(
            "________________________________________________"
        )
    lines.append("")

# ==================================================
# STUDENT SCORE SHEET
# ==================================================
lines.append("")
lines.append("=" * 70)
lines.append("STUDENT SCORE SHEET")
lines.append("=" * 70)
lines.append("")
lines.append(f"MCQ            ____ / {len(paper.get('mcq', []))}")
lines.append(f"Fill Blank     ____ / {len(paper.get('fill_blank', []))}")
lines.append(f"True False     ____ / {len(paper.get('true_false', []))}")
lines.append(f"Match          ____ / {len(paper.get('match', []))}")
lines.append(f"Short Answer   ____ / {len(paper.get('short_answer', [])) * 2}")
lines.append(f"Medium Answer  ____ / {len(paper.get('medium_answer', [])) * 4}")
lines.append(f"Long Answer    ____ / {len(paper.get('long_answer', [])) * 6}")
lines.append("")
lines.append(f"TOTAL          ____ / {total_marks}")
lines.append("")

# ==================================================
# END OF PAPER
# ==================================================
lines.append("")
lines.append("=" * 70)
lines.append("END OF PAPER")
lines.append("=" * 70)

# ==================================================
# SAVE
# ==================================================
OUTPUT_FILE = ( OUTPUT_DIR / f"{topic}_test.txt" )

with open( OUTPUT_FILE, "w", encoding="utf-8" ) as f:
    f.write( "\n".join(lines) )

# ==================================================
# DONE
# ==================================================
print()
print("=" * 60)
print("PAPER CREATED")
print("=" * 60)
print(OUTPUT_FILE)
print()