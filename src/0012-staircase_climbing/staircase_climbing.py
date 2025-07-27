#!/usr/bin/python3
# Questioner: Amazon
# Difficulty: Hard

"""
There exists a staircase with N steps, and you can climb up either 1 or 2 steps at a time. Given N, write a function that returns the number of unique ways you can climb the staircase. The order of the steps matters.

For example, if N is 4, then there are 5 unique ways:
- 1, 1, 1, 1
- 2, 1, 1
- 1, 2, 1
- 1, 1, 2
- 2, 2

What if, instead of being able to climb 1 or 2 steps at a time, you could climb any number from a set of positive integers X? For example, if X = {1, 3, 5}, you could climb 1, 3, or 5 steps at a time.
"""

# -----------------------------------------------------------------------------

def solution_brute(height, step_sizes = [1, 2], perm = None, path = []):
  if (height < 0):
    return 0
  elif height == 0:
    # print(path)
    return 1
  else:
    return sum([solution_brute(height - step, step_sizes=step_sizes, path=[*path, step]) for step in step_sizes])

import functools

@functools.lru_cache(maxsize = 512)
def solution_brute_cached(height, step_sizes = [1, 2], perm = None):
  if (height < 0):
    return 0
  elif height == 0:
    return 1
  else:
    return sum([solution_brute_cached(height - step, step_sizes=step_sizes) for step in step_sizes])

# -----------------------------------------------------------------------------

import math

def permutations(f1, f2):
  """
  How many ways are there to put f2 items between f1 items?

  Example:
    f1 = 4:                     a   a   a   a   
    items can be placed here: ^   ^   ^   ^   ^
    
    if f2 = 2, items can be placed at these locations (each index specifying the place of one item):
      (0,0), (0,1), (0,2), (0,3), (0,4),
             (1,1), (1,2), (1,3), (1,4),
                    (2,2), (2,3), (2,4),
                           (3,3), (3,4),
                                  (4,4)
      
    Others like (1,0) don't count since the items are equivalent and therefore (0,1) looks exactly like (1,0)
  """

  # print('permutations', f1, f2)

  if f1 == 0 or f2 == 0:
    return 1

  res = 0
  working = True
  counter = [0] * f2
  while working:
    while counter[-1] <= f1:
      res += 1
      print(counter) # Print all possibilities
      counter[-1] += 1
    working = False
    for i in range(f2 - 1, -1, -1):
      if counter[i] < f1:
        counter[i] += 1
        for j in range(i + 1, f2):
          counter[j] = counter[i]
        # print("\t\t.")
        working = True
        break
  return res

def print_permutations_table(f1_max, f2_max, just = 6, perm = permutations):
  """print_permutations_table(10, 10)
  f1\f2   1        2        3        4        5        6        7        8        9        10     
     1:      2        3        4        5        6        7        8        9       10       11   
     2:      3        6       10       15       21       28       36       45       55       66   
     3:      4       10       20       35       56       84      120      165      220      286   
     4:      5       15       35       70      126      210      330      495      715     1001   
     5:      6       21       56      126      252      462      792     1287     2002     3003   
     6:      7       28       84      210      462      924     1716     3003     5005     8008   
     7:      8       36      120      330      792     1716     3432     6435    11440    19448   
     8:      9       45      165      495     1287     3003     6435    12870    24310    43758   
     9:     10       55      220      715     2002     5005    11440    24310    48620    92378   
    10:     11       66      286     1001     3003     8008    19448    43758    92378   184756
  """

  print("f1\\f2 ", end = '')
  for i in range(1, f2_max + 1):
    print(f"{str(i).center(just)}   ", end = '')
  for i in range(1, f1_max + 1):
    print(f"\n{str(i).rjust(4)}: ", end = '')
    for j in range(1, f2_max + 1):
      print(f"{str(perm(i,j)).rjust(just)}   ", end='')
  print()

@functools.lru_cache(maxsize=512)
def binom(n, k):
  return math.factorial(n) // math.factorial(k) // math.factorial(n - k)

def permutations2(f1, f2):
  """
  The permutations_table is very similar to Pascal's triangle!
  """

  # if f2 < f1:
  #   tmp = f2
  #   f2 = f1
  #   f1 = tmp
  # assert(f1 <= f2)
  # return binom(f2 + f1, f1)

  return binom(f1 + f2, min(f1, f2))

def solution_thoughtful(height, step_sizes = (1, 2), perm = permutations2):
  length = len(step_sizes)
  max_step_factor = [height // step for step in step_sizes]
  combination = [f for f in max_step_factor]
  possibilities = 0
  while combination[0] >= 0:
    k = 0
    for c, s in zip(combination, step_sizes):
      k += c * s
    if k == height:
      if length == 1:
        possibilities += 1
      else:
        p = 1
        hold = combination[0]
        magnitude = combination[0]
        for i in range(1, length):
          if combination[i] == 0:
            continue
          if hold == 0:
            hold = combination[i]
            magnitude = combination[i]
          else:
            p = (p if p != 1 else 1) * perm(magnitude, combination[i])
            magnitude += combination[i]
        possibilities += p
        # print('combination: ', combination, '->', p)
    i = length - 1
    while True:
      combination[i] -= 1
      if combination[i] >= 0 or i <= 0:
        break
      combination[i] = max_step_factor[i]
      i -= 1
  return possibilities

# -----------------------------------------------------------------------------

SOLUTIONS = {
  (1, (1, 2)): 1, # 1
  (2, (1, 2)): 2, # 1,1 ; 2
  (3, (1, 2)): 3, # 1,1,1 ; 1,2 ; 2,1
  (4, (1, 2)): 5, # see task description

  # Solutions below were calculated with solution_brute
  (1, (1, 2)): 1,
  (2, (1, 2)): 2,
  (3, (1, 2)): 3,
  (4, (1, 2)): 5,
  (5, (1, 2)): 8,
  (6, (1, 2)): 13,
  (7, (1, 2)): 21,
  (8, (1, 2)): 34,
  (9, (1, 2)): 55,
  (10, (1, 2)): 89,
  (11, (1, 2)): 144,
  (12, (1, 2)): 233,
  (13, (1, 2)): 377,
  (14, (1, 2)): 610,
  (15, (1, 2)): 987,
  (16, (1, 2)): 1597,
  (17, (1, 2)): 2584,
  (18, (1, 2)): 4181,
  (19, (1, 2)): 6765,
  (20, (1, 2)): 10946,
  (21, (1, 2)): 17711,
  (22, (1, 2)): 28657,
  (23, (1, 2)): 46368,
  (24, (1, 2)): 75025,
  (25, (1, 2)): 121393,
  (26, (1, 2)): 196418,
  (27, (1, 2)): 317811,
  (28, (1, 2)): 514229,
  (29, (1, 2)): 832040,
  (30, (1, 2)): 1346269,
  (31, (1, 2)): 2178309,
  (32, (1, 2)): 3524578,
  (1, (1, 2, 3)): 1,
  (2, (1, 2, 3)): 2,
  (3, (1, 2, 3)): 4,
  (4, (1, 2, 3)): 7,
  (5, (1, 2, 3)): 13,
  (6, (1, 2, 3)): 24,
  (7, (1, 2, 3)): 44,
  (8, (1, 2, 3)): 81,
  (9, (1, 2, 3)): 149,
  (10, (1, 2, 3)): 274,
  (11, (1, 2, 3)): 504,
  (12, (1, 2, 3)): 927,
  (13, (1, 2, 3)): 1705,
  (14, (1, 2, 3)): 3136,
  (15, (1, 2, 3)): 5768,
  (16, (1, 2, 3)): 10609,
  (17, (1, 2, 3)): 19513,
  (18, (1, 2, 3)): 35890,
  (19, (1, 2, 3)): 66012,
  (20, (1, 2, 3)): 121415,
  (21, (1, 2, 3)): 223317,
  (22, (1, 2, 3)): 410744,
  (23, (1, 2, 3)): 755476,
  (24, (1, 2, 3)): 1389537,
  (25, (1, 2, 3)): 2555757,
}

def test(func):
  for (height, step_sizes), solution in SOLUTIONS.items():
    actual = func(height, step_sizes)
    if actual != solution:
      print(f"There are {str(solution)} ways to climb {str(height)} steps with step sizes {','.join(map(str, step_sizes))} but the algorithm computed {str(actual)}!")

if __name__ == '__main__':
  # print_permutations_table(10, 10)
  # print_permutations_table(10, 10, perm=permutations2)
  # exit(1)

  # print(solution_thoughtful(4, [1, 2, 3], perm=permutations))

  # exit(1)

  # for i in range(1, 27):
  #   print(i, solution_brute_cached(i, (1, 2, 3), perm=permutations2))
  #   # print('\n')

  # exit(1)

  import timeit

  print("Simple tests")
  # print("brute",        timeit.timeit(lambda: test(solution_brute),        number=3))
  print("brute_cached", timeit.timeit(lambda: test(solution_brute_cached), number=50))
  print("thoughtful",   timeit.timeit(lambda: test(solution_thoughtful),   number=50))

  def test2(func, max_height = 65, step_sizes = (1, 2, 3)):
    for height in range(max_height):
      func(height, step_sizes, perm=permutations2)

  print("\nharder tests")
  print("brute_cached", timeit.timeit(lambda: test2(solution_brute_cached), number=30))
  print("thoughtful",   timeit.timeit(lambda: test2(solution_thoughtful),   number=30))