import math
import numpy as np

def geo(p):
	R = np.random.uniform(low=np.nextafter(0.0, 1.0), high=1.0) 
	return math.ceil(math.log2(R) / math.log2(1 - p))

