"""
Given an array of integers, return a new array such that each element at index i of the new array is the product of all the numbers in the original array except the one at i.

For example, if our input was [1, 2, 3, 4, 5], the expected output would be [120, 60, 40, 30, 24]. If our input was [3, 2, 1], the expected output would be [2, 3, 6].

Follow-up: what if you can't use division?
"""

arr = [1, 2, 3, 4, 5]

def main(arr):
  res = [1] * len(arr)
  product = 1
  for i in range(1, len(arr)):
    product *= arr[i - 1]
    res[i] = product
  product = 1
  for i in reversed(range(0, len(arr) - 1)):
    product *= arr[i + 1]
    res[i] *= product
  return res

def with_division(arr):
  # This fails when the array contains 0

  product = 1
  for num in arr:
    product *= num
  return map(lambda e: product / e, arr)

if __name__ == '__main__':
  print(arr, main(arr))