def parse_command(raw: str):
    """
    Split raw input into command and argument.
    Returns (command, argument) or ("NO_OP", None) if invalid.
    """

    # handle empty input
    if not raw:
        return "NO_OP", None

    # parse raw input into command and argument
    parts = raw.strip().split(maxsplit=1)
    command = parts[0].upper() # ensure uppercase
    argument = parts[1] if len(parts) > 1 else None

    return command, argument
