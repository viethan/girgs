import math

# returns the smallest volume >= to x
# when we have a d-dimensional hypercuber
def roundUpCellVol(x, d):
	x = x ** (-1)
	l = math.floor(math.log(x, 2**d))
	print(l)
	return 2 ** ((-1) * l * d)

# determine geometric ordering of the cells of volume mu

# iterate through the points in P

# determine the cell the point belongs to

# increment count if point really belongs in that cell


