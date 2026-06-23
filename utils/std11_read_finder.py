import re


def find_read_positions(
    unit_text: str
):

    matches = list(
        re.finditer(
            r"Read\s+[123]",
            unit_text,
            flags=re.IGNORECASE
        )
    )

    return [
        match.start()
        for match in matches
    ]