import re
import sys
from pathlib import Path

# Fix path resolution upfront so testing works perfectly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def find_position(text: str, pattern: str):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.start()
    return -1


# --- THE REUSABLE FUNCTION THAT REPLACES SPLIT_READ_1 AND SPLIT_READ_2 ---
def split_read_block(read_block: str):
    glossary_pos = find_position(read_block, r"Glossary")
    comprehension_pos = find_position(read_block, r"Comprehension")

    content = read_block[:glossary_pos]
    glossary = read_block[glossary_pos:comprehension_pos]
    comprehension = read_block[comprehension_pos:]

    return {
        "content": content.strip(),
        "glossary": glossary.strip(),
        "comprehension": comprehension.strip(),
    }


if __name__ == "__main__":
    from ingestion.load_unit import load_unit

    # Load complete unit text
    text = load_unit(1)

    # Find the boundaries for the blocks
    read_1_start = text.find("Read 1")
    read_2_start = text.find("Read 2")
    vocab_start = text.find("Vocabulary")

    # Slice the text into distinct blocks
    read_1_block = text[read_1_start:read_2_start]
    read_2_block = text[read_2_start:vocab_start]

    # --- Test Read 1 ---
    print("\n================= TESTING READ 1 =================")
    result_1 = split_read_block(read_1_block)

    print("\n--- CONTENT PREVIEW ---")
    print(result_1["content"][:300])

    print("\n--- GLOSSARY PREVIEW ---")
    print(result_1["glossary"][:200])

    print("\n--- COMPREHENSION PREVIEW ---")
    print(result_1["comprehension"][:200])

    # --- Test Read 2 ---
    print("\n================= TESTING READ 2 =================")
    result_2 = split_read_block(read_2_block)

    print("\n--- CONTENT PREVIEW ---")
    print(result_2["content"][:300])