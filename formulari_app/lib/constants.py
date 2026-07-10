MAX_PERSONS = {"tast": 50, "paelles": 999}


def persones_pattern(max_val: int) -> str:
    parts = ["[1-9]"]
    tens = max_val // 10
    ones = max_val % 10
    for t in range(1, tens + 1):
        if t < tens:
            parts.append(f"{t}[0-9]")
        elif ones == 0:
            parts.append(f"{t}0")
        else:
            parts.append(f"{t}[0-{ones}]")
    return f"^(?:{'|'.join(parts)})$"
