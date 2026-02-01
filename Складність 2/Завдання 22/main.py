"""Результат: програма має видалити від'ємні числа зі списку."""

nums = [3, -1, 4, -2, 5]

for x in nums:
    if x < 0:
        nums.remove(x)

bad = int("12a")
print(nums)
