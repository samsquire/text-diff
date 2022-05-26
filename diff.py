# based on Ruby code
# from https://blog.jcoglan.com/2017/02/17/the-myers-diff-algorithm-part-3/
# i am still trying to understand this algorithm

from functools import cmp_to_key

root_text = """
1. wine
"""

left1 = """
1. wine
2. celery
3. tomatoes
"""

left2 = """
1. wine
2. celery
3. tomatoes
4. cabbage
5. coffee
"""

original = """
1. wine
2. celery
"""

right1 = """
1. wine
2. salmon
3. garlic
"""

right2 = """
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
      
      while x < n and y < m and left[x] == right[y]:
        
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
      
      yield prev_x, prev_y, x, y 
      
    x, y = prev_x, prev_y
    
  

from itertools import zip_longest

def diff(left, right):
  diffs = []
  for l, r in zip_longest(left, right, fillvalue=""):
    diff = []
    differences = backtrack(*diffstring(l, r))

    for prev_x, prev_y, x, y in differences:
      
      if prev_x >= len(l):
        break
      if prev_y >= len(r):
        break
      if prev_x < 0 or prev_y < 0:
        break
      print(prev_x, prev_y, len(left), len(right))
      a_line, b_line = l[prev_x], r[prev_y]

      if x == prev_x:
        diff.insert(0, ("insert", None, b_line))
      elif y == prev_y:
        diff.insert(0, ("delete", a_line, None))
      else:
        diff.insert(0, ("same", a_line, b_line))
      
    

    
    
    for difference in diff:
      print("difference", difference)
    if diff:
      diffs.append(diff)
  return diffs

def apply_diffs(original, diffs):
  for source, diff in zip_longest(original, diffs):
    merged = ""
    if diff:
      for patch in diff:
        if patch[0] == "same":
          merged += patch[2]
        if patch[0] == "insert":
          merged += patch[2]
      yield merged

def diff_and_apply(original, a):
  original_split = original
  a_split = a
  
  diffs = diff(original_split, a_split)
  print(diffs)

  merged_left = list(apply_diffs(original_split, diffs))
  
  return Document(merged_left, original)

def label_and_number(identifier, diffs):
  updated_diffs = []
  
  for diffset in diffs:
    for index, diff in enumerate(diffset):
      print("diff", diff)
      updated_diffs.append((identifier, index, diff[0], diff[1], diff[2]))
  return updated_diffs

def diff_sorter(left, right):
  left_identifier = left[0]
  right_identifier = right[0]
  left_index = left[1]
  right_index = right[1]
  left_type = left[2]
  right_type = right[2]

  if left_identifier > right_identifier:
    return 1
  if right_identifier < left_identifier:
    return -1
  if left_index > right_index:
    return 1
  if right_index > left_index:
    return -1
  if left_type == "delete":
    return 1
  if right_type == "delete":
    return -1
  return 0

def delabel(diffs):
  delabelled = []
  for diff in diffs:
    delabelled.append((diff[2], diff[3], diff[4]))
  return delabelled

def merge_diffs(original, a, b):
  diffs_a = label_and_number(0, diff(original.text, a))
  diffs_b = label_and_number(1, diff(original.text, b))
  
  diffs = diffs_a + diffs_b
  print(diffs)
  diffs.sort(key=cmp_to_key(diff_sorter))

  print("diffs", diffs)

  merged_left = list(apply_diffs(original.text, delabel(diffs)))
  
  return Document(merged_left, original)
  

def rindex(items, search):
  for index, item in reversed(list(enumerate(items))):
    if item == search:
      return index
  return None

def common_ancestor(a, b):
  
  for event in reversed(a):
    print("b", b)
    if event in b:
      last_occurrence = b.index(event)
      return b[last_occurrence]
  return None
    

def get_history(document):
  history = []
  current = document
  while current.previous != None:
    history.insert(0, current)
    current = current.previous
  history.insert(0, current)
  return history

def versions_from(source, history):
  start = history.index(source)
  return history[start:]

def diff3(a, b):
  a_history = get_history(a)
  print(a_history)
  b_history = get_history(b)
  print(b_history)
  S = common_ancestor(a_history, b_history)
  print("common ancestor", S)
  left_sequence = versions_from(S, a_history)
  right_sequence = versions_from(S, b_history)
  last_left = S
  last_right = S
  for left, right in zip_longest(left_sequence, right_sequence):
    if left:
      
      last_left = merge_diffs(last_left, left.text, right.text)
    if right:
      
      last_right = merge_diffs(last_right, left.text, right.text)

    

    
  
  merged = merge_diffs(last_left, last_left.text, last_right.text)

  
  return merged

class Document():
  def __init__(self, text, previous):
    self.text = text
    self.previous = previous

print(diff_and_apply(original, left2))

common = Document(root_text, None)

S = Document(original, common)

document_left1 = Document(left1, S)
document_left2 = Document(left2, document_left1)

document_right1 = Document(right1, S)
document_right2 = Document(right2, document_right1)

merged = diff3(document_left2, document_right2)
print("merged", merged.text)
