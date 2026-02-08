"""Результат: програма має вивести добуток чисел від 1 до n."""

n = int(input("Введи n: "))

prod = 0
for i in range(1, n + 1):
    prod *= i

print("Добуток: " + prod)
