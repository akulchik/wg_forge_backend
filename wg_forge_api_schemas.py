CAT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "color": {"type": "string"},
        "tail_length": {"type": "integer"},
        "whiskers_length": {"type": "integer"}
    },
    "required": ["name", "color", "tail_length", "whiskers_length"],
}
