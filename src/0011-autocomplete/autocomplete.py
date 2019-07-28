#!/usr/bin/python3
# Questioner: Twitter
# Difficulty: Medium

"""
Implement an autocomplete system. That is, given a query string s and a set of all possible query strings, return all strings in the set that have s as a prefix.

For example, given the query string de and the set of strings [dog, deer, deal], return [deer, deal].

Hint: Try preprocessing the dictionary into a more efficient data structure to speed up queries.
"""

def simple(q, arr, prep=None):
  return [e for e in arr if e.startswith(q)]

# ------------------------------------------------------------------------------

import math

def narrow_prep(arr):
  return sorted(arr)

def narrow(q, arr, prep=None):
  if prep == None:
    prep = narrow_prep(arr)
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

# ------------------------------------------------------------------------------

TERMINATOR = '\0'

def tree_prep(arr):
  root = dict()
  for s in arr:
    node = root
    for c in s:
      if not c in node:
        node[c] = dict()
      node = node[c]
    node[TERMINATOR] = True
  return root

def tree(q, arr, prep=None):
  if prep == None:
    prep = tree_prep(arr)
  node = prep
  for c in q:
    if c in node:
      node = node[c]
    else:
      return []
  res = tree_result(node)
  return map(lambda s: q + s, res)

def tree_result(node):
  res = []
  for c in node:
    if c == TERMINATOR:
      res.append("")
    else:
      inner_res = tree_result(node[c])
      res.extend(map(lambda s: c + s, inner_res))
  return res

# ------------------------------------------------------------------------------

if __name__ == '__main__':
  import random
  random.seed(a="almost random")
  tests = [
    (["dog", "deer", "deal"], {"de": ["deal", "deer"]})
  ]
  def word(max_length = 7): return ''.join(random.choices('abcde', k=random.randint(1, max_length)))
  for i in range(50):
    arr = set()
    for j in range(random.randint(10, 250)):
      arr.add(word())
    test = dict()
    for j in range(50):
      q = word(4)
      expected = sorted(simple(q, arr))
      test[q] = expected
    tests.append((arr, test))

  func = tree
  prep_func = tree_prep

  for i, test in enumerate(tests):
    arr = test[0]
    prep = prep_func(arr)
    for q in test[1]:
      expected = test[1][q]
      actual = sorted(func(q, arr, prep))
      if expected != actual:
        print('\n'.join([f"{i}: {v}" for i, v in enumerate(sorted(arr))]))
      assert expected == actual, f"Test {i} failed: q: {q}\n\texpected: {expected}\n\tactual   : {actual}"
  print("All tests passed")
