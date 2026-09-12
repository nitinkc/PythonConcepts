def capitalize_words(text: str | None) -> str | None:
    if text is None:
        return None
    if not isinstance(text, str):
        raise TypeError("text must be a string or None")
    return text.title()
