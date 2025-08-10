#!/usr/bin/python3
# Questioner: Twitter
# Difficulty: Easy

"""
You run an e-commerce website and want to record the last N order ids in a log.
Implement a data structure to accomplish this, with the following API:

    record(order_id): adds the order_id to the log
    get_last(i): gets the ith last element from the log. i is guaranteed to be smaller than or equal to N.

You should be as efficient with time and space as possible.
"""

# -----------------------------------------------------------------------------


class RecentRecord:
  """
  S(N) = O(N) for storing the N order ids
  T(N) = O(1) for both record and get_last.
  """

  def __init__(self, N):
    assert N > 0
    self.data = [None] * N
    self.idx = 0

  def record(self, order_id):
    self.data[self.idx] = order_id
    self.idx += 1
    if self.idx == len(self.data):
      self.idx = 0

  def get_last(self, i):
    # 1 <= i <= N
    return self.data[self.idx - i]
    
    # The one-liner above is python comfort equivalent to the snippet below:
    # j = self.idx - i
    # if j < 0:
    #   j += len(self.data)
    # return self.data[j]

# -----------------------------------------------------------------------------

import random
from tqdm import tqdm

if __name__ == '__main__':
  for n in tqdm([1, 5, 21, 89, 377, 1597, 6765, 28657, 121393]):
    random.seed(f"almost random {n}")
    r = RecentRecord(n)
    for i in tqdm(range(1, n+1)):
      assert r.get_last(i) == None
    data = [random.random()]
    r.record(data[0])
    for _ in tqdm(range(1_000_000)):
      if random.random() < 0.5:
        datum = random.random()
        r.record(datum)
        data.append(datum)
      else:
        i = random.randint(1, min(n, len(data)))
        assert data[-i] == r.get_last(i)
  print("All tests passed")


"""
100%|█████████████████████████████████████████████████| 1/1 [00:00<00:00, 9279.43it/s]
100%|███████████████████████████████████| 1000000/1000000 [00:01<00:00, 919755.30it/s]
100%|████████████████████████████████████████████████| 5/5 [00:00<00:00, 94042.69it/s]
100%|███████████████████████████████████| 1000000/1000000 [00:01<00:00, 874049.51it/s]
100%|█████████████████████████████████████████████| 21/21 [00:00<00:00, 503316.48it/s]
100%|███████████████████████████████████| 1000000/1000000 [00:01<00:00, 873031.24it/s]
100%|████████████████████████████████████████████| 89/89 [00:00<00:00, 1269704.27it/s]
100%|███████████████████████████████████| 1000000/1000000 [00:01<00:00, 832446.96it/s]
100%|██████████████████████████████████████████| 377/377 [00:00<00:00, 1794838.37it/s]
100%|███████████████████████████████████| 1000000/1000000 [00:01<00:00, 821031.93it/s]
100%|████████████████████████████████████████| 1597/1597 [00:00<00:00, 1960287.82it/s]
100%|███████████████████████████████████| 1000000/1000000 [00:01<00:00, 813367.42it/s]
100%|████████████████████████████████████████| 6765/6765 [00:00<00:00, 1971818.38it/s]
100%|███████████████████████████████████| 1000000/1000000 [00:01<00:00, 830403.31it/s]
100%|██████████████████████████████████████| 28657/28657 [00:00<00:00, 1991156.63it/s]
100%|███████████████████████████████████| 1000000/1000000 [00:01<00:00, 798112.37it/s]
100%|████████████████████████████████████| 121393/121393 [00:00<00:00, 2003609.09it/s]
100%|███████████████████████████████████| 1000000/1000000 [00:01<00:00, 789163.99it/s]
100%|███████████████████████████████████████████████████| 9/9 [00:10<00:00,  1.21s/it]
All tests passed
"""
