BOOK_PAYLOAD = {
    "id": 999,
    "title": "Pytest JSON-Schema Demo",
    "description": "Testing JSON schema validation",
    "pageCount": 0,
    "excerpt": "Once upon a test…",
    "publishDate": "2025-05-27T00:00:00Z"
}

INVALID_BOOK_PAYLOAD = {
    "id": 0,
    "title": "Pytest JSON-Schema Demo",
    "description": "Testing JSON schema validation",
    "pageCount": "ZERO",  # Invalid type, should be integer
    "excerpt": "Once upon a test…",
    "publishDate": "2025-05-27T00:00:00Z"
}
