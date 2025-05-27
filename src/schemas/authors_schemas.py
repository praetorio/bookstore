AUTHOR_SCHEMA = {
    "type": "object",
    "required": ["id", "idBook", "firstName", "lastName"],
    "properties": {
        "id":        {"type": "integer"},
        "idBook":    {"type": "integer"},
        "firstName": {"type": ["string", "null"]},
        "lastName":  {"type": ["string", "null"]}
    },
    "additionalProperties": False
}

AUTHOR_LIST_SCHEMA = {"type": "array", "items": AUTHOR_SCHEMA}
