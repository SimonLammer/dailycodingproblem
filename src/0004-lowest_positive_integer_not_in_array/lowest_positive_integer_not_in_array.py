#!/usr/bin/python3
# Questioner: Stripe
# Difficulty: Hard
"""
Given an array of integers, find the first missing positive integer in linear time and constant space. In other words, find the lowest positive integer that does not exist in the array. The array can contain duplicates and negative numbers as well.

For example, the input [3, 4, -1, 1] should give 2. The input [1, 2, 0] should give 3.

You can modify the input array in-place.
"""

def main(arr):
  for i, num in enumerate(arr):
    if num < 1:
      arr[i] = len(arr) + 1
  for i, num in enumerate(arr):
    num = abs(num)
    if 0 < num and num <= len(arr):
      if num > i: # and num + 1 != i
        if arr[num - 1] > 0:
          arr[num - 1] = -arr[num - 1]
      else:
        arr[num - 1] = 0
  for i, num in enumerate(arr, 1):
    if num > 0:
      return i
  return len(arr) + 1


def linear_space(arr):
  # Fails with [8, 1, 10, 6, 2, 4, 0, 0, 12, 1] (returns 1 instead of 3)
  found_arr = [False] * len(arr)
  for num in arr:
    if 0 < num and num <= len(arr):
      found_arr[num - 1] = True
  for i, found in enumerate(found_arr, 1):
    if not found:
      return i
  return len(arr) + 1

def simple(arr):
  # Fails with [3, 1, 2, 12, -8, 10, 12, 11, 5, 7] (returns 1 instead of 4)
  # Fails with [4, 11, 2, 1, 3, 1, 0, 7, 5, -1] (returns 2 instead of 6)
  lowest_missing_int = 1
  found_new = True
  while found_new:
    found_new = False
    for num in arr:
      if num == lowest_missing_int:
        found_new = True
        lowest_missing_int += 1
  return lowest_missing_int


if __name__ == '__main__':
  assert main([3, 4, -1, 1]) == 2
  assert main([1, 2, 0]) == 3

  import random
  arr_size = 10
  arr = [0] * arr_size
  for i in range(1000):
    for j in range(arr_size):
      arr[j] = random.randint(0, (int(arr_size * 5 / 4)))
      if random.random() > 0.9:
        arr[j] = -arr[j]
    old_arr = arr.copy()
    actual = main(arr)
    expected = simple(arr)
    if actual != expected:
      print(f"{old_arr} -> {actual} (instead of {expected})")
      import pdb; pdb.set_trace()
