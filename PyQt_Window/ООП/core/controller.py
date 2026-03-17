from Flask_Site.repo_sqlite import SqliteNotesRepo


class DiaryController:
    def __init__(self):
        self.repo = SqliteNotesRepo()

    def get_notes(self):
        return self.repo.list_all()

    def get_note(self, note_id: int):
        return self.repo.get(note_id)

    def create_note(self):
        return self.repo.create()

    def update_note(self, note_id: int, title: str, body: str):
        self.repo.update(note_id, title, body)

    def delete_note(self, note_id: int):
        self.repo.delete(note_id)