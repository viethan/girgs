import math
import helper

class Partitioning:
	def __init__(self, v, d):
		self.d = d
		self.l, self.mu = helper.roundUpCellVolume(v, d)
		self.P = set()

		if self.l <= 0:
			self.l = 0
			self.P.add((0, ((0.0, 0.0), (0.0, 0.0))))
			return

		 
		for level in range(self.l, 0, -1):
			cells = helper.getCells(level, self.d)

			for c in cells:
				neighbours = []
				helper.getNeighbours(c, level, self.d, 0, [], neighbours)

				# type I.
				if level == self.l:
					for neighbour in neighbours:
						par = (level, tuple(sorted([tuple(c), tuple(neighbour)])))
						if par in self.P:
							print("):")
						self.P.add(tuple(par))

				# type II.
				else:
					c_children = helper.getChildren(c, level, self.d)
					for neighbour in neighbours:
						n_children = helper.getChildren(neighbour, level, self.d)

						for c1 in c_children:
							for c2 in n_children:
								par = (level+1, tuple(sorted([tuple(c1), tuple(c2)])))
								if par in self.P:
									print("):")
								self.P.add(tuple(par))


ds = Partitioning(0.00001, 2)
count = [0, 0, 0, 0, 0, 0, 0]
tempo = []
for level, pair in ds.P:
	if level <= 3:
		count[level] += 1

	if level == 4:
		tempo.append((level, pair))

print(count[3], count[2], count[1], count[0])
print(len(ds.P))

for pair in sorted(tempo):
	print(pair)

	# 1184