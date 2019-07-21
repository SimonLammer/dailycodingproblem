#!/usr/bin/python3
# Questioner: Twitter
# Difficulty: Medium

"""
Implement an autocomplete system. That is, given a query string s and a set of all possible query strings, return all strings in the set that have s as a prefix.

For example, given the query string de and the set of strings [dog, deer, deal], return [deer, deal].

Hint: Try preprocessing the dictionary into a more efficient data structure to speed up queries.
"""

def simple(q, arr):
  return [e for e in arr if e.startswith(q)]

# -----------------------------------------------------------------------

import math

def narrow(q, arr):
  prep = sorted(arr) # This would only be done once for arr, with different q
  low, high = narrow_search(q, prep)
  return prep[low : high] if low < len(arr) else []

def narrow_search(q, arr):
  low = 0
  high = len(arr)
  for i in range(len(q)):
    midh = high
    while True:
      midl = low + int((midh - low) / 2)
      if low == midl:
        break
      if len(arr[midl]) <= i or arr[midl][i] < q[i]:
        low = midl
      else:
        midh = midl
    if len(arr[midl]) <= i or arr[midl][i] < q[i]:
      low += 1
      if len(arr) <= low:
        break
      midl += 1
    while True:
      midh = midl + int((high - midl) / 2)
      if midl == midh:
        break
      if len(arr[midh]) <= i or arr[midh][i] <= q[i]:
        midl = midh
      else:
        high = midh
    if len(arr[midh]) > i and arr[midh][i] > q[i]:
      high -= 1
    if low == high:
      break
  return low, high

if __name__ == '__main__':
  import random
  random.seed(a="almost random")
  tests = [
    (["deal", "deer"], ("de", ["dog", "deer", "deal"]))
  ]
  def word(max_length = 7): return ''.join(random.choices('abcde', k=random.randint(1, max_length)))
  for i in range(50):
    arr = []
    for j in range(random.randint(5, 50)):
      arr.append(word())
    for j in range(50):
      q = word(4)
      expected = simple(q, arr)
      tests.append((expected, (q, arr)))
  for i, test in enumerate(tests):
    expected = sorted(test[0])
    actual = sorted(narrow(*test[1]))
    if expected != actual:
      print('\n'.join([f"{i}: {v}" for i, v in enumerate(sorted(test[1][1]))]))
    assert expected == actual, f"Test {i} failed: q: {test[1][0]}, arr: {test[1][1]}\n\texpected: {expected}\n\tactual   : {actual}"
  print("All tests passed")
