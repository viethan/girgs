import math
import helper

def partition(x, d):
	l, vol = helper.roundUpCellVol(x, d)

	#P = 
	for level in range(l, 0, -1):
		cells = helper.getCells(level, d)

		for c in cells.keys():
			neighbours = []
			helper.getNeighbours(c, level, d, 0, [], neighbours)



			# backtracking to get all neighbours
			# MAKE SURE TO NOT HAVE DUPLICATES !!!!!!!! try both (x1, x2) and (x2, x1) in set? or modified backtracking

	return P


helper.getCells(2,2)
neighbours = []
helper.getNeighbours([3.0, 3.0], 2, 2, 0, [], neighbours)
print(neighbours)



# I.

# enumerate all blocks of that size

# for each of them, get their neighbours (make sure to wrap around if needed)

# add them to the set P


# II.

# start bottom up


