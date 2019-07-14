#!/usr/bin/python3
# Questioner: Twitter
# Difficulty: Medium

"""
Implement an autocomplete system. That is, given a query string s and a set of all possible query strings, return all strings in the set that have s as a prefix.

For example, given the query string de and the set of strings [dog, deer, deal], return [deer, deal].

Hint: Try preprocessing the dictionary into a more efficient data structure to speed up queries.
"""

def simple(arr, q):
  return [e for e in arr if e.startswith(q)]

if __name__ == '__main__':
  for i, test in enumerate([
    (["deer", "deal"], (["dog", "deer", "deal"], "de"))
  ]):
    expected = test[0]
    actual = simple(*test[1])
    assert expected == actual, f"Test {i} failed: q: {test[1][1]}, arr: {test[1][0]}\n\texpected: {expected}\n\tactual   : {actual}"
  print("All tests passed")
