#!/usr/bin/python3
# Questioner: Airbnb
# Difficulty: Hard
"""
Given a list of integers, write a function that returns the largest sum of non-adjacent numbers. Numbers can be 0 or negative.

For example, [2, 4, 6, 2, 5] should return 13, since we pick 2, 6, and 5. [5, 1, 1, 5] should return 10, since we pick 5 and 5.

Follow-up: Can you do this in O(N) time and constant space?
"""

def simple(arr):
  def simple_(arr, start = 0):
    l = len(arr) - start
    if l == 0:
      return 0
    elif l == 1:
      return max(0, arr[start])
    elif l == 2:
      return max(0, max(arr[start:]))
    elif l > 2:
      return max(
        max(0, arr[start]) + simple_(arr, start + 2),
        max(0, arr[start + 1]) + simple_(arr, start + 3))
    else:
      raise Exception("ERROR")

  return calc(arr, simple_) 

def calc(arr, f):
  m = arr[0]
  allneg = True
  for i in range(len(arr)):
    if arr[i] > m:
      m = arr[i]
    if arr[i] > 0:
      allneg = False
  if allneg:
    return m
  else:
    return f(arr)

if __name__ == '__main__':
  for i, test in enumerate([
    (4, [1, 2, 3]),
    (13, [2, 4, 6, 2, 5]),
    (10, [5, 1, 1, 5]),
    (-3, [-5, -24, -65, -7, -3, -4, -6, -9])
  ]):
    actual = simple(test[1])
    if actual != test[0]:
      import pdb; pdb.set_trace()
      simple(test[1])
    assert actual == test[0], f"Test {i} failed: {test[1]}\n\texpected: {test[0]}\n\tactual:   {actual}"
  print("All tests passed")
