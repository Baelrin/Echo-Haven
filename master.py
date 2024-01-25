from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemes import Note, NotesList, NoteID
from cipher import get_note_id

app = FastAPI()
templates = Jinja2Templates(directory="templates")

notes_list = NotesList()

@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    """
    Handle requests to the home page.

    Args:
    - request (Request): The request object.

    Returns:
    - HTMLResponse: Rendered home page with count of notes.
    """
    # Render the home page with the number of notes
    return templates.TemplateResponse("index.html", {
        "request": request,
        "notes_count": len(notes_list.all_notes)
    })


class NoteManager:
    """
    A manager for note operations, including note creation and retrieval.
    """

    def __init__(self):
        """
        Initialize the NoteManager with an empty notes list.
        """
        self.notes_list = NotesList()

    def create_note(self, note_data: Note):
        """
        Create a new note with the provided data and add it to the notes list.

        Args:
        - note_data (Note): The note data structure to add.

        Returns:
        - dict: A response with an 'ok' status and the generated note ID.
        """
        # Generate a unique ID for the note using the note content and a secret
        note_id = get_note_id(text=note_data.text, salt=note_data.secret)
        note_data.note_hash = note_id  # Store the generated note ID in note_data

        # Add the note with its ID to the notes list
        self.notes_list.all_notes.append(note_data)
        return {"response": "ok", "note_id": note_id}

    def get_note(self, note_data: NoteID):
        """
        Retrieve a note by its ID and secret, then remove it from the list.

        Args:
        - note_data (NoteID): The identifier with the note ID and secret.

        Returns:
        - dict: A response with an 'ok' status and the note's text.

        Raises:
        - ValueError: If the note with the given ID and secret doesn't exist.
        """
        # Find the index of the note with the matching ID and secret, if it exists
        note_index = next((i for i in range(len(self.notes_list.all_notes)) if note_data.note_id == self.notes_list.all_notes[i].note_hash and note_data.note_secret == self.notes_list.all_notes[i].secret), None)

        if note_index is None:
            raise ValueError("Such a note does not exist")  # No matching note was found

        note = self.notes_list.all_notes[note_index]  # Retrieve the note
        self.notes_list.all_notes.remove(note)  # Remove the note from the list

        return {"response": "ok", "note_final_text": note.text}


@app.get("/note_page/{note_text}", response_class=HTMLResponse)
async def get_result_note(request: Request, note_text: str):
    """
    Serve the note page for a given note text.

    Args:
    - request (Request): The request object.
    - note_text (str): The text of the note to display.

    Returns:
    - HTMLResponse: Rendered page showing the note.
    """
    # Render the note page with the provided note_text
    return templates.TemplateResponse("note_page.html", {
        "request": request,
        "note_text": note_text
    })