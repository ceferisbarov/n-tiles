import numpy as np

def pprint(matrix):
	for row in matrix:
		print(row)
	print("-----------------------------------")

def get_values(matrix):
	matrix = np.array(matrix)
	p1 = np.zeros(matrix.shape, dtype=int)
	p2 = matrix.copy()
	p2[0, :] = [0,0,0,0]
	p2[-1, :] = [0,0,0,0]
	p2[:,0] = [0,0,0,0]
	p2[:,-1] = [0,0,0,0]

	p3a = matrix.copy()
	p3b = matrix.copy()
	p3c = matrix.copy()
	p3d = matrix.copy()
	p3a[-1, :] = [0,0,0,0]
	p3a[:, 0] = [0,0,0,0]

	p3b[-1, :] = [0,0,0,0]
	p3b[:, -1] = [0,0,0,0]

	p3c[0, :] = [0,0,0,0]
	p3c[:, 0] = [0,0,0,0]

	p3d[0, :] = [0,0,0,0]
	p3d[:, -1] = [0,0,0,0]
	
	return p1.tolist(), p2.tolist(), p3a.tolist(), p3b.tolist(), p3c.tolist(), p3d.tolist()

def is_full_block(matrix):
	return not any([i for row in matrix for i in row])

def is_outer_boundary(matrix):
	matrix = np.array(matrix)

	if is_full_block(matrix):
		return False
	
	return (matrix[-1, :] == np.zeros(4)).all() and \
			(matrix[0, :] == np.zeros(4)).all() and \
			(matrix[:, -1] == np.zeros(4)).all() and \
			(matrix[:, 0] == np.zeros(4)).all()
			
def is_el_shape(matrix):
	matrix = np.array(matrix)
	if is_outer_boundary(matrix):
		return False
	
	if is_full_block(matrix):
		return False
	
	if (matrix[-1, :] == np.zeros(4)).all() and \
		(matrix[:, 0] == np.zeros(4)).all():
		return True

	if (matrix[-1, :] == np.zeros(4)).all() and \
		(matrix[:, -1] == np.zeros(4)).all():
		return True
	
	if (matrix[0, :] == np.zeros(4)).all() and \
		(matrix[:, 0] == np.zeros(4)).all():
		return True
	
	if (matrix[0, :] == np.zeros(4)).all() and \
		(matrix[:, -1] == np.zeros(4)).all():
		return True
	
	return False
