#!/usr/bin/python3
# Questioner: Stripe
# Difficulty: Hard
"""
Given an array of integers, find the first missing positive integer in linear time and constant space. In other words, find the lowest positive integer that does not exist in the array. The array can contain duplicates and negative numbers as well.

For example, the input [3, 4, -1, 1] should give 2. The input [1, 2, 0] should give 3.

You can modify the input array in-place.
"""

def main(arr):
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
