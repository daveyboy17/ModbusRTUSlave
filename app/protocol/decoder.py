def describe(frame: bytes):
    """Returns a str describing the frame if valid."""
    if len(frame) < 2:
        return ""

    function = frame[1]

    names = {
        3: "Read Holding Registers",
        4: "Read Input Registers",
        6: "Write Single Register",
        16: "Write Multiple Registers"
    }

    description = names.get(
        function,
        "Unknown Function"
    )

    return (
        f"Slave: {frame[0]}\n"
        f"Function: {function} "
        f"({description})"
    )