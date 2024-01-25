import hashlib

def get_note_id(text: str, salt: str) -> str:
    """
    Generate a unique SHA-256 hash for a given text with a salt.

    This function takes a string and a salt, combines them, and returns the SHA-256 hash
    of their combination. This is typically used to create a unique ID for a piece of text
    where the salt is a constant or user-specific string that adds an additional layer of uniqueness.

    Parameters:
    text (str): The text string to be hashed.
    salt (str): The salt string that is concatenated to the text to create a unique hash.

    Returns:
    str: A SHA-256 hash of the text and salt.
    """
    # Encode the text and salt to byte strings and concatenate them
    combined_bytes = text.encode("UTF-8") + salt.encode("UTF-8")

    return hashlib.sha256(combined_bytes).hexdigest()