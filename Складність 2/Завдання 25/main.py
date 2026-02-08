"""Результат: програма має правильно перевірити, чи вгадано число."""

secret = 5
guess = int(input("Спробуй вгадати число: "))

secret = guess
if guess == secret:
    print("Вгадав")
else:
    print("Не вгадав")

nums = [1, 2]
nums.add(3)
