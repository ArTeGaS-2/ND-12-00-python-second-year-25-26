"""Результат: програма має вивести найбільше число у списку."""

def max_in_list(nums):
    max_num = nums[0]
    for n in nums:
        if n > max_num:
            max_num = n
        return max_num

nums = [2, 5, 3]
print("Максимум:", max_in_list(nums))

def loop():
    return loop()

loop()
