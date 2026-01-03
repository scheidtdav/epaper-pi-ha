import board


def deserialize(serialized: str):
    try:
        return getattr(board, serialized)
    except AttributeError:
        raise ValueError(f"Invalid pin name: {serialized}")
