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

def brute(height, step_sizes = [1, 2]):
  if (height < 0):
    return 0
  elif height == 0:
    return 1
  else:
    return sum([brute(height - step) for step in step_sizes])

# -----------------------------------------------------------------------------

SOLUTIONS = {
  (1, (1, 2)): 1, # 1
  (2, (1, 2)): 2, # 1,1 ; 2
  (3, (1, 2)): 3, # 1,1,1 ; 1,2 ; 2,1
  (4, (1, 2)): 5 # see task description
}

if __name__ == '__main__':
  for (height, step_sizes), solution in SOLUTIONS.items():
    actual = brute(height, step_sizes)
    if actual != solution:
      print(f"There are {str(solution)} ways to climb {str(height)} steps with step sizes {','.join(map(str, step_sizes))} but the algorithm computed {str(actual)}!")
