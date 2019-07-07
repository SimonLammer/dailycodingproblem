#!/usr/bin/python3
# Questioner: Google
# Difficulty: Easy
"""
A unival tree (which stands for "universal value") is a tree where all nodes under it have the same value.

Given the root to a binary tree, count the number of unival subtrees.

For example, the following tree has 5 unival subtrees:

   0
  / \
 1   0
    / \
   1   0
  / \
 1   1
"""

class Node:
  def __init__(self, value, left = None, right = None):
    self.value = value
    self.left = left
    self.right = right
  
  def __repr__(self):
    return f"{self.value} ({self.left}, {self.right})"

def count(root):
  def count_(root):
    lc = 0
    lv = None
    if root.left:
      lc, lv = count_(root.left)
    rc = 0
    rv = None
    if root.right:
      rc, rv = count_(root.right)
    count = lc + rc
    value = False
    if (lv == None or (type(lv) is not bool and lv == root.value)) and (rv == None or (type(rv) is not bool and rv == root.value)):
      count += 1
      value = root.value
    return count, value
  return count_(root)[0]

if __name__ == '__main__':
  for i, test in enumerate([
    (5, Node(0, Node(1), Node(0, Node(1, Node(1), Node(1)), Node(0)))),
    (3, Node(0, Node(0), Node(0, Node(1), Node(1))))
  ]):
    actual = count(test[1])
    assert actual == test[0], f"Test {i} failed:\n\texpected: {test[0]}\n\tactual:   {actual}"
  print("All tests succeeded")
