import math
import helper

def partition(x, d):
	l, vol = helper.roundUpCellVol(x, d)

	P = set() 
	for level in range(l, 0, -1):
		cells = helper.getCells(level, d)

		for c in cells.keys():
			neighbours = []
			helper.getNeighbours(c, level, d, 0, [], neighbours)

			# type I.
			if level == l:
				for neighbour in neighbours:
					if (level, tuple(c), tuple(neighbour)) not in P and (level, tuple(neighbour), tuple(c)) not in P:
						P.add((level, tuple(c), tuple(neighbour)))

			# type II.


			# backtracking to get all neighbours
			# MAKE SURE TO NOT HAVE DUPLICATES !!!!!!!! try both (x1, x2) and (x2, x1) in set? or modified backtracking

	return P


P = partition(0.0625, 2)
count = 0
for level, c1, c2 in P:
	if c1 == (3.0, 3.0):
		count += 1
		print((c1, c2))
	elif c2 == (3.0, 3.0):
		count += 1
		print((c2, c1))

print(count)
print(len(P))
print(P)

# I.

# enumerate all blocks of that size

# for each of them, get their neighbours (make sure to wrap around if needed)

# add them to the set P


# II.

# start bottom up


