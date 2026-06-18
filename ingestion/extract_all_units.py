import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ingestion.extract_unit import extract_unit


for unit_number in range(1, 11):

    try:

        extract_unit(unit_number)

        print(
            f"✅ Unit {unit_number} done"
        )

    except Exception as e:

        print(
            f"❌ Unit {unit_number} failed"
        )

        print(e)