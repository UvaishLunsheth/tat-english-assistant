from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.retriever import get_retriever

retriever = get_retriever()

# ==================================================
# QUERY
# ==================================================

query = input("Question: ")

docs = retriever.invoke(query)

# ==================================================
# RESULTS
# ==================================================

print()
print("=" * 80)
print("RETRIEVAL RESULTS")
print("=" * 80)

for i, doc in enumerate(docs, start=1):

    metadata = doc.metadata

    source = metadata.get(
        "source",
        "unknown"
    )

    print()
    print(f"RESULT {i}")
    print("-" * 60)

    print(f"Source : {source}")

    # =====================================
    # STD 11 / STD 12
    # =====================================

    if source in [
        "std11_textbook",
        "std12_textbook"
    ]:

        print(
            f"Unit   : {metadata.get('unit')}"
        )

        print(
            f"Title  : {metadata.get('title')}"
        )

        print(
            f"Section: {metadata.get('section')}"
        )

    # =====================================
    # PEDAGOGY 1
    # =====================================

    elif source == "pedagogy_1":

        print(
            f"Unit   : {metadata.get('unit')}"
        )

        print(
            f"Topic  : {metadata.get('topic')}"
        )

        print(
            f"Topic# : {metadata.get('topic_number')}"
        )

    # =====================================
    # PEDAGOGY 2
    # =====================================

    elif source == "pedagogy_2":

        print(
            f"Block  : {metadata.get('block')}"
        )

        print(
            f"Unit   : {metadata.get('unit')}"
        )

        print(
            f"Title  : {metadata.get('title')}"
        )

    print()
    print(doc.page_content[:500])
    print()