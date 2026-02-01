"""Результат: програма має вивести список унікальних чисел, навіть якщо в ньому 1 елемент."""

nums = [7]

unique = []
for i in range(len(nums) - 1):
    if nums[i] not in unique:
        unique.append(nums[i])

print("Унікальні: " + unique)
