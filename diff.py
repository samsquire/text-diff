# based on Ruby code
# from https://blog.jcoglan.com/2017/02/17/the-myers-diff-algorithm-part-3/
# i am still trying to understand this algorithm

from functools import cmp_to_key

root_text = """
1. wine
"""

left1 = """
Recipe
1. wine
2. celery
3. tomatoes
"""

left2 = """
Recipe
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
2. celery

Method
Mix the ingredients together
"""

right2 = """
1. wine
2. celery

Method
Mix the ingredients together
Put in oven

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
  
  
  diff = []
  differences = backtrack(*diffstring(left, right))

  for prev_x, prev_y, x, y in differences:
    
    if prev_x >= len(left):
      continue
    if prev_y >= len(right):
      continue
    if prev_x < 0 or prev_y < 0:
      continue
    else:
    
      a_line, b_line = left[prev_x], right[prev_y]
  
      if x == prev_x:
        diff.insert(0, ("insert", None, b_line, x, y, prev_x, prev_y))
      elif y == prev_y:
        diff.insert(0, ("delete", a_line, None, x, y, prev_x, prev_y))
      else:
        diff.insert(0, ("same", a_line, b_line, x, y, prev_x, prev_y))
    
  

    
    
    
    
  return diff

def apply_diffs(original, diff):
  merged = ""
  
  for patch in diff:
    if patch[0] == "same":
      merged += patch[2]
    if patch[0] == "insert":
      merged += patch[2]
    if patch[0] == "conflict":
      merged += "<<" + patch[1] + "|" + (patch[2] if patch[2] != None else "-") + ">>"
  return merged

def diff_and_apply(original, a):
  original_split = original
  a_split = a
  
  diffs = diff(original_split, a_split)
  print(diffs)

  merged_left = apply_diffs(original_split, diffs)
  
  return Document(merged_left, None)

def label_and_number(identifier, diffs):
  updated_diffs = []
  
  
  for index, diff in enumerate(diffs):
    
    updated_diffs.append((identifier, index, diff[0], diff[1], diff[2], diff[3], diff[4], diff[5], diff[6]))
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
  if left_index > right_index:
    return -1
  if right_index > left_index:
    return 1
  return 0

def delabel(diffs):
  delabelled = []
  for diff in diffs:
    delabelled.append((diff[2], diff[3], diff[4], diff[5], diff[6], diff[7], diff[8]))
  return delabelled

def find_conflicts(left, right, diffs):
  rewritten = []
  conflicts = []
  end = len(diffs) - 1
  left_end = len(left) - 1
  right_end = len(right) - 1
  print(diffs)
  
  for outer_index, outer in enumerate(diffs):
    if outer in conflicts:
      continue
    conflicted = None
    
    for inner_index, inner in enumerate(diffs):
      outer_identifier = outer[0]
      inner_identifier = inner[0]
      outer_internal_index = outer[1]
      inner_internal_index = inner[1]
      outer_type = outer[2]
      inner_type = inner[2]

      outer_value = outer[4]
      inner_value = inner[4]

      outer_source_x = outer[5]
      inner_source_x = inner[5]
      outer_source_y = outer[6]
      inner_source_y = inner[6]

      outer_prev_source_x = outer[7]
      inner_prev_source_x = inner[7]
      outer_prev_source_y = outer[8]
      inner_prev_source_y = inner[8]

      
      #  and (outer_source_x <= inner_source_x or inner_source_y <= outer_source_y or outer_prev_source_x <= inner_prev_source_x or outer_prev_source_y <= inner_prev_source_y

      if (inner_index > outer_index and inner_identifier != outer_identifier and inner_source_x == outer_source_x and inner_source_y == outer_source_y) and inner_value != outer_value and outer_internal_index == inner_internal_index:
        
        if outer_index != end and outer_index != 0 and outer_internal_index != left_end and outer_internal_index != 0 and inner_internal_index != right_end and inner_internal_index != 0:
          print("conflict", inner_value, outer_value)
          conflicted = (outer_identifier, outer_internal_index, "conflict", inner_value, outer_value, outer_source_x, outer_source_y, outer_prev_source_x, outer_prev_source_y)
          break
          
          
    if not conflicted:
      rewritten.append(outer)
    else:
      conflicts.append(outer)
      rewritten.append(conflicted)
  return rewritten

def remove_duplicates(diffs):
  deduplicated_diffs = []
  for outer_index, outer in enumerate(diffs):
    valid = True
    for inner_index, inner in enumerate(diffs):
      outer_identifier = outer[0]
      inner_identifier = inner[0]
      outer_internal_index = outer[1]
      inner_internal_index = inner[1]
      outer_type = outer[2]
      inner_type = inner[2]

      outer_value = outer[4]
      inner_value = inner[4]

      outer_source_x = outer[5]
      inner_source_x = inner[5]
      outer_source_y = outer[6]
      inner_source_y = inner[6]

      outer_prev_source_x = outer[7]
      outer_prev_source_y = outer[8]
      inner_prev_source_x = inner[7]
      inner_prev_source_y = inner[8]

      if (inner_index < outer_index and inner_value == outer_value and inner_type == outer_type and outer_source_x == inner_source_x and inner_source_y == outer_source_y and outer_prev_source_x == inner_prev_source_x and outer_prev_source_y == inner_prev_source_y):
        valid = False
        break
        
        
      
    if valid:
      deduplicated_diffs.append(outer)
  return deduplicated_diffs

def has_conflicts(diff):
  if diff[2] == "conflict":
    return True
  return False

def merge_diffs(original, a, b):
  print(original.text)
  diffs_a = label_and_number(0, diff(original.text, a))
  diffs_b = label_and_number(1, diff(original.text, b))
  
  diffs = diffs_a + diffs_b
  
  diffs.sort(key=cmp_to_key(diff_sorter))
  diffs = find_conflicts(diffs_a, diffs_b, diffs)
  diffs = remove_duplicates(diffs)

  
  conflicts = list(filter(has_conflicts, diffs))
  print(conflicts)
  
  print("diffs", diffs)

  merged_left = apply_diffs(original.text, delabel(diffs))
  
  
  return Document(merged_left, None, len(conflicts) > 0)
  

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
  valid = True
  for left, right in zip_longest(left_sequence, right_sequence):
    
    if left:
      
      last_left = merge_diffs(last_left, left.text, right.text)

      if last_left.conflicts:
        valid = False
    if right:
      
      last_right = merge_diffs(last_right, left.text, right.text)
      if last_right.conflicts:
        valid = False

    if not valid:
      break
    
  if (last_left.conflicts or last_right.conflicts):
    return last_left, last_right
    
  merged = merge_diffs(last_left, last_left.text, last_right.text)
  

  
  return (merged,)

class Document():
  def __init__(self, text, previous, conflicts=False):
    self.text = text
    self.previous = previous
    self.conflicts = conflicts

print(diff_and_apply(original, left2))

common = Document(root_text, None)

S = Document(original, common)

document_left1 = Document(left1, S)
document_left2 = Document(left2, document_left1)

document_right1 = Document(right1, S)
document_right2 = Document(right2, document_right1)

merged = diff3(document_left2, document_right2)
if merged:
  print("merged")
  for item in merged:
    print(item.text)

conflict1 = """
1. cheese
"""

conflict2 = """
1. chocolate
"""

a = Document(conflict1, S)
b = Document(conflict2, S)

conflicted = diff3(a, b)
if conflicted:
  for item in conflicted:
    print("conflict")
    print(item.text)
