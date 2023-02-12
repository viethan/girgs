import math
import helper

def partition(x, d):
	l, vol = helper.roundUpCellVol(x, d)
	print("level:", l)
	P = set() 
	for level in range(l, 0, -1):
		cells = helper.getCells(level, d)

		for c in cells.keys():
			neighbours = []
			helper.getNeighbours(c, level, d, 0, [], neighbours)

			# type I.
			if level == l:
				for neighbour in neighbours:
					par = (level, tuple(sorted([tuple(c), tuple(neighbour)])))
					P.add(tuple(par))

					#if (level, tuple(c), tuple(neighbour)) not in P and (level, tuple(neighbour), tuple(c)) not in P:
					#	P.add((level, tuple(c), tuple(neighbour))) # maybe replace with sorting?

			# type II.
			else:
				# make sure to not make identical!!!!!!!!!!!!!!!!!!!
				c_children = helper.getChildren(c, level, d)
				for neighbour in neighbours:
					n_children = helper.getChildren(neighbour, level, d)

					for c1 in c_children:
						for c2 in n_children:
							par = (level+1, tuple(sorted([tuple(c1), tuple(c2)])))
							P.add(tuple(par))


			# backtracking to get all neighbours
			# MAKE SURE TO NOT HAVE DUPLICATES !!!!!!!! try both (x1, x2) and (x2, x1) in set? or modified backtracking

	return P


P = partition(0.015625, 2)
count = [0, 0, 0, 0]
for level, pair in P:
	count[level] += 1

print(count[3], count[2], count[1], count[0])
print(len(P))
