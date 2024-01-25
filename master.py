from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemes import Note, NotesList, NoteID
from cipher import get_note_id

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Тут шаблоны
notes_list = NotesList()

@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "notes_count": len(notes_list.all_notes)
    })


class NoteManager:
    """Class responsible for managing notes."""

    def __init__(self):
        """Initialize the NoteManager with an empty notes list."""
        self.notes_list = NotesList()

    def create_note(self, note_data: Note):
        """Create a new note and add it to the notes list."""
        note_id = get_note_id(text=note_data.text, salt=note_data.secret)
        note_data.note_hash = note_id
        self.notes_list.all_notes.append(note_data)
        return {"response": "ok", "note_id": note_id}

    def get_note(self, note_data: NoteID):
        """Get a note from the notes list by its ID and secret."""
        for note in self.notes_list.all_notes:
            if (note_data.note_id == note.note_hash and
                    note_data.note_secret == note.secret):
                note_index = self.notes_list.all_notes.index(note)
                self.notes_list.all_notes.pop(note_index)
                return {"response": "ok", "note_final_text": note.text}
        raise ValueError("Such a note does not exist")

@app.get("/note_page/{note_text}", response_class=HTMLResponse)
async def get_result_note(request: Request, note_text: str):
    return templates.TemplateResponse("note_page.html", {
        "request": request,
        "note_text": note_text
    })