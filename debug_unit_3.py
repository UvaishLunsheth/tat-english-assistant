import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ingestion.load_unit import load_unit

# Load the Unit 3 text
text = load_unit(3)

# Find where Vocabulary starts and Writing ends
vocab_pos = text.find("Vocabulary")
writing_pos = text.find("Writing")

print("\n===== UNIT 3 RAW OCR TEXT =====")
if vocab_pos != -1 and writing_pos != -1:
    # Print the text where the function marker is hiding
    print(text[vocab_pos:writing_pos])
else:
    print(f"Could not find positions. Vocab: {vocab_pos}, Writing: {writing_pos}")