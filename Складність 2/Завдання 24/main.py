"""Результат: програма має видалити парні числа зі списку."""

nums = [1, 2, 3, 4, 6]

for n in nums:
    if n % 2 == 0:
        nums.remove(n)

info = {"a": 1}
print(info["b"])
