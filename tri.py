from pprint import pprint
from random import randint
from copy import deepcopy

class tri:
  def __init__(self, N, ch='O'):
    self.N      = N
    self.ch     = ch
    self.tri    = self.construct(N)
    self.lines  = [[j for j in i] for i in self.tri.split('\n')]
    self.deltas = [
      ((-1, +1) , (-1, -1)),  #above
      ((+1, +1) , (+1, -1)),  #below
      ((-1, +1) , (+0, +2)),  #up right
      ((+1, +1) , (+0, +2)),  #down right
      ((-1, -1) , (+0, -2)),  #up left
      ((+1, -1) , (+0, -2)),] #down left

  def construct(self, n):
    line = '' if self.N != n else ' ' * (n + 4) + '\n'
    line += ' ' * (n + 2)
    line += (self.ch + ' ') * (self.N - n + 1)
    line += ' \n'
    if n > 1:
      line += self.construct(n-1)
    else: 
      line += '  ' * (self.N + 2)
    return line

  def get_points(self):
    points = []
    for i, line in enumerate(self.lines):
      for j, ch in enumerate(line):
        if ch == self.ch:
          points += [(i,j)]
    return points

  def get_triads(self, point):
    row, col = point
    triads = []
    for (dr1, dc1), (dr2, dc2) in self.deltas:
      r1  = row+dr1
      c1  = col+dc1
      r2  = row+dr2
      c2  = col+dc2
      ch1 = self.lines[r1][c1]
      ch2 = self.lines[r2][c2]
      if ch1 == ch2 == self.ch:
        triads.append( ((r1, c1), (r2, c2),) ) #TODO decide if you return (row, col) also in result
    return triads

  def fill(self, ls, triads, depth=0):
    filled = False
    if not triads:
      print('\n'.join([''.join(i) for i in ls]))
      return True
    point, triad = triads.popitem()
    for i, (p1, p2) in enumerate(triad):
      if ls[p1[0]][p1[1]] == self.ch and\
         ls[point[0]][point[1]] == self.ch and\
         ls[p2[0]][p2[1]] == self.ch:
        lines_copy  = deepcopy(ls)
        fill_ch = chr(randint(65,78))
        lines_copy[point[0]][point[1]] = fill_ch
        lines_copy[p1[0]][p1[1]]       = fill_ch
        lines_copy[p2[0]][p2[1]]       = fill_ch
        triads_copy = triads.copy()
        del triads_copy[p1]
        del triads_copy[p2]
        if self.fill(lines_copy, triads_copy, depth+1):
          filled = True
          break
    return filled

  def __repr__(self):
    return self.tri


total = 0
numbers = list(filter(lambda x: ((x**2 + x)/2)%3 ==0 ,range(2,40) ))
for i in numbers:
  t=tri(i)
  points = t.get_points()
  triads = {}
  for p in points:
    triads[p] = t.get_triads(p)
  result=t.fill(t.lines, triads)
  print(str(i)+': '+str(result))
  list(filter(lambda x: ((x**2 + x)/2)%3 ==0 ,range(2,40) ))
  if result:
    total += i
print(total)
