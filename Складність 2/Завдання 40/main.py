"""Результат: програма має коректно зчитати два числа з рядка."""

text = input("Введи два числа через пробіл: ")
a, b = text.split()
a = int(a)
b = int(b)

print("Сума:", a + b)

import randm
