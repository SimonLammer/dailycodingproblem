#!/usr/bin/python3
# Questioner: Amazon
# Difficulty: Hard

"""
Given an integer k and a string s, find the length of the longest substring that contains at most k distinct characters.

For example, given s = "abcba" and k = 2, the longest substring with k distinct characters is "bcb".
"""

# -----------------------------------------------------------------------------

def sol1(k, s):
  if len(s) <= k:
    return s
  chars = dict()
  for i in range(k):
    chars[s[i]] = chars.get(s[i], 0) + 1
  max_len = k
  max_len_substr_start = 0
  lo = 0
  hi = k
  while hi < len(s):
    while hi < len(s):
      chars[s[hi]] = chars.get(s[hi], 0) + 1
      if len(chars.keys()) > k:
        break
      hi += 1
    prev_substr_len = hi - lo
    if prev_substr_len > max_len:
      max_len = prev_substr_len
      max_len_substr_start = lo
    if hi >= len(s):
      break
    hi += 1
    while True:
      c = s[lo]
      lo += 1
      if chars[c] == 1:
        del chars[c]
        if len(chars.keys()) <= k:
          break
      else:
        chars[c] -= 1
  return s[max_len_substr_start : max_len_substr_start+max_len]

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  functions = (
    sol1,
  )

  tests = [
    ((2, "abcba"), "bcb"),
    ((2, "bcbax"), "bcb"),
    ((2, "xabcb"), "bcb"),
  ]
  s = "0010120123012340123450123456012345670123456780123456789"
  for k in range(11):
    r = s[:(1 + k) * (k + 2) // 2 - 1]
    tests.extend([
      ((k, s), r),
      ((k, s[::-1]), r[::-1]),
    ])

  for args, expectation in tests:
    print(f"{args=} {expectation=}")
    results = []
    for f in functions:
      res = f(*args)
      results.append(res)
      print(res, f)
    assert all([res == expectation for res in results])
  print("All tests passed")

