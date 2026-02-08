"""Результат: програма має порахувати кількість голосних у слові."""

def count_vowels(text):
    vowels = "аеєиіїоуюя"
    count = 0
    for ch in text:
        if ch in vowels:
            count += 1
        return count

word = input("Введи слово: ")
print("Голосних:", count_vowels(word))
  print("Готово")
