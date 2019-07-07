#!/usr/bin/python3

# Questioner: Facebook
# Difficulty: Medium
"""
Given the mapping a = 1, b = 2, ... z = 26, and an encoded message, count the number of ways it can be decoded.

For example, the message '111' would give 3, since it could be decoded as 'aaa', 'ka', and 'ak'.

You can assume that the messages are decodable. For example, '001' is not allowed.
"""

def advanced(text):
  """
  1: 1
  2: 2
  3: 3
  4: 5
  5: 8
  6: 13
  7: 21
  8: 34
  9: 55
  10: 89
  f(x): fibonacci(x+2)


  1111 ... 5, 3
  ----
  __--
  -__-
  --__
  ____


  11111 ... 8, 5
  -----
  __---
  -__--
  --__-
  ---__
  __-__
  -____
  ____-

  111111 ... 13, 8
  ------
  __----
  -__---
  --__--
  ---__-
  ----__
  ____--
  __-__-
  __--__
  -__-__
  --____
  -____-
  ______
  """
  text = ''
  for i in range(20):
    text += '1'
    print(f'{i+1}: {recursive(text)} {fibonacci(i + 2)}')
  pass

  possibilities = 0
  counter = 0
  char = None
  for index in range(len(text)):
    if text[index] == char:
      counter += 1
    else:
      if counter == 0:
        char = text[index]
      else:
        if (index + 1) < len(text) and isCombinable(text[index], text[index + 1]):
          pass # TODO

def fibonacci(n):
  if n < 1:
    return 0
  elif n == 1:
    return 1
  else:
    return fibonacci(n - 2) + fibonacci(n - 1)


def recursive(text, index = 0, is_combination = False):
  if (index + 1) == len(text):
    return 1
  if is_combination:
    return recursive(text, index + 1)
  possibilities = recursive(text, index + 1, False)
  if isCombinable(text[index], text[index + 1]):
    possibilities += recursive(text, index + 1, True)
  return possibilities

def isCombinable(a, b):
  return a == '1' or (a == '2' and ('0' <= b and b <= '6'))

if __name__ == '__main__':
  from random import randint, random
  for i in range(1000):
    text = str(randint(1, 9))
    for j in range(50):
      if not text[-1] in ['1', '2']:
        text += str(randint(1, 9))
      else:
        text += str(randint(0, 9 if text[-1] != '2' else 6))
    expected = recursive(text)
    actual = advanced(text)
    assert expected == actual, f"text: '{text}'\n\texpected: {expected}\n\tactual:   {actual}"
