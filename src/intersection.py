import math

# returns the smallest volume >= to x
# when we have a d-dimensional hypercube
def roundUpCellVol(x, d):
	x = x ** (-1)
	l = math.floor(math.log(x, 2**d))
	return l, 2 ** ((-1) * l * d)

# obtaining the geometric ordering for a given level
# is the exact same one of ordered combinations of d numbers chosen from the range [0,2**l)
# we use backtracking to solve it
def getGeometricOrdering(comb, l, d, ans):
	if len(comb) is d:
		temp = []
		for x_i in comb:
			temp.append([x_i * 2 ** (-l), (x_i+1) * 2 ** (-l)])
		ans.append([l, temp])	
	
		# ans.append([l, comb[:]])
		return
	
	for i in range(2**l):
		comb.append(i)
		getGeometricOrdering(comb, l, d, ans)
		comb.pop()

ordering = []
getGeometricOrdering([], 1, 2, ordering)

for cell in ordering:
	print(cell)
print(len(ordering))

# iterate through the points in P

l = 1
d = 2
P = [[0.7, 0.2]]

for point in P:
	cell = []
	for i in range(d):
		cell.append(math.floor(point[i] / (2 ** (-l))))

	print(cell)	


# determine the cell the point belongs to

# increment count if point really belongs in that cell


