# Questioner: Google
# Difficulty: Easy
"""
Given a list of numbers and a number k, return whether any two numbers from the list add up to k.

For example, given [10, 15, 3, 7] and k of 17, return true since 10 + 7 is 17.

Bonus: Can you do this in one pass?
"""

arr = [10, 15, 3, 7]
k   = 17

def main(arr, k):
  arr.sort()

  low = 0
  high = len(arr) - 1

  while low <= high:
    x = arr[low] + arr[high]
    if x == k:
      return True
    elif x < k:
      low += 1
    else: # x > k
      high -= 1
  return False

if __name__ == '__main__':
  print(main(arr, k))