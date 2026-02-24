from core.models import Note


class InMemoryStorage:
    def __init__(self):
        self.notes = [
            Note("Запис 1", ""),
            Note("Запис 2", ""),
            Note("Запис 3", "")
        ]

    def get_all(self):
        return self.notes

    def add(self, note: Note):
        self.notes.append(note)