import re


def find_position(
    text: str,
    pattern: str
):
    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.start()

    return -1


def split_read_block(
    read_block: str
):

    glossary_pos = find_position(
        read_block,
        r"Glossary"
    )

    comprehension_pos = find_position(
        read_block,
        r"Comprehension"
    )

    if glossary_pos == -1:

        raise ValueError(
            "Glossary not found"
        )

    if comprehension_pos == -1:

        raise ValueError(
            "Comprehension not found"
        )

    return {

        "content": read_block[
            :glossary_pos
        ].strip(),

        "glossary": read_block[
            glossary_pos:
            comprehension_pos
        ].strip(),

        "comprehension": read_block[
            comprehension_pos:
        ].strip()
    }