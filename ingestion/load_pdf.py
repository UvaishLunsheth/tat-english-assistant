from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

PDF_PATH = Path("data/12-English.pdf")

loader = PyPDFLoader(str(PDF_PATH))
documents = loader.load()

print(f"Total Pages: {len(documents)}")

for i in range(10):

    print("\n" + "=" * 50)
    print(f"PAGE {i+1}")
    print("=" * 50)

    print(
        repr(
            documents[i].page_content[:300]
        )
    )