#!/usr/bin/python3

# Questioner: Facebook
# Difficulty: Medium
"""
Given the mapping a = 1, b = 2, ... z = 26, and an encoded message, count the number of ways it can be decoded.

For example, the message '111' would give 3, since it could be decoded as 'aaa', 'ka', and 'ak'.

You can assume that the messages are decodable. For example, '001' is not allowed.
"""

def simple(text, index = 0, is_combination = False):
  if (index + 1) == len(text):
    return 1
  if is_combination:
    return simple(text, index + 1)
  possibilities = simple(text, index + 1, False)
  if isCombinable(text[index], text[index + 1]):
    possibilities += simple(text, index + 1, True)
  return possibilities

def isCombinable(a, b):
  return a == '1' or (a == '2' and ('0' <= b and b <= '6'))

if __name__ == '__main__':
  for i in [
    ('1', 1),
    ('11', 2),
    ('111', 3),
    ('1111', 5),
    ('11111', 8),
    ('1122', 5),
    ('111222', 3 * 3 + 2 * 2)
  ]:
    actual = simple(i[0])
    assert actual == i[1], f'text: {i[0]}\n\texpected: {i[1]}\n\tactual:   {actual}'
  print("All tests passed")
