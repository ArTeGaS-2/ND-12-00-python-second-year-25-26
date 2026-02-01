"""Результат: програма має вивести суму елементів списку плюс 5."""

def sum_list(nums):
    total = 0
    for n in nums:
        total += n
    print("Сума:", total)

nums = [1, 2, 3]
result = sum_list(nums)
print("Разом:", result + 5
