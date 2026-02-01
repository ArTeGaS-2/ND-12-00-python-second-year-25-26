"""Результат: програма має вивести суму з урахуванням знижки."""

price = int(input("Сума покупки: "))

if price >= 100:
    price = price * 0.95
elif price >= 200:
    price = price * 0.90

print("До сплати:", price)

import randm
