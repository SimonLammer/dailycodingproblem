#!/usr/bin/python3
# Asked by Google
"""
Given the root to a binary tree, implement serialize(root), which serializes the tree into a string, and deserialize(s), which deserializes the string back into the tree.

For example, given the following Node class

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

The following test should pass:

node = Node('root', Node('left', Node('left.left')), Node('right'))
assert deserialize(serialize(node)).left.left.val == 'left.left'
"""

SEPARATOR = '|'
NODE_START = '('
NODE_END = ')'

class Node:
  def __init__(self, val, left=None, right=None):
    self.val = val
    self.left = left
    self.right = right

def serialize(node):
  if node == None:
    return ""
  res = NODE_START
  if node.val != None:
    res += node.val.replace(SEPARATOR, SEPARATOR + SEPARATOR)
  res += SEPARATOR
  res += serialize(node.left)
  res += SEPARATOR
  res += serialize(node.right)
  res += NODE_END
  return res

def deserialize(s):
  if s == '':
    return None
  return deserialize_(s, 0)[0]

def deserialize_(s, start_index):
  if s[start_index] != NODE_START:
    raise ValueError("INVALID: expected node start at index " + str(start_index))
  print('s', start_index) # DEBUG
  first_separator_index = start_index
  while True:
    first_separator_index = s.index(SEPARATOR, first_separator_index)
    if s[first_separator_index + 1] == SEPARATOR:
      if s[first_separator_index + 2] == NODE_END:
        break # for deserialize("(||||)")
      else:
        first_separator_index += 2
    else:
      break
  node = Node(s[start_index + 1 : first_separator_index].replace(SEPARATOR + SEPARATOR, SEPARATOR))
  print(node.val) # DEBUG
  print('1', first_separator_index) # DEBUG
  second_separator_index = first_separator_index + 1
  if s[second_separator_index] != SEPARATOR:
    node.left, second_separator_index = deserialize_(s, second_separator_index)
    if s[second_separator_index] != SEPARATOR:
      raise ValueError("INVALID: expected separator at index " + str(second_separator_index))
  print('2', second_separator_index) # DEBUG
  end_index = second_separator_index + 1
  if s[end_index] != NODE_END:
    node.right, end_index = deserialize_(s, end_index)
    if s[end_index] != NODE_END:
      raise ValueError("INVALID: expected node end at index " + str(end_index))
  print('e', end_index) # DEBUG
  return node, end_index + 1

if __name__ == '__main__':
  node = Node('root', Node('left', Node('left.left')), Node('right'))
  print('012345678901234567890123456789012345678901234567890123456789')
  print(serialize(node))
  assert deserialize(serialize(node)).left.left.val == 'left.left'