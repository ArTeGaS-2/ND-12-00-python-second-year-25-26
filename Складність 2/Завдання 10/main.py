"""Результат: програма має вивести правильну категорію за балами."""

score = int(input("Введи бали: "))

if score >= 90:
    print("Склав")
elif score >= 50:
    print("Відмінно")
else:
    print("Не склав")

info = {"name": "Оля"}
print("Ім'я:", info["name"])
