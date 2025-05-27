BOOK_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "description", "pageCount", "excerpt", "publishDate"],
    "properties": {
        "id":          {"type": "integer"},
        "title":       {"type": ["string", "null"]},
        "description": {"type": ["string", "null"]},
        "pageCount":   {"type": "integer"},
        "excerpt":     {"type": ["string", "null"]},
        "publishDate": {"type": "string", "format": "date-time"}
    },
    "additionalProperties": False
}

BOOK_LIST_SCHEMA = {"type": "array", "items": BOOK_SCHEMA}
