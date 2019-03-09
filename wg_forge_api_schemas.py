CAT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "color": {"type": "string"},
        "tail_length": {"type": "number"},
        "whiskers_length": {"type": "number"}
    },
    "required": ["name", "color", "tail_length", "whiskers_length"],
}
