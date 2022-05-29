# Myers algorithm based on Ruby code on
# from https://blog.jcoglan.com/2017/02/17/the-myers-diff-algorithm-part-3/
# i am still trying to understand this algorithm
# I've implemented the diff3 algorithm with it which handles arbitrary text merges.
from pprint import pprint
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
  y = 0
  
  for d in range(0, max_size):
    trace.append(list(costs))
    for k in [i for i in range(-d, max_size, 2)]:
      if k == -d or (k != d and costs[k - 1] < costs[k + 1] > costs[k + 1]): # insert if its too costly to move diagonally
        x = costs[k + 1] # insert
      else:
        x = costs[k - 1] + 1
      y = x - k
      
      if y < 0:
        y = 0

      costs[k] = x
      
      while x < n and y < m and left[x] == right[y]:
        
        x, y = x + 1, y + 1
      
      
      if x >= n and y >= m:
        return n, m, max_size, trace
      
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

    if d >= 0:
      
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
    if prev_x < 0:
      continue
    if prev_y < 0:
      continue
    else:
    
      a_line, b_line = left[prev_x], right[prev_y]
  
      if x == prev_x:
        diff.insert(0, ("insert", None, b_line, x, y, prev_x, prev_y))
      elif y == prev_y:
        pass # diff.insert(0, ("delete", a_line, None, x, y, prev_x, prev_y))
      else:
        
        diff.insert(0, ("same", a_line, b_line, x, y, prev_x, prev_y))
    
  

    
    
    
    
  return diff

def apply_diffs(original, diff):
  merged = ""
  
  for patch in diff:
    if patch[2] == "same":
      merged += patch[4]
    if patch[2] == "insert":
      merged += patch[4]
    if patch[2] == "conflict":
      posttag = "\u001b[39m"
      if patch[0] == 1:
        pretag = "\u001b[31m"
      if patch[0] == 0:
        pretag = "\u001b[32m"
      merged += pretag + (patch[4] if patch[4] != None else "-") + posttag
  return merged

def diff_and_apply(original, a):
  original_split = original
  a_split = a
  
  diffs = label_and_number(0, diff(original_split, a_split))
  pprint(diffs)

  merged_left = apply_diffs(original_split, diffs)
  
  return Document(merged_left, None, display=merged_left)

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

  outer_source_x = left[5]
    
  outer_source_y = left[6]
    
  outer_prev_source_x = left[7]
    
  outer_prev_source_y = left[8]

  inner_source_x = right[5]
    
  inner_source_y = right[6]
    
  inner_prev_source_x = right[7]
    
  inner_prev_source_y = right[8]

  
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
    delabelled.append((diff[2], diff[3], diff[4], diff[5], diff[6], diff[7], diff[8]))
  return delabelled

def find_conflicts(left, right, diffs):
  rewritten = []
  conflicts = []
  end = len(diffs) - 1
  left_end = len(left) - 1
  right_end = len(right) - 1
  cursors = {
    "0": 0,
    "1": 0
  }
  
  for outer_index, outer in enumerate(diffs):
    
    
    innercursor = 0
    outer_identifier = outer[0]

    
    outer_internal_index = outer[1]
  
    outer_type = outer[2]
    
    current_identifier = outer[0]
    
    outer_source_x = outer[5]
    
    outer_source_y = outer[6]
    
    outer_prev_source_x = outer[7]
    
    outer_prev_source_y = outer[8]
    
    
    
    if outer_type == "insert":
      cursors[str(current_identifier)] = cursors[str(current_identifier)] + 1
        
      
    
    for inner_index, inner in enumerate(diffs):
     
        inner_identifier = inner[0]
        inner_internal_index = inner[1]
        inner_type = inner[2]
        inner_value = inner[4]
        inner_source_x = inner[5]
        inner_source_y = inner[6]
        inner_prev_source_x = inner[7]
        inner_prev_source_y = inner[8]
  
        
        
        
        if inner_identifier != outer_identifier:
          
          if inner_type == "insert":
            innercursor = innercursor + 1

          

    
        
    
    already_conflicted = False
    conflicted = None
    for inner_index, inner in enumerate(diffs):
      
      
      if inner == outer:
        continue
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
      
      # print(cursor, innercursor)
      past_end = (cursors[str(outer_identifier)] >= cursors[str(((inner_identifier + 1)% 2))]) and outer_type != "delete" and inner_type != "delete"
      already_conflicted =  (inner in conflicts) and outer_type != "delete"

      
      
      if past_end and already_conflicted or (inner_identifier != outer_identifier and (inner_source_x == outer_source_x and inner_source_y == outer_source_y or (outer_prev_source_x == inner_prev_source_x and outer_prev_source_y == inner_prev_source_y))) and inner_value != outer_value and outer_type != "delete":
        
        if inner_value != "\n" and outer_value != "\n":
          
            # print("conflict", inner_value, outer_value)
            conflicted = ((outer_identifier + 1) % 2, outer_internal_index, "conflict", "", outer_value, outer_source_x, outer_source_y, outer_prev_source_x, outer_prev_source_y)
            break
            
          
          
          
    if not conflicted:
      rewritten.append(outer)
    elif conflicted:
      conflicts.append(outer)
      conflicts.append(inner)
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

      if (inner_index > outer_index and inner_value == outer_value and inner_type == outer_type and (outer_source_x == inner_source_x and inner_source_y == outer_source_y) and (outer_prev_source_x == inner_prev_source_x and outer_prev_source_y == inner_prev_source_y)):
        valid = False
        break
        
        
      
    if valid:
      deduplicated_diffs.append(outer)
  return deduplicated_diffs

def has_conflicts(diff):
  if diff[2] == "conflict":
    return True
  return False
from itertools import combinations

class DiffRange:
  def __init__(self, identifier, type):
    self.type = type
    self.identifier = identifier
    self.diffs = []
    self.divergences = []
    self.next = None
    self.conflicted = False

  def create_coordinate(self):
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for diffrange in self.divergences:
      
      for divergence in diffrange.diffs:
        min_x = min(min_x, divergence[5])
        min_y = min(min_y, divergence[6])
        max_x = max(max_x, divergence[5])
        max_y = max(max_y, divergence[6])
    return Coordinate(min_x, min_y, max_x, max_y, diffrange)
  
  def add_diff(self, diff):
    if diff[2] == "same":
      self.diffs.append((-1, diff[1], diff[2], diff[3], diff[4], diff[5], diff[6], diff[7], diff[8]))
    else:
      self.diffs.append(diff)
  
  def add_child(self, divergence):
    self.divergences.append(divergence)

  def add_join(self, join):
    for item in self.divergences:
      item.next = join

  def equal(left, right):
    left_string = ""
    for item in left.diffs:
      
        left_string += item[4]
    right_string = ""
    for item in right.diffs:
      
        right_string += item[4]
    return left_string == right_string

  def remove_equal(self):
    for pair in combinations(self.divergences, 2):
      if self.equal(pair[0], pair[1]):
        self.divergences.remove(pair[1])
  
  def walk(self, path=""):
    print(path + self.type)
    
    for item in self.divergences:
      for diff in item.diffs:
        print(path + str(diff))
      
    if self.next:
      self.next.walk(path)

def apply_alignments(alignment):
  current = alignment
  conflict = False
  display = ""
  plain = ""
  while current != None:
    if len(current.divergences) > 0:
      conflict = True
    for divergence in current.divergences:
      for patch in divergence.diffs:
        pretag = ""
        posttag = "\u001b[39m"
        
        if divergence.conflicted:
          
          
          if patch[0] == 1:
            pretag = "\u001b[31m"
          if patch[0] == 0:
            pretag = "\u001b[32m"
          if patch[0] == -1:
            pretag = ""
        display += pretag + (patch[4] if patch[4] != None else "") + posttag
        plain += patch[4] if patch[4] != None else ""

    current = current.next
  
  return (conflict, (display, plain))

class Coordinate:
  def __init__(self, min_x, min_y, max_x, max_y, diffrange):
    self.min_x = min_x
    self.min_y = min_y
    self.max_x = max_x
    self.max_y = max_y

    self.diffrange = diffrange
    


def mark_conflicting_coordinates(coordinates):
  
  for outer in coordinates:
    for inner in coordinates:
      if inner == outer:
        continue
      if inner.min_x >= outer.min_x and \
        inner.max_x <= outer.max_x or \
        inner.min_y >= outer.min_y and \
        inner.max_y <= outer.max_y:
          
          
          inner.diffrange.conflicted = True
          outer.diffrange.conflicted = True
          
          

def create_coordinate_tree(alignments):
  tree = []
  current = alignments
  coordinates = []
  while current != None:
    tree.append(current)
    coordinate = current.create_coordinate()
    coordinates.append(coordinate)
    current = current.next
  
  mark_conflicting_coordinates(coordinates)

def create_alignment(diffs):
  previous = diffs[0]
  
  previous_identifier = previous[0]
  previous_type = previous[2]

  previous_source_x = previous[5]
  
  
  previous_root = DiffRange(previous_identifier, previous_type)
  root = previous_root
  current_span = DiffRange(previous_identifier, previous_type)
  current_span.add_diff(previous)
  previous_root.add_child(current_span)
  for outer in diffs[1:]:
    outer_identifier = outer[0]
    
    outer_internal_index = outer[1]
    
    outer_type = outer[2]
    

    outer_value = outer[4]
    

    outer_source_x = outer[5]
    
    outer_source_y = outer[6]
    

    outer_prev_source_x = outer[7]
    outer_prev_source_y = outer[8]

    matches_type = previous_type == outer_type
    matches_identifier = outer_identifier == previous_identifier

    
      
    
    if not matches_identifier or not matches_type:
      
      new_root = DiffRange(outer_identifier, outer_type)
      
      new_span = DiffRange(outer_identifier, outer_type)
      previous_root.next = new_root
      
      new_root.add_child(new_span)
      new_span.add_diff(outer)
      current_span = new_span
      previous_root.add_join(new_root)
      
      previous_root = new_root
    else:
      current_span.add_diff(outer)
    
    previous_identifier = outer_identifier
    previous_type = outer_type
    previous_source_x = outer_source_x
  
  root.remove_equal()
  
  return root
    
    

def merge_diffs(original, a, b):
  print("source document", a)
  print("target document", b)
  # print(original.text)
  diffs_a = label_and_number(0, diff(original.text, a))
  diffs_b = label_and_number(1, diff(original.text, b))
  
  diffs = diffs_a + diffs_b
  
  diffs.sort(key=cmp_to_key(diff_sorter))

  
  # diffs = find_conflicts(diffs_a, diffs_b, diffs)
  # diffs = remove_duplicates(diffs)
  pprint(diffs)
  alignment = create_alignment(diffs)
  create_coordinate_tree(alignment)
  # print(alignment.walk())
  # merged_left = apply_diffs(original, diffs)
  conflicts, merged = apply_alignments(alignment)
  # print(merged[1])
  # conflicts = list(filter(has_conflicts, diffs))
  # print(conflicts)
  
  print("diffs")
  # pprint(diffs)

  print("display", merged[0])
  
  return Document(text=merged[1], previous=None, conflicts=conflicts, display=merged[0])
  

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
  return history[start  + 1:]

def diff3(a, b):
  a_history = get_history(a)
  
  b_history = get_history(b)
  
  S = common_ancestor(a_history, b_history)
  
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
        

    
    
  
    
  merged = merge_diffs(last_left, last_left.text, last_right.text)
  

  
  return (merged,)

class Document():
  def __init__(self, text, previous, display="", conflicts=False):
    self.text = text
    self.display = display
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
    print(item.display)

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
    print(item.display)

t1 = diff_and_apply(original, left1)
print(t1.display)
