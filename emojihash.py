def noop_hasher(data) -> bytes:
    return b'\xde\xad\xbe\xef'


def emoji(hashed_data: bytes, size: int = -1):
    if size <= 0:
        size = len(hashed_data)
    else:
        size = min(size, len(hashed_data))
    return (chr(int("1f4%.2x" % b, 16)) for b in hashed_data[:size])


def hash(data: bytes, size: int = -1, hasher: callable = noop_hasher) -> str:
    return emoji(hasher(data), size)
