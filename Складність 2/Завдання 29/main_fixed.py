"""Результат: програма має вивести суму чисел у списку."""

def sum_list(nums):
    total = 0
    for n in nums:
        total += n
        return total

nums = [1, 2, 3]
print("Сума:", sum_list(nums))

"""
Помилка: пропущена двокрапка після керуючої конструкції.
Виправлення: додано двокрапку після if/for/while/def.
"""
