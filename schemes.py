from pydantic import BaseModel
from typing import Optional


class Note(BaseModel):
    text: str
    secret: str
    note_hash: Optional[str] = None  # Результат, ссылка на готовую записку


class NotesList(BaseModel):
    all_notes: list[Note] = []


class NoteID(BaseModel):
    note_id: str
    note_secret: str