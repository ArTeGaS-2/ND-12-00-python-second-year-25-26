"""Результат: програма має вивести суму цифр числа."""

n = int(input("Введи число: "))

total = 0
while n > 0:
    total += n % 10

return total
