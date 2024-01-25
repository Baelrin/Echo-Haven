from pydantic import BaseModel
from typing import Optional

class Note(BaseModel):
    """
    Represents a note in the system with its contents, secrets and an optional hash.
    """
    text: str                    # The actual text content of the note
    secret: str                  # A secret associated with the note for security purposes
    note_hash: Optional[str] = None  # An optional hash to uniquely identify the note


class NotesList(BaseModel):
    """
    A list holding instances of Note objects.
    """
    all_notes: list[Note] = []  # Initializes an empty list to store Note instances


class NoteID(BaseModel):
    """
    This model is used to represent a unique identifier for a Note with its associated secret.
    """
    note_id: str        # A unique identifier for the note
    note_secret: str    # The secret associated with the note for authentication purposes