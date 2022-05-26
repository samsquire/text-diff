# based on Ruby code
# from https://blog.jcoglan.com/2017/02/17/the-myers-diff-algorithm-part-3/
# i am still trying to understand this algorithm

text1 = """
1. celery
2. salmon
3. tomatoes
4. garlic
5. onions
6. wine
"""

original = """
1. celery
2. garlic
3. onions
4. salmon
5. tomatoes
6. wine
"""

text2 = """
1. celery
2. salmon
3. garlic
4. onions
5. tomatoes
6. wine
"""

import numpy as np


def shortest_edit(left, right):
    n = len(left)
    m = len(right)
    return n + m

def diffstring(left, right):
  max_size = shortest_edit(left, right)
  trace = []
  print(max_size)
  n = len(left)
  m = len(right)
  costs = [0] *  (1 + (2 * max_size + 1))
  
  
  costs[1] = 0
  x = 0
  y = -1
  
  for d in range(0, max_size):
    trace.append(list(costs))
    for k in [i for i in range(-d, max_size, 2)]:
      if k == -d or (k != d and costs[k - 1] < costs[k + 1] > costs[k + 1]): # insert if its too costly to move diagonally
        x = costs[k + 1] + 1 # insert
      else:
        x = costs[k - 1] + 1
      y = x - k
      if y < 0:
        y = 0
      print(x, y, k)
      while x < n and y < m and left[x] == right[y]:
        print(x, y)
        x, y = x + 1, y + 1
      
      
      if x >= n and y >= m:
        return n, m, max_size, trace
      costs[k] = x
  return n, m, max_size, trace

def backtrack(n, m, max_size, trace):
  x, y = n, m
  
  for d, costs in reversed(list(enumerate(trace))):
    k = x - y

    if k == -d or (k != d and costs[k - 1] < costs[k + 1]):
      prev_k = k + 1
    else:
      prev_k = k - 1

    prev_x = costs[prev_k]
    prev_y = prev_x - prev_k

    while x > prev_x and y > prev_y:
      yield x - 1, y - 1, x, y
      x, y = x - 1, y - 1

    if d > 0:
      print("prev_x", prev_x)
      print("prev_y", prev_y)
      yield prev_x, prev_y, x, y 
      
    x, y = prev_x, prev_y
    
  

from itertools import zip_longest
def diff(left, right):
  
  for l, r in zip_longest(left, right, fillvalue=""):
    diff = []
    differences = backtrack(*diffstring(l, r))

    for prev_x, prev_y, x, y in differences:
      print(prev_x, len(l), prev_y, len(r))
      if prev_x == len(l):
        prev_x = prev_x - 1
      if prev_y == len(r):
        prev_y = prev_y - 1
      a_line, b_line = l[prev_x], r[prev_y]

      if x == prev_x:
        diff.insert(0, ("insert", None, b_line))
      elif y == prev_y:
        diff.insert(0, ("delete", a_line, None))
      else:
        diff.insert(0, ("same", a_line, b_line))
      
    

    
    
    for difference in diff:
      print("difference", difference)
  

def diff3(original, a, b):
  original_split = original.split("\n")
  a_split = a.split("\n")
  b_split = b.split("\n")
  left = diff(original_split, a_split)
  right = diff(original_split, b_split)
  

print(diff3(original, text1, text2))
