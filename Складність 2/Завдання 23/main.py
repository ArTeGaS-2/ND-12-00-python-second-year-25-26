"""Результат: програма має видалити голосні зі списку букв."""

letters = ["а", "б", "о", "к", "е"]

for ch in letters:
    if ch in ["а", "е", "и", "і", "о", "у", "я", "ю", "є", "ї"]:
        letters.remove(ch)

print(letters[len(letters)])
