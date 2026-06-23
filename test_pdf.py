from ingestion.load_std11_unit import (
    load_std11_unit
)

from utils.std11_read_finder import (
    find_read_positions
)

for unit in [1, 5, 9, 10]:

    text = load_std11_unit(unit)

    positions = find_read_positions(text)

    print(
        f"Unit {unit} -> {len(positions)} reads"
    )