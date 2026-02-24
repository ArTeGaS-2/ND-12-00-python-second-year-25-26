from core.models import Note


class DiaryController:
    def __init__(self, storage):
        self.storage = storage

    def get_notes(self):
        return self.storage.get_all()

    def create_note(self, title="Новий запис"):
        note = Note(title, "")
        self.storage.add(note)
        return note