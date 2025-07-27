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

def reference_solution(N, steps):
  # This solution was published on dailycodingproblem.com
  cache = [0 for _ in range(N + 1)]
  cache[0] = 1
  for i in range(1, N + 1):
    cache[i] += sum(cache[i - x] for x in steps if i - x >= 0)
  return cache[N]

# -----------------------------------------------------------------------------

import decimal
decimal.getcontext().prec = 10
import timeit
FUNCNAME_LEN = 18
HEIGHT_LEN = 4
VALUE_LEN = 6

if __name__ == '__main__':
  functions = (
    solve,
    reference_solution,
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
function              N  value time [s]
solve                 1      1 8.368299959984142e-07
reference_solution    1      1 1.5810803000204032e-06
bruteforce            1      1 1.1653236400161405e-06
solve                 2      2 1.636574960029975e-06
reference_solution    2      2 2.4255773100594526e-06
bruteforce            2      2 1.5370235150112422e-06
solve                 3      3 2.0852342899888755e-06
reference_solution    3      3 2.738937390022329e-06
bruteforce            3      3 1.9980097999723513e-06
solve                 4      5 2.762393500015605e-06
reference_solution    4      5 3.43394713003363e-06
bruteforce            4      5 3.1765896800061457e-06
solve                 5      8 3.3024096400185955e-06
reference_solution    5      8 4.074978240096243e-06
bruteforce            5      8 5.950586359977023e-06
solve                 8     34 6.203141399892047e-06
reference_solution    8     34 7.041075059969444e-06
bruteforce            8     34 2.459670169992023e-05
solve                13    377 9.497016800014536e-06
reference_solution   13    377 1.0490396349996444e-05
bruteforce           13    377 0.00026064437800232555
solve                21  17711 1.606362700003956e-05
reference_solution   21  17711 1.6420170549827162e-05
bruteforce           21  17711 0.01549952539971855
solve                34 9227465 2.5791124300303636e-05
reference_solution   34 9227465 2.6519357999495698e-05
bruteforce           34 9227465 8.200105157993676
solve                55 2.2585e+11 5.122660880006151e-05
reference_solution   55 2.2585e+11 5.595858960004989e-05
solve                89 2.8801e+18 8.54515901999548e-05
reference_solution   89 2.8801e+18 9.504046579968417e-05
solve               144 8.9892e+29 9.661914839962265e-05
reference_solution  144 8.9892e+29 0.00010426295900106198
solve               233 3.5779e+48 0.00015895950249978342
reference_solution  233 3.5779e+48 0.00016876255500028491
solve               377 4.4447e+78 0.00024914531000104034
reference_solution  377 4.4447e+78 0.0002911490929982392
solve               610 2.1977e+127 0.0003955200729978969
reference_solution  610 2.1977e+127 0.0004970505880046403
solve               987 1.3499e+206 0.00066388849800569
reference_solution  987 1.3499e+206 0.0008102355820010416
solve              1597 4.0998e+333 0.0010869669900057488
reference_solution 1597 4.0998e+333 0.0014079671800209326
solve              2584 7.6483e+539 0.0024405429849866777
reference_solution 2584 7.6483e+539 0.0023793206499976806
solve              4181 4.3334e+873 0.0028342363499541533
reference_solution 4181 4.3334e+873 0.0037877741400006927
solve              6765 4.5802e+1413 0.004919248179940041
reference_solution 6765 4.5802e+1413 0.009200063939933898
solve              10946 2.7429e+2287 0.008628759720013477
reference_solution 10946 2.7429e+2287 0.013434136400246644
solve              17711 1.7362e+3701 0.016660095849874778
reference_solution 17711 1.7362e+3701 0.02743075059988769
solve              28657 6.5813e+5988 0.03247606639997684
reference_solution 28657 6.5813e+5988 0.06005671099992469
solve              46368 1.5791e+9690 0.0659464559998014
reference_solution 46368 1.5791e+9690 0.1224635920007131
solve              75025 1.4362e+15679 0.13862297400191892
reference_solution 75025 1.4362e+15679 0.2590084379990003
solve              121393 3.1341e+25369 0.24593021400505677
reference_solution 121393 3.1341e+25369 0.9174563130000024
solve              196418 6.2205e+41048 0.9012884960029623
steps=(1, 3, 5)
function              N  value time [s]
solve                 1      1 1.0285421579901594e-06
reference_solution    1      1 1.747167610010365e-06
bruteforce            1      1 1.0403201699955388e-06
solve                 2      1 2.4137543600227218e-06
reference_solution    2      1 2.3113555400050247e-06
bruteforce            2      1 1.499355359992478e-06
solve                 3      2 2.981446709964075e-06
reference_solution    3      2 3.366106730027241e-06
bruteforce            3      2 1.861649469974509e-06
solve                 4      3 4.162283740006387e-06
reference_solution    4      3 3.79952401999617e-06
bruteforce            4      3 2.6957337299973005e-06
solve                 5      5 6.080169600027148e-06
reference_solution    5      5 4.425955560000148e-06
bruteforce            5      5 4.146517699991819e-06
solve                 8     19 9.977732539991847e-06
reference_solution    8     19 7.114579339977354e-06
bruteforce            8     19 1.5717382099683164e-05
solve                13    182 1.614401580009144e-05
reference_solution   13    182 1.0814979950009729e-05
bruteforce           13    182 0.0001479133395005192
solve                21   6728 2.7761437300068794e-05
reference_solution   21   6728 1.663613445016381e-05
bruteforce           21   6728 0.006068924660066841
solve                34 2371987 4.4742006801243406e-05
reference_solution   34 2371987 2.8596959300193703e-05
bruteforce           34 2371987 2.5913614720047917
solve                55 3.0893e+10 7.876558459975059e-05
reference_solution   55 3.0893e+10 4.641608379897661e-05
solve                89 1.4185e+17 0.00012359929800004465
reference_solution   89 1.4185e+17 7.633136479998938e-05
solve               144 8.4831e+27 0.00019682345950059244
reference_solution  144 8.4831e+27 0.00012560364199816831
solve               233 2.3294e+45 0.00038659625900618267
reference_solution  233 2.3294e+45 0.0006186194780020742
solve               377 3.8253e+73 0.0005834128660062561
reference_solution  377 3.8253e+73 0.00042284257200662977
solve               610 1.7250e+119 0.0009688895580038661
reference_solution  610 1.7250e+119 0.0006685408899938921
solve               987 1.2774e+193 0.0015993230350068188
reference_solution  987 1.2774e+193 0.0011533803099882788
solve              1597 4.2654e+312 0.00264879991998896
reference_solution 1597 4.2654e+312 0.0019456291499955114
solve              2584 1.0547e+506 0.004287183479900705
reference_solution 2584 1.0547e+506 0.0033428398900286994
solve              4181 8.7087e+818 0.007523827440018067
reference_solution 4181 8.7087e+818 0.005641573419998167
solve              6765 1.7781e+1325 0.01251678999979049
reference_solution 6765 1.7781e+1325 0.010455419799836819
solve              10946 2.9975e+2144 0.023856389700085856
reference_solution 10946 2.9975e+2144 0.022022333399945637
solve              17711 1.0317e+3470 0.04108423380093882
reference_solution 17711 1.0317e+3470 0.04411255900049582
solve              28657 5.9867e+5614 0.08968529499979923
reference_solution 28657 5.9867e+5614 0.09840290439897217
solve              46368 1.1957e+9085 0.21031220800068695
reference_solution 46368 1.1957e+9085 0.16046275150074507
solve              75025 1.3857e+14700 0.2584686129994225
reference_solution 75025 1.3857e+14700 0.3993380750034703
solve              121393 3.2072e+23785 0.5788726289974875
reference_solution 121393 3.2072e+23785 1.049552307005797
steps=(2, 5, 11, 17, 23, 31, 41, 47, 59, 67, 73, 83, 97)
function              N  value time [s]
solve                 1      0 2.6798218800104222e-06
reference_solution    1      0 2.246607520064572e-06
bruteforce            1      0 1.325386834978417e-06
solve                 2      1 2.8305637100129388e-06
reference_solution    2      1 3.135213889981969e-06
bruteforce            2      1 1.2949527899763779e-06
solve                 3      0 5.262363439978799e-06
reference_solution    3      0 4.327116960048443e-06
bruteforce            3      0 2.029069710006297e-06
solve                 4      1 5.9713492800074166e-06
reference_solution    4      1 5.746933939954033e-06
bruteforce            4      1 2.0225577000383056e-06
solve                 5      1 8.137339539971436e-06
reference_solution    5      1 8.716619900078513e-06
bruteforce            5      1 3.4566680699936116e-06
solve                 8      1 2.2528104699449612e-05
reference_solution    8      1 1.3750566500311834e-05
bruteforce            8      1 6.693324700027006e-06
solve                13      7 4.4286638199992015e-05
reference_solution   13      7 2.0210258100269128e-05
bruteforce           13      7 2.0620096499624195e-05
solve                21     41 0.0001060027245002857
reference_solution   21     41 3.85782706005557e-05
bruteforce           21     41 0.0001724707790017419
solve                34   1017 0.0002056934200008982
reference_solution   34   1017 6.787771480012453e-05
bruteforce           34   1017 0.004035078120068647
solve                55 168783 0.00030831374000263166
reference_solution   55 168783 8.527588500001002e-05
bruteforce           55 168783 0.5641005629950087
solve                89 661008892 0.0007281913599872496
reference_solution   89 661008892 0.00016164221549843204
solve               144 4.2877e+14 0.0014284635549847735
reference_solution  144 4.2877e+14 0.00027477888800058283
solve               233 1.0893e+24 0.0026820442400639875
reference_solution  233 1.0893e+24 0.0004972473980014911
solve               377 1.7950e+39 0.004573067900055321
reference_solution  377 1.7950e+39 0.0009863081140065334
solve               610 7.5143e+63 0.007935181479988387
reference_solution  610 7.5143e+63 0.0017676939249940916
solve               987 5.1837e+103 0.013190075199963758
reference_solution  987 5.1837e+103 0.002955600190034602
solve              1597 1.4970e+168 0.021342966399970464
reference_solution 1597 1.4970e+168 0.005091752500011353
solve              2584 2.9824e+272 0.03610248760014656
reference_solution 2584 2.9824e+272 0.009137564980046592
solve              4181 1.7159e+441 0.05744635519949952
reference_solution 4181 1.7159e+441 0.015681454449804733
solve              6765 1.9668e+714 0.10023157359973993
reference_solution 6765 1.9668e+714 0.02750073240022175
solve              10946 1.2970e+1156 0.16279059950102237
reference_solution 10946 1.2970e+1156 0.04842509260051884
solve              17711 9.8039e+1870 0.2806818640019628
reference_solution 17711 9.8039e+1870 0.10377510359976441
solve              28657 4.8870e+3027 0.5180760820003343
reference_solution 28657 4.8870e+3027 0.19065853000211064
reference_solution 46368 1.8414e+4899 0.3835958620038582
reference_solution 75025 3.4584e+7927 0.9087077720032539
steps=range(1, 100)
function              N  value time [s]
solve                 1      1 1.956650915017235e-05
reference_solution    1      1 7.209900860034395e-06
bruteforce            1      1 5.597561800095718e-06
solve                 2      2 4.390869479975663e-05
reference_solution    2      2 1.3559934549994068e-05
bruteforce            2      2 9.812153759994544e-06
solve                 3      4 6.492319420067361e-05
reference_solution    3      4 2.0422936500108336e-05
bruteforce            3      4 1.8905335199815454e-05
solve                 4      8 9.191272720054258e-05
reference_solution    4      8 2.6582559799862793e-05
bruteforce            4      8 3.513285290027852e-05
solve                 5     16 9.909742559975711e-05
reference_solution    5     16 2.8204206500231522e-05
bruteforce            5     16 6.46364767992054e-05
solve                 8    128 0.00017409350849993644
reference_solution    8    128 4.513355600065552e-05
bruteforce            8    128 0.0004963465839973651
solve                13   4096 0.00029771548099961367
reference_solution   13   4096 7.065285420103464e-05
bruteforce           13   4096 0.015519869200215908
solve                21 1048576 0.0005784300240047742
reference_solution   21 1048576 0.00011825747100010631
bruteforce           21 1048576 4.174514913000166
solve                34 8589934592 0.0011247971250122645
reference_solution   34 8589934592 0.00021242970100138336
solve                55 1.8014e+16 0.0023247009699844056
reference_solution   55 1.8014e+16 0.0003588483190033003
solve                89 3.0949e+26 0.004884307500033174
reference_solution   89 3.0949e+26 0.0006972395140037406
solve               144 1.1150e+43 0.010416535249896696
reference_solution  144 1.1150e+43 0.001384763075002411
solve               233 6.9017e+69 0.0202427443000488
reference_solution  233 6.9017e+69 0.0025797315299860204
solve               377 1.5391e+113 0.03614993579976726
reference_solution  377 1.5391e+113 0.004765824579953915
solve               610 2.1246e+183 0.06547290599992266
reference_solution  610 2.1246e+183 0.009765603999985615
solve               987 6.5400e+296 0.11570139849936822
reference_solution  987 6.5400e+296 0.016168709950216
solve              1597 2.7789e+480 0.2028318840020802
reference_solution 1597 2.7789e+480 0.030221483300556427
solve              2584 3.6348e+777 0.3246866109984694
reference_solution 2584 3.6348e+777 0.05637934080004925
solve              4181 2.0201e+1258 0.5188942189997761
reference_solution 4181 2.0201e+1258 0.0987475715999608
reference_solution 6765 1.4686e+2036 0.21632349099672865
reference_solution 10946 5.9334e+3294 0.4631111470007454
reference_solution 17711 1.7427e+5331 1.1478029880017857
All tests passed
"""
