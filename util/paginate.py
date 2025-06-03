def next_offset(offset, limit, total):
    return offset + limit if offset + limit < total else None