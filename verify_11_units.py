import json
from pathlib import Path

# ==========================================
# PATHS
# ==========================================
PROJECT_ROOT = Path(__file__).resolve().parent
UNIT_DIR = PROJECT_ROOT / "data" / "std11_units"

if not UNIT_DIR.exists():
    print(f"Directory not found: {UNIT_DIR}")
    raise SystemExit

# ==========================================
# VERIFY UNITS
# ==========================================
print()
print("=" * 50)
print("UNIT VERIFICATION")
print("=" * 50)

# Grab all the json files and sort them
unit_files = sorted(UNIT_DIR.glob("*.json"))

for file_path in unit_files:
    # Open and load the JSON data from each file
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    name = file_path.name
    start = data.get("start_page", "N/A")
    end = data.get("end_page", "N/A")
    
    # Print it out nicely formatted
    print(f"{name: <15} | Start Page: {start: <4} | End Page: {end}")

print()
print("=" * 50)
print(f"Total units found: {len(unit_files)}")
print("=" * 50)