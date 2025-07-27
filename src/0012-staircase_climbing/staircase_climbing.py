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

def solve_heapq(N, steps=STEPS):
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

from bintrees import BinaryTree as Tree

def solve_btree(N, steps=STEPS):
  height_ways = Tree()
  height_ways.insert(0, 1)
  while True:
    height, ways = height_ways.pop_min() # Continue walking up from the lowest stair.
    if height >= N:
      break
    for step in steps: # Perform every possible step from the current stair.
      h = height + step
      w = height_ways.get(h, 0)
      height_ways[h] = w + ways
  return ways if height == N else 0


# -----------------------------------------------------------------------------

from sortedcontainers import SortedDict

def solve_sorteddict(N, steps=STEPS):
  height_ways = SortedDict()
  height_ways[N] = 1
  while True:
    height, ways = height_ways.popitem() # Continue walking down from the highest stair.
    if height <= 0:
      break
    for step in steps: # Perform every possible step from the current stair.
      h = height - step
      w = height_ways.get(h, 0)
      height_ways[h] = w + ways
  return ways if height == 0 else 0

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
    solve_btree,
    solve_sorteddict,
    solve_heapq,
    reference_solution,
    bruteforce,
  )
  for steps in (
    STEPS,
    (1, 3, 5),
    (2, 5, 11, 17, 23, 31, 41, 47, 59, 67, 73, 83, 97), # every other prime
    (11, 31, 59, 83, 109), # sparse primes
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
solve_btree           1      1 4.1040121599507985e-06
solve_sorteddict      1      1 8.84608306005248e-06
solve_heapq           1      1 6.983544260001509e-07
reference_solution    1      1 1.251540630000818e-06
bruteforce            1      1 8.500327059882693e-07
solve_btree           2      2 7.127727580082137e-06
solve_sorteddict      2      2 1.129619464991265e-05
solve_heapq           2      2 1.2709796200215351e-06
reference_solution    2      2 1.892354970004817e-06
bruteforce            2      2 1.2522356499903254e-06
solve_btree           3      3 9.908960040047531e-06
solve_sorteddict      3      3 1.3394469700142508e-05
solve_heapq           3      3 2.0512768699700247e-06
reference_solution    3      3 2.4594755499856546e-06
bruteforce            3      3 1.861699539986148e-06
solve_btree           4      5 1.2067719200058491e-05
solve_sorteddict      4      5 1.5414168699862783e-05
solve_heapq           4      5 2.6200457400409505e-06
reference_solution    4      5 3.139032910039532e-06
bruteforce            4      5 2.9670504500245444e-06
solve_btree           5      8 1.4299621649843174e-05
solve_sorteddict      5      8 1.7337701699943864e-05
solve_heapq           5      8 3.076190569991013e-06
reference_solution    5      8 3.6630348400649383e-06
bruteforce            5      8 5.023670880036661e-06
solve_btree           8     34 2.252904409979237e-05
solve_sorteddict      8     34 2.3703886799921747e-05
solve_heapq           8     34 4.746872139949119e-06
reference_solution    8     34 5.569308179983636e-06
bruteforce            8     34 2.0117201399989426e-05
solve_btree          13    377 3.5424534000048876e-05
solve_sorteddict     13    377 3.4672644599777414e-05
solve_heapq          13    377 7.429189599934034e-06
reference_solution   13    377 8.091801240079804e-06
bruteforce           13    377 0.00021493278499838198
solve_btree          21  17711 5.60016433999408e-05
solve_sorteddict     21  17711 5.1336318800167645e-05
solve_heapq          21  17711 1.2325465499816346e-05
reference_solution   21  17711 1.5459067900155786e-05
bruteforce           21  17711 0.013939606749772793
solve_btree          34 9227465 0.00010246260249914485
solve_sorteddict     34 9227465 8.763138399954187e-05
solve_heapq          34 9227465 2.2686093999800507e-05
reference_solution   34 9227465 2.4516435300029116e-05
bruteforce           34 9227465 13.357205031003105
solve_btree          55 2.2585e+11 0.00016285261350276414
solve_sorteddict     55 2.2585e+11 0.00013683062250129297
solve_heapq          55 2.2585e+11 3.565540859999601e-05
reference_solution   55 2.2585e+11 3.910624310010462e-05
solve_btree          89 2.8801e+18 0.0002538397310054279
solve_sorteddict     89 2.8801e+18 0.0002111627080012113
solve_heapq          89 2.8801e+18 5.659174920001533e-05
reference_solution   89 2.8801e+18 6.273257919965545e-05
solve_btree         144 8.9892e+29 0.0004099790479958756
solve_sorteddict    144 8.9892e+29 0.00033399969399761174
solve_heapq         144 8.9892e+29 9.030855579912896e-05
reference_solution  144 8.9892e+29 0.00010306225699969218
solve_btree         233 3.5779e+48 0.0006610913339973194
solve_sorteddict    233 3.5779e+48 0.0005401654460001736
solve_heapq         233 3.5779e+48 0.00014975512450109818
reference_solution  233 3.5779e+48 0.0001755823355015309
solve_btree         377 4.4447e+78 0.0012013796649989672
solve_sorteddict    377 4.4447e+78 0.0009605941159970825
solve_heapq         377 4.4447e+78 0.0002692199709999841
reference_solution  377 4.4447e+78 0.0003236397880027653
solve_btree         610 2.1977e+127 0.002352461369955563
solve_sorteddict    610 2.1977e+127 0.004639690940020955
solve_heapq         610 2.1977e+127 0.0006817951160046505
reference_solution  610 2.1977e+127 0.0008331305160099873
solve_btree         987 1.3499e+206 0.0044945915399875955
solve_sorteddict    987 1.3499e+206 0.0030181590999563924
solve_heapq         987 1.3499e+206 0.0008031859100010479
reference_solution  987 1.3499e+206 0.0008953402299957815
solve_btree        1597 4.0998e+333 0.0052056213200557975
solve_sorteddict   1597 4.0998e+333 0.004324176779919071
solve_heapq        1597 4.0998e+333 0.0012005190200216021
reference_solution 1597 4.0998e+333 0.0018139167049957905
solve_btree        2584 7.6483e+539 0.009278925899998285
solve_sorteddict   2584 7.6483e+539 0.004953170719963964
solve_heapq        2584 7.6483e+539 0.0015688436150230701
reference_solution 2584 7.6483e+539 0.0020800177900673587
solve_btree        4181 4.3334e+873 0.010477865199936787
solve_sorteddict   4181 4.3334e+873 0.008958234379970237
solve_heapq        4181 4.3334e+873 0.0026388640599907375
reference_solution 4181 4.3334e+873 0.0034386403799726395
solve_btree        6765 4.5802e+1413 0.018428671800211304
solve_sorteddict   6765 4.5802e+1413 0.01459579059992393
solve_heapq        6765 4.5802e+1413 0.004566438140027457
reference_solution 6765 4.5802e+1413 0.006634498579951469
solve_btree        10946 2.7429e+2287 0.033860223499505085
solve_sorteddict   10946 2.7429e+2287 0.02878396150044864
solve_heapq        10946 2.7429e+2287 0.009471969479927794
reference_solution 10946 2.7429e+2287 0.013384038300137036
solve_btree        17711 1.7362e+3701 0.059376833400165197
solve_sorteddict   17711 1.7362e+3701 0.050240301599842496
solve_heapq        17711 1.7362e+3701 0.01782328970002709
reference_solution 17711 1.7362e+3701 0.027687005800544284
solve_btree        28657 6.5813e+5988 0.1042928694987495
solve_sorteddict   28657 6.5813e+5988 0.088967493599921
solve_heapq        28657 6.5813e+5988 0.029183050600113346
reference_solution 28657 6.5813e+5988 0.05594119460001821
solve_btree        46368 1.5791e+9690 0.18434847149910638
solve_sorteddict   46368 1.5791e+9690 0.1655748439989111
solve_heapq        46368 1.5791e+9690 0.05734167379996506
reference_solution 46368 1.5791e+9690 0.1172748054996191
solve_btree        75025 1.4362e+15679 0.34771635500510456
solve_sorteddict   75025 1.4362e+15679 0.30975505099922884
solve_heapq        75025 1.4362e+15679 0.1449931015013135
reference_solution 75025 1.4362e+15679 0.25971352199849207
solve_btree        121393 3.1341e+25369 0.7021976379983244
solve_sorteddict   121393 3.1341e+25369 0.6122479820041917
solve_heapq        121393 3.1341e+25369 0.24595105899788905
reference_solution 121393 3.1341e+25369 0.599180263998278
solve_heapq        196418 6.2205e+41048 0.5672614079958294
steps=(1, 3, 5)
function              N  value time [s]
solve_btree           1      1 6.93934208000428e-06
solve_sorteddict      1      1 1.1628819899851806e-05
solve_heapq           1      1 9.36293589998968e-07
reference_solution    1      1 1.4091192750129267e-06
bruteforce            1      1 9.219916119909613e-07
solve_btree           2      1 1.2865887899897643e-05
solve_sorteddict      2      1 1.6034778300308973e-05
solve_heapq           2      1 1.700977190012054e-06
reference_solution    2      1 2.0521933500276648e-06
bruteforce            2      1 1.2759165200259304e-06
solve_btree           3      2 1.6452967899749638e-05
solve_sorteddict      3      2 1.877301320018887e-05
solve_heapq           3      2 2.7800929200020617e-06
reference_solution    3      2 2.730545459999121e-06
bruteforce            3      2 2.0570405099715572e-06
solve_btree           4      3 2.198435089958366e-05
solve_sorteddict      4      3 2.1158172500145156e-05
solve_heapq           4      3 3.877521840040572e-06
reference_solution    4      3 3.473306719970424e-06
bruteforce            4      3 2.480294210035936e-06
solve_btree           5      5 2.4482197200268275e-05
solve_sorteddict      5      5 2.3901937500340865e-05
solve_heapq           5      5 5.425394799967762e-06
reference_solution    5      5 4.57320236004307e-06
bruteforce            5      5 4.199706640065415e-06
solve_btree           8     19 4.17577779997373e-05
solve_sorteddict      8     19 4.3432900799962224e-05
solve_heapq           8     19 1.0026224849934806e-05
reference_solution    8     19 7.15364473988302e-06
bruteforce            8     19 1.4597646499896655e-05
solve_btree          13    182 5.682264819915872e-05
solve_sorteddict     13    182 4.536127880128333e-05
solve_heapq          13    182 1.5575454250210898e-05
reference_solution   13    182 1.0051174500040361e-05
bruteforce           13    182 0.00013718018000145093
solve_btree          21   6728 8.961940640001558e-05
solve_sorteddict     21   6728 6.754117740056244e-05
solve_heapq          21   6728 2.6223842400213472e-05
reference_solution   21   6728 1.7106492899984003e-05
bruteforce           21   6728 0.005281035759981023
solve_btree          34 2371987 0.00014208481300011043
solve_sorteddict     34 2371987 0.00010382063149882015
solve_heapq          34 2371987 4.2381713799841235e-05
reference_solution   34 2371987 2.5432829100464004e-05
bruteforce           34 2371987 2.2643952469952637
solve_btree          55 3.0893e+10 0.000223313260001305
solve_sorteddict     55 3.0893e+10 0.00016578854100225725
solve_heapq          55 3.0893e+10 7.087128679995658e-05
reference_solution   55 3.0893e+10 4.157855840021511e-05
solve_btree          89 1.4185e+17 0.0003835496259998763
solve_sorteddict     89 1.4185e+17 0.0002786349279995193
solve_heapq          89 1.4185e+17 0.00011551020749902818
reference_solution   89 1.4185e+17 6.878008219937329e-05
solve_btree         144 8.4831e+27 0.0005868505179969361
solve_sorteddict    144 8.4831e+27 0.00039335211400612027
solve_heapq         144 8.4831e+27 0.00018176067549939033
reference_solution  144 8.4831e+27 0.00011426017400299316
solve_btree         233 2.3294e+45 0.0010053897899706499
solve_sorteddict    233 2.3294e+45 0.0007131312679994153
solve_heapq         233 2.3294e+45 0.00030645541100238915
reference_solution  233 2.3294e+45 0.00019426939549884993
solve_btree         377 3.8253e+73 0.0015203361499879975
solve_sorteddict    377 3.8253e+73 0.0010410094799954096
solve_heapq         377 3.8253e+73 0.0004953804399992805
reference_solution  377 3.8253e+73 0.00033605552899825853
solve_btree         610 1.7250e+119 0.002457202880032128
solve_sorteddict    610 1.7250e+119 0.0017997190800087993
solve_heapq         610 1.7250e+119 0.0008137845460005338
reference_solution  610 1.7250e+119 0.0005804320979950717
solve_btree         987 1.2774e+193 0.0043256369199662
solve_sorteddict    987 1.2774e+193 0.0030473998699744697
solve_heapq         987 1.2774e+193 0.0014600306799911777
reference_solution  987 1.2774e+193 0.0010171765650011366
solve_btree        1597 4.2654e+312 0.006944737900048494
solve_sorteddict   1597 4.2654e+312 0.004732880899973679
solve_heapq        1597 4.2654e+312 0.0022101859700342174
reference_solution 1597 4.2654e+312 0.0015935075100060204
solve_btree        2584 1.0547e+506 0.010658512400186736
solve_sorteddict   2584 1.0547e+506 0.007566006800043396
solve_heapq        2584 1.0547e+506 0.003607416250015376
reference_solution 2584 1.0547e+506 0.003424093299981905
solve_btree        4181 8.7087e+818 0.017726758700155186
solve_sorteddict   4181 8.7087e+818 0.01303443934993993
solve_heapq        4181 8.7087e+818 0.005925794079957996
reference_solution 4181 8.7087e+818 0.004648617539933184
solve_btree        6765 1.7781e+1325 0.028757539299840575
solve_sorteddict   6765 1.7781e+1325 0.021245203200669492
solve_heapq        6765 1.7781e+1325 0.010017853349927464
reference_solution 6765 1.7781e+1325 0.008460733460087794
solve_btree        10946 2.9975e+2144 0.048582718201214445
solve_sorteddict   10946 2.9975e+2144 0.035584361300425374
solve_heapq        10946 2.9975e+2144 0.0170373049499176
reference_solution 10946 2.9975e+2144 0.015872175700133086
solve_btree        17711 1.0317e+3470 0.08331446700030938
solve_sorteddict   17711 1.0317e+3470 0.06191622939950321
solve_heapq        17711 1.0317e+3470 0.03384823009982938
reference_solution 17711 1.0317e+3470 0.03364576439998927
solve_btree        28657 5.9867e+5614 0.14896199050053838
solve_sorteddict   28657 5.9867e+5614 0.11355384749913355
solve_heapq        28657 5.9867e+5614 0.06038595259888098
reference_solution 28657 5.9867e+5614 0.06915110080008162
solve_btree        46368 1.1957e+9085 0.2646840719971806
solve_sorteddict   46368 1.1957e+9085 0.22868041499896208
solve_heapq        46368 1.1957e+9085 0.11128700699919136
reference_solution 46368 1.1957e+9085 0.14588704950074316
solve_btree        75025 1.3857e+14700 0.4935725570030627
solve_sorteddict   75025 1.3857e+14700 0.4058223669999279
solve_heapq        75025 1.3857e+14700 0.2187716990010813
reference_solution 75025 1.3857e+14700 0.32154209600412287
solve_btree        121393 3.2072e+23785 0.9803011809999589
solve_sorteddict   121393 3.2072e+23785 0.8337033860007068
solve_heapq        121393 3.2072e+23785 0.46754743000201415
reference_solution 121393 3.2072e+23785 0.7489275179977994
solve_heapq        196418 8.6029e+38485 1.077368401005515
steps=(2, 5, 11, 17, 23, 31, 41, 47, 59, 67, 73, 83, 97)
function              N  value time [s]
solve_btree           1      0 3.224451969945221e-05
solve_sorteddict      1      0 2.3194891599996482e-05
solve_heapq           1      0 2.185184330010088e-06
reference_solution    1      0 1.9719817000077457e-06
bruteforce            1      0 1.0772968899982515e-06
solve_btree           2      1 3.1433233300049325e-05
solve_sorteddict      2      1 2.1673820100113518e-05
solve_heapq           2      1 2.447662210033741e-06
reference_solution    2      1 2.8104562899534357e-06
bruteforce            2      1 1.193701534975844e-06
solve_btree           3      0 6.324553580052452e-05
solve_sorteddict      3      0 3.7334422799904135e-05
solve_heapq           3      0 4.675743999978294e-06
reference_solution    3      0 3.869208409960266e-06
bruteforce            3      0 1.7706836650177138e-06
solve_btree           4      1 6.300968699943041e-05
solve_sorteddict      4      1 3.7074324300192526e-05
solve_heapq           4      1 4.994600399950286e-06
reference_solution    4      1 4.992921800003387e-06
bruteforce            4      1 1.9152700650010955e-06
solve_btree           5      1 9.777324559981935e-05
solve_sorteddict      5      1 5.304093919985462e-05
solve_heapq           5      1 7.71131632005563e-06
reference_solution    5      1 7.496077460091328e-06
bruteforce            5      1 3.4853621500224106e-06
solve_btree           8      1 0.0002915501099996618
solve_sorteddict      8      1 0.00014015034699696116
solve_heapq           8      1 2.040545919953729e-05
reference_solution    8      1 1.3050578249749379e-05
bruteforce            8      1 6.532078680029372e-06
solve_btree          13      7 0.0004172740360008902
solve_sorteddict     13      7 0.000160755575998337
solve_heapq          13      7 4.4993215399881594e-05
reference_solution   13      7 2.1127474300010362e-05
bruteforce           13      7 2.2453207500075224e-05
solve_btree          21     41 0.0007963336620014161
solve_sorteddict     21     41 0.0002638798220068566
solve_heapq          21     41 0.0001410393705999013
reference_solution   21     41 3.3641535399510756e-05
bruteforce           21     41 0.00016308043000026374
solve_btree          34   1017 0.0011162718000196038
solve_sorteddict     34   1017 0.0005294851769940579
solve_heapq          34   1017 0.00023545548700349173
reference_solution   34   1017 8.712568820046727e-05
bruteforce           34   1017 0.006136060459975851
solve_btree          55 168783 0.00209389594005188
solve_sorteddict     55 168783 0.0006905705739918631
solve_heapq          55 168783 0.0005731733919965336
reference_solution   55 168783 0.00010570257850122289
bruteforce           55 168783 0.5997222199948737
solve_btree          89 661008892 0.0038594156200269934
solve_sorteddict     89 661008892 0.0008101785400067456
solve_heapq          89 661008892 0.0006494051940098871
reference_solution   89 661008892 0.0001510580324975308
solve_btree         144 4.2877e+14 0.009277368420007405
solve_sorteddict    144 4.2877e+14 0.0013016566400256124
solve_heapq         144 4.2877e+14 0.0013301625499661895
reference_solution  144 4.2877e+14 0.00025314554200303976
solve_btree         233 1.0893e+24 0.019621361899771726
solve_sorteddict    233 1.0893e+24 0.001906763984989084
solve_heapq         233 1.0893e+24 0.0022537510699476115
reference_solution  233 1.0893e+24 0.00040547774599690456
solve_btree         377 1.7950e+39 0.027670074000343447
solve_sorteddict    377 1.7950e+39 0.003070522289999644
solve_heapq         377 1.7950e+39 0.0037679366099473556
reference_solution  377 1.7950e+39 0.0007663391660025809
solve_btree         610 7.5143e+63 0.04642876279976917
solve_sorteddict    610 7.5143e+63 0.0050892989001295064
solve_heapq         610 7.5143e+63 0.0060590856199269185
reference_solution  610 7.5143e+63 0.0012941809550102335
solve_btree         987 5.1837e+103 0.07619974260014714
solve_sorteddict    987 5.1837e+103 0.007517940639954759
solve_heapq         987 5.1837e+103 0.01049064319995523
reference_solution  987 5.1837e+103 0.0024353303799580315
solve_btree        1597 1.4970e+168 0.12430616650090087
solve_sorteddict   1597 1.4970e+168 0.012225435599975753
solve_heapq        1597 1.4970e+168 0.02061677149977186
reference_solution 1597 1.4970e+168 0.003965128010022454
solve_btree        2584 2.9824e+272 0.22243037199950777
solve_sorteddict   2584 2.9824e+272 0.02053015420024167
solve_heapq        2584 2.9824e+272 0.026772727700154063
reference_solution 2584 2.9824e+272 0.007184730699955253
solve_btree        4181 1.7159e+441 0.3439946169964969
solve_sorteddict   4181 1.7159e+441 0.04831145889984327
solve_heapq        4181 1.7159e+441 0.051779401999374385
reference_solution 4181 1.7159e+441 0.0167267830001947
solve_btree        6765 1.9668e+714 0.5418182299981709
solve_sorteddict   6765 1.9668e+714 0.05850639060081449
solve_heapq        6765 1.9668e+714 0.0784607658002642
reference_solution 6765 1.9668e+714 0.020910720100073377
solve_sorteddict   10946 1.2970e+1156 0.1180453134002164
solve_heapq        10946 1.2970e+1156 0.16634749449804076
reference_solution 10946 1.2970e+1156 0.05548256320034852
solve_sorteddict   17711 9.8039e+1870 0.23680707799940137
solve_heapq        17711 9.8039e+1870 0.3017125719998148
reference_solution 17711 9.8039e+1870 0.11315134100004798
solve_sorteddict   28657 4.8870e+3027 0.4365236219964572
solve_heapq        28657 4.8870e+3027 0.4356240320048528
reference_solution 28657 4.8870e+3027 0.17259325349732535
solve_sorteddict   46368 1.8414e+4899 0.8099161879945314
solve_heapq        46368 1.8414e+4899 1.1096802800020669
reference_solution 46368 1.8414e+4899 0.39027841800270835
reference_solution 75025 3.4584e+7927 0.8340267099993071
steps=(11, 31, 59, 83, 109)
function              N  value time [s]
solve_btree           1      0 1.4918674149885191e-05
solve_sorteddict      1      0 1.8002579099993454e-05
solve_heapq           1      0 1.4576726250015782e-06
reference_solution    1      0 2.164073425010429e-06
bruteforce            1      0 1.407250970005407e-06
solve_btree           2      0 1.550228074993356e-05
solve_sorteddict      2      0 3.523033180026687e-05
solve_heapq           2      0 2.2937711450140343e-06
reference_solution    2      0 3.979182090042741e-06
bruteforce            2      0 1.219811530027073e-06
solve_btree           3      0 1.604656835006608e-05
solve_sorteddict      3      0 1.8934250650272587e-05
solve_heapq           3      0 1.620378174993675e-06
reference_solution    3      0 3.901493029989069e-06
bruteforce            3      0 1.4747882899973775e-06
solve_btree           4      0 2.324231120001059e-05
solve_sorteddict      4      0 2.3308401200483786e-05
solve_heapq           4      0 1.6336362099900725e-06
reference_solution    4      0 5.2565292798681186e-06
bruteforce            4      0 1.3336252250155667e-06
solve_btree           5      0 1.612272109996411e-05
solve_sorteddict      5      0 2.0306370499747573e-05
solve_heapq           5      0 1.7267384650040185e-06
reference_solution    5      0 6.794043900008546e-06
bruteforce            5      0 1.7118796100112376e-06
solve_btree           8      0 1.793191149990889e-05
solve_sorteddict      8      0 2.7661895399796776e-05
solve_heapq           8      0 1.7118944500180078e-06
reference_solution    8      0 1.245723129977705e-05
bruteforce            8      0 1.745571214996744e-06
solve_btree          13      0 4.701413139991928e-05
solve_sorteddict     13      0 5.6174302598810756e-05
solve_heapq          13      0 7.091117779928027e-06
reference_solution   13      0 2.579552019960829e-05
bruteforce           13      0 2.6604417599446606e-06
solve_btree          21      0 3.587501880028867e-05
solve_sorteddict     21      0 2.8043037799943703e-05
solve_heapq          21      0 3.068121480027912e-06
reference_solution   21      0 2.163266819989076e-05
bruteforce           21      0 1.3083856800221838e-06
solve_btree          34      0 9.040806580014759e-05
solve_sorteddict     34      0 6.508277599932626e-05
solve_heapq          34      0 7.237352240044856e-06
reference_solution   34      0 3.3549816700542576e-05
bruteforce           34      0 3.933361259987577e-06
solve_btree          55      1 0.0001141006664984161
solve_sorteddict     55      1 7.427796260017204e-05
solve_heapq          55      1 1.4421731000038563e-05
reference_solution   55      1 4.8293831999762915e-05
bruteforce           55      1 7.093217899964657e-06
solve_btree          89      0 0.00045746559600229374
solve_sorteddict     89      0 0.00022308106999844313
solve_heapq          89      0 4.911155859881546e-05
reference_solution   89      0 0.00011324209349913871
bruteforce           89      0 3.309044630004791e-05
solve_btree         144      0 0.0015646920400104137
solve_sorteddict    144      0 0.0005723878440039698
solve_heapq         144      0 0.000191329383997072
reference_solution  144      0 0.00018187826299981679
bruteforce          144      0 0.0003907016130033298
solve_btree         233    920 0.008685039400006644
solve_sorteddict    233    920 0.0020396799849913805
solve_heapq         233    920 0.0007124779320001835
reference_solution  233    920 0.000361664011994435
bruteforce          233    920 0.028942021600232692
solve_btree         377 546903 0.02036191149963997
solve_sorteddict    377 546903 0.0021648662900406635
solve_heapq         377 546903 0.0020593234300031325
reference_solution  377 546903 0.0008413459419971331
bruteforce          377 546903 7.768512236005336
solve_btree         610 1.1619e+10 0.026237181900069118
solve_sorteddict    610 1.1619e+10 0.002784390179949696
solve_heapq         610 1.1619e+10 0.002388482059977832
reference_solution  610 1.1619e+10 0.0008373044580075657
solve_btree         987 1.3594e+17 0.05539203719963552
solve_sorteddict    987 1.3594e+17 0.0035057980300189228
solve_heapq         987 1.3594e+17 0.0034711647700169123
reference_solution  987 1.3594e+17 0.001090096089974395
solve_btree        1597 3.6607e+28 0.06431857260031393
solve_sorteddict   1597 3.6607e+28 0.006056625679921126
solve_heapq        1597 3.6607e+28 0.005570270940079353
reference_solution 1597 3.6607e+28 0.0018519410099906964
solve_btree        2584 1.1411e+47 0.10972381149986177
solve_sorteddict   2584 1.1411e+47 0.01034021234991087
solve_heapq        2584 1.1411e+47 0.009763999939896167
reference_solution 2584 1.1411e+47 0.0033165846399788278
solve_btree        4181 9.5698e+76 0.17485791349827196
solve_sorteddict   4181 9.5698e+76 0.025293897149822442
solve_heapq        4181 9.5698e+76 0.020432237799832366
reference_solution 4181 9.5698e+76 0.006849043120018905
solve_btree        6765 2.5018e+125 0.41244667800492607
solve_sorteddict   6765 2.5018e+125 0.03528537599995616
solve_heapq        6765 2.5018e+125 0.04256522189971292
reference_solution 6765 2.5018e+125 0.013696168400201714
solve_btree        10946 5.4847e+203 0.894016472993826
solve_sorteddict   10946 5.4847e+203 0.08818697420065291
solve_heapq        10946 5.4847e+203 0.07171050540055149
reference_solution 10946 5.4847e+203 0.022816105499805416
solve_sorteddict   17711 3.1435e+330 0.10475237500213552
solve_heapq        17711 3.1435e+330 0.09856305699941004
reference_solution 17711 3.1435e+330 0.03602817089995369
solve_sorteddict   28657 3.9497e+535 0.1575987600008375
solve_heapq        28657 3.9497e+535 0.1463773575014784
reference_solution 28657 3.9497e+535 0.0544634681995376
solve_sorteddict   46368 2.8443e+867 0.26109964899660554
solve_heapq        46368 2.8443e+867 0.2454997250024462
reference_solution 46368 2.8443e+867 0.09240602799982298
solve_sorteddict   75025 2.5737e+1404 0.33077574799972354
solve_heapq        75025 2.5737e+1404 0.3140056280026329
reference_solution 75025 2.5737e+1404 0.14488273250026396
solve_sorteddict   121393 1.6770e+2273 0.7042472649991396
solve_heapq        121393 1.6770e+2273 0.56170120400202
reference_solution 121393 1.6770e+2273 0.28764758900069864
reference_solution 196418 9.8878e+3678 0.5839809180033626
steps=range(1, 100)
function              N  value time [s]
solve_btree           1      1 0.0008921071140066488
solve_sorteddict      1      1 0.00013742874300078255
solve_heapq           1      1 1.5488124799958313e-05
reference_solution    1      1 5.8342990999517495e-06
bruteforce            1      1 4.105895440006861e-06
solve_btree           2      2 0.001631350725001539
solve_sorteddict      2      2 0.00020689087250138981
solve_heapq           2      2 3.521055829987745e-05
reference_solution    2      2 1.14786162499513e-05
bruteforce            2      2 7.964516740030377e-06
solve_btree           3      4 0.002575672879975173
solve_sorteddict      3      4 0.00028904527200211303
solve_heapq           3      4 7.5384295200638e-05
reference_solution    3      4 2.3033414299425202e-05
bruteforce            3      4 1.9341217150213196e-05
solve_btree           4      8 0.0044516750000184405
solve_sorteddict      4      8 0.0005429042519972427
solve_heapq           4      8 0.00011017000999709126
reference_solution    4      8 2.9549621299520367e-05
bruteforce            4      8 3.865645270052482e-05
solve_btree           5     16 0.00488891449989751
solve_sorteddict      5     16 0.0005006894380057929
solve_heapq           5     16 0.00013024548300018067
reference_solution    5     16 3.716132849949645e-05
bruteforce            5     16 8.068966019927757e-05
solve_btree           8    128 0.008550515239912784
solve_sorteddict      8    128 0.0006503517259989167
solve_heapq           8    128 0.00022162920799746643
reference_solution    8    128 5.83400364004774e-05
bruteforce            8    128 0.0006155171519931173
solve_btree          13   4096 0.012026246599998559
solve_sorteddict     13   4096 0.0009396628719987348
solve_heapq          13   4096 0.0002780663919984363
reference_solution   13   4096 8.857327679870651e-05
bruteforce           13   4096 0.0212092070003564
solve_btree          21 1048576 0.020620206800231244
solve_sorteddict     21 1048576 0.0014463155600242317
solve_heapq          21 1048576 0.000661060118000023
reference_solution   21 1048576 0.00014610762900338158
bruteforce           21 1048576 4.30276744299772
solve_btree          34 8589934592 0.023519246399519033
solve_sorteddict     34 8589934592 0.0016550536850263597
solve_heapq          34 8589934592 0.0010246848200040405
reference_solution   34 8589934592 0.00019021104450075654
solve_btree          55 1.8014e+16 0.03898581030007335
solve_sorteddict     55 1.8014e+16 0.0027813204700214557
solve_heapq          55 1.8014e+16 0.0020913316199585095
reference_solution   55 1.8014e+16 0.00042954380599258003
solve_btree          89 3.0949e+26 0.10075507180008572
solve_sorteddict     89 3.0949e+26 0.004833563800057164
solve_heapq          89 3.0949e+26 0.004946855539892567
reference_solution   89 3.0949e+26 0.0007221417660039151
solve_btree         144 1.1150e+43 0.10361729999931413
solve_sorteddict    144 1.1150e+43 0.006959575939981732
solve_heapq         144 1.1150e+43 0.011219403100039927
reference_solution  144 1.1150e+43 0.0013747538499956137
solve_btree         233 6.9017e+69 0.17809553050028626
solve_sorteddict    233 6.9017e+69 0.010306082650276948
solve_heapq         233 6.9017e+69 0.018423648249881807
reference_solution  233 6.9017e+69 0.0027539750399591867
solve_btree         377 1.5391e+113 0.5034915360010928
solve_sorteddict    377 1.5391e+113 0.02413870719974511
solve_heapq         377 1.5391e+113 0.05977016879915027
reference_solution  377 1.5391e+113 0.007162750460120151
solve_sorteddict    610 2.1246e+183 0.04735525459982455
solve_heapq         610 2.1246e+183 0.14122236460098064
reference_solution  610 2.1246e+183 0.008990569160087034
solve_sorteddict    987 6.5400e+296 0.05935375459957868
solve_heapq         987 6.5400e+296 0.12373089600077947
reference_solution  987 6.5400e+296 0.020659979499760082
solve_sorteddict   1597 2.7789e+480 0.08852600079990225
solve_heapq        1597 2.7789e+480 0.18342793749980046
reference_solution 1597 2.7789e+480 0.02681053189953673
solve_sorteddict   2584 3.6348e+777 0.13596253799914848
solve_heapq        2584 3.6348e+777 0.29428551599994535
reference_solution 2584 3.6348e+777 0.0475685055993381
solve_sorteddict   4181 2.0201e+1258 0.26317741500679404
solve_heapq        4181 2.0201e+1258 0.5198517620010534
reference_solution 4181 2.0201e+1258 0.08979069979977794
solve_sorteddict   6765 1.4686e+2036 0.6775753250039998
reference_solution 6765 1.4686e+2036 0.18932192799911718
reference_solution 10946 5.9334e+3294 0.40353796699491795
reference_solution 17711 1.7427e+5331 0.8957750289991964
All tests passed
"""
