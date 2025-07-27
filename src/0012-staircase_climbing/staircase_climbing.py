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

STEPS = (1, 2)

# -----------------------------------------------------------------------------

from heapq import heappush, heappop

def solve(N, steps=STEPS):
  height_ways = []
  heappush(height_ways, (0, 1)) # Initiailize with 1 way to get to height 0.
  while height_ways[0][0] < N:
    height, ways = heappop(height_ways) # Continue walking from the lowest stair.
    while height_ways and height_ways[0][0] == height: # Combine multiple ways to get to the same stair.
      ways += heappop(height_ways)[1]
    for step in steps: # Perform every possible step from the current stair.
      heappush(height_ways, (height + step, ways))
  ways = 0
  while height_ways and height_ways[0][0] == N: # Sum ways that climbed to the correct height N.
    ways += heappop(height_ways)[1]
  return ways

# -----------------------------------------------------------------------------

def bruteforce(N, steps=STEPS, verbose=False):
  solutions = 0
  traces = dict()
  def walk(n, trace):
    nonlocal solutions
    for step in steps:
      if n == step:
        if not trace.get(step, False):
          solutions += 1
          trace[step] = True
      elif n > step:
        t = dict()
        trace[step] = t
        walk(n - step, t)
  walk(N, traces)
  if verbose:
    def rec(trace, desc):
      for step, t in trace.items():
        if t == True:
          print(desc + str(step))
        else:
          rec(t, desc + f"{step},")
    rec(traces, '')
  return solutions

# -----------------------------------------------------------------------------

import decimal
decimal.getcontext().prec = 10
import timeit
FUNCNAME_LEN = 10
HEIGHT_LEN = 4
VALUE_LEN = 6

if __name__ == '__main__':
  functions = (
    solve,
    bruteforce,
  )
  for steps in (
    STEPS,
    (1, 3, 5),
    (2, 5, 11, 17, 23, 31, 41, 47, 59, 67, 73, 83, 97), # every other prime
    range(1, 100),
  ):
    print(f"{steps=}")
    print(f"{'function':{FUNCNAME_LEN}} {'N':>{HEIGHT_LEN}} {'value':>{VALUE_LEN}} time [s]")
    functions_enabled = [True for _ in functions]
    for N in (list(range(1,6)) + [8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269]):
      value = None
      for i, func in enumerate(functions):
        if not functions_enabled[i]:
          continue
        v = func(N, steps)
        if value is None:
          value = v
        else:
          assert value == v
        t = timeit.Timer(lambda: func(N, steps))
        reps, time = t.autorange()
        time /= reps
        if time > 0.5:
          functions_enabled[i] = False
        v_fmt = f"{v:{VALUE_LEN}}" if v < 1e10 else f"{decimal.Decimal(v):.{VALUE_LEN-2}e}"
        print(f"{func.__name__:{FUNCNAME_LEN}} {N:{HEIGHT_LEN}} {v_fmt} {time}")
  print("All tests passed")

"""
steps=(1, 2)
function      N  value time [s]
solve         1      1 1.1652569299985771e-06
bruteforce    1      1 1.2492309050139737e-06
solve         2      2 2.2561874299572083e-06
bruteforce    2      2 1.8001279100280954e-06
solve         3      3 2.9732621800212656e-06
bruteforce    3      3 2.8915330999734578e-06
solve         4      5 3.811635639940505e-06
bruteforce    4      5 4.27864879995468e-06
solve         5      8 4.500275059981505e-06
bruteforce    5      8 6.6587179400085006e-06
solve         8     34 7.473951279971515e-06
bruteforce    8     34 3.0360300400207053e-05
solve        13    377 1.1083111150219337e-05
bruteforce   13    377 0.00034703985400119566
solve        21  17711 1.892489720012236e-05
bruteforce   21  17711 0.017075301750082872
solve        34 9227465 3.0347677799727534e-05
bruteforce   34 9227465 9.028785833004804
solve        55 2.2585e+11 4.362992539972765e-05
solve        89 2.8801e+18 7.103988379967632e-05
solve       144 8.9892e+29 0.00011248409700056072
solve       233 3.5779e+48 0.0001804529350010853
solve       377 4.4447e+78 0.00046114783400844317
solve       610 2.1977e+127 0.0006027603399998043
solve       987 1.3499e+206 0.0010250332860014168
solve      1597 4.0998e+333 0.0014792824399773963
solve      2584 7.6483e+539 0.002452573339978699
solve      4181 4.3334e+873 0.003720924989975174
solve      6765 4.5802e+1413 0.006417034820042317
solve      10946 2.7429e+2287 0.00864715397998225
solve      17711 1.7362e+3701 0.015965885249897838
solve      28657 6.5813e+5988 0.03154126899971743
solve      46368 1.5791e+9690 0.06579046179977013
solve      75025 1.4362e+15679 0.24602215400227578
solve      121393 3.1341e+25369 0.2848649449952063
solve      196418 6.2205e+41048 1.1717795869990368
steps=(1, 3, 5)
function      N  value time [s]
solve         1      1 1.3457329850280076e-06
bruteforce    1      1 1.511307004984701e-06
solve         2      1 2.896362770043197e-06
bruteforce    2      1 2.8249189999769443e-06
solve         3      2 6.182978760043625e-06
bruteforce    3      2 2.7081187199655686e-06
solve         4      3 8.479881219973323e-06
bruteforce    4      3 8.29771789998631e-06
solve         5      5 1.3248142350130365e-05
bruteforce    5      5 1.2705353549972641e-05
solve         8     19 2.9967307900369632e-05
bruteforce    8     19 3.41361760001746e-05
solve        13    182 2.807523180017597e-05
bruteforce   13    182 0.00020073178700113204
solve        21   6728 4.681695839972235e-05
bruteforce   21   6728 0.009210656640061644
solve        34 2371987 5.969574199989438e-05
bruteforce   34 2371987 3.463830781998695
solve        55 3.0893e+10 0.00011784603150226757
solve        89 1.4185e+17 0.00029388950749853395
solve       144 8.4831e+27 0.0005327710400015349
solve       233 2.3294e+45 0.0012340454399964074
solve       377 3.8253e+73 0.0015237054300087038
solve       610 1.7250e+119 0.002452711799996905
solve       987 1.2774e+193 0.004834177840020857
solve      1597 4.2654e+312 0.004284119079966331
solve      2584 1.0547e+506 0.004702485199959483
solve      4181 8.7087e+818 0.011868945919995894
solve      6765 1.7781e+1325 0.01370038455024769
solve      10946 2.9975e+2144 0.021820449500228278
solve      17711 1.0317e+3470 0.040167021499655675
solve      28657 5.9867e+5614 0.10901695300126449
solve      46368 1.1957e+9085 0.20884021499659866
solve      75025 1.3857e+14700 0.4228997750033159
solve      121393 3.2072e+23785 1.2775404200001503
steps=(2, 5, 11, 17, 23, 31, 41, 47, 59, 67, 73, 83, 97)
function      N  value time [s]
solve         1      0 3.023085649983841e-06
bruteforce    1      0 1.4289484300024923e-06
solve         2      1 5.084699239960173e-06
bruteforce    2      1 2.425822209988837e-06
solve         3      0 9.115325379971181e-06
bruteforce    3      0 4.642472069972428e-06
solve         4      1 2.376227709974046e-05
bruteforce    4      1 4.4438234600238504e-06
solve         5      1 2.3886651300563243e-05
bruteforce    5      1 4.384915880073095e-06
solve         8      1 2.9285287499806146e-05
bruteforce    8      1 9.84927705998416e-06
solve        13      7 3.657640279998304e-05
bruteforce   13      7 1.5591632399809898e-05
solve        21     41 7.221838699915679e-05
bruteforce   21     41 0.00010964318349942915
solve        34   1017 0.00013894156749665854
bruteforce   34   1017 0.0026312778000283287
solve        55 168783 0.0002978300410031807
bruteforce   55 168783 0.500199646994588
solve        89 661008892 0.0005808226499939337
solve       144 4.2877e+14 0.0011854301649873377
solve       233 1.0893e+24 0.0021909916900040116
solve       377 1.7950e+39 0.0037255996499879983
solve       610 7.5143e+63 0.0070087664399761706
solve       987 5.1837e+103 0.01660708404997422
solve      1597 1.4970e+168 0.017904315499981747
solve      2584 2.9824e+272 0.029564396000205308
solve      4181 1.7159e+441 0.05834299679991091
solve      6765 1.9668e+714 0.15191580249666004
solve      10946 1.2970e+1156 0.13002287299968884
solve      17711 9.8039e+1870 0.2462074319992098
solve      28657 4.8870e+3027 0.4166856249939883
solve      46368 1.8414e+4899 0.7194121700013056
steps=range(1, 100)
function      N  value time [s]
solve         1      1 1.4608877849968849e-05
bruteforce    1      1 4.160389199969358e-06
solve         2      2 3.3243655600381315e-05
bruteforce    2      2 7.64638089996879e-06
solve         3      4 5.29955665988382e-05
bruteforce    3      4 1.484199600017746e-05
solve         4      8 7.841039040067699e-05
bruteforce    4      8 3.4585364899976414e-05
solve         5     16 0.00010897425949951867
bruteforce    5     16 9.159459399961633e-05
solve         8    128 0.00020270015299684018
bruteforce    8    128 0.0005789796419994672
solve        13   4096 0.0003455692839997937
bruteforce   13   4096 0.017987316050130174
solve        21 1048576 0.0006210261700034607
bruteforce   21 1048576 4.764993703000073
solve        34 8589934592 0.0010298544350007433
solve        55 1.8014e+16 0.0020662652800092474
solve        89 3.0949e+26 0.004458421820017975
solve       144 1.1150e+43 0.010862168049789034
solve       233 6.9017e+69 0.023273136299394537
solve       377 1.5391e+113 0.04022741880035028
solve       610 2.1246e+183 0.07111455619888148
solve       987 6.5400e+296 0.1302794225011894
solve      1597 2.7789e+480 0.21061822549745557
solve      2584 3.6348e+777 0.36312042899953667
solve      4181 2.0201e+1258 0.507329722000577
All tests passed
"""
