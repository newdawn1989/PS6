
import numpy as np
'''
these functions correspond to the available operations in our string alignment.
The functions define the behavior as well as the value of these operations
'''
def insert(cost_matrix, ix, iy):
	y_indel = cost_matrix[ix-1, iy]
	return  y_indel+1

def delete(cost_matrix, ix, iy):
	x_indel = cost_matrix[ix,iy-1]
	return x_indel+1

def sub(cost_matrix, ix, iy, x, y):
	if x[ix-1]!=y[iy-1]:
		sub_cost = cost_matrix[ix-1, iy-1]
		sub_cost+=10
	else:
		sub_cost = cost_matrix[ix-1, iy-1]
	return sub_cost

def swap(cost_matrix, ix, iy):
	swap = cost_matrix[ix-2, iy-2]
	return swap+10+10+10


def cost_of_op(cost_matrix, ix, iy, x, y): #function to calculate the min cost of all available operations
	insert_cost = insert(cost_matrix,ix,iy)	
	delete_cost = delete(cost_matrix,ix,iy)
	sub_cost = sub(cost_matrix,ix,iy, x, y)
	swap_cost = swap(cost_matrix,ix,iy)
	ops = [(insert_cost, ix-1, iy),(delete_cost, ix,iy-1),(sub_cost, ix-1, iy-1),(swap_cost, ix-2, iy-2)]
	return min(ops,key = lambda v: v[0])
def alignStrings(x,y):
	nx = len(x)
	ny = len(y)
	pointer_matrix = np.zeros((nx+1, ny+1, 2))# 3d array to hold pairs of values for the path we take to optimal solution
	cost_matrix = np.zeros((nx+1, ny+1))
	for i in xrange(0,nx+1):
		cost_matrix[i,0]=i
		pointer_matrix[i,0,0] = i-1 #x coordinate
		pointer_matrix[i,0,1] = 0 #y coordinate
	for i in xrange(0,ny+1):
		cost_matrix[0,i] = i
		pointer_matrix[0,i,0] = 0 #x coordinate
		pointer_matrix[0,i,1] = i-1 #y coordinate

	for ix in xrange (1, nx+1):
		for iy in xrange(1, ny+1):
			cost,prev_ix, prev_iy = cost_of_op(cost_matrix,ix,iy, x, y)
			cost_matrix[ix,iy] = cost
			pointer_matrix[ix,iy,0] = prev_ix 
			pointer_matrix[ix,iy,1] = prev_iy 
	return cost_matrix, pointer_matrix

cost_matrix, pointer_matrix = alignStrings("AGA","ACGT")
'''
 returns a

vector a that represents an optimal sequence of edit operations to convert x into y.

This optimal sequence is recovered by finding a path on the implicit DAG of decisions

made by alignStrings to obtain the value S[nx, ny], starting from S[0, 0].

extractAlignment(S) : // S is an optimal cost matrix from alignStrings

	initialize a // empty vector of edit operations

	[i,j] = [nx,ny] // initialize the search for a path to S[0,0]

	while i > 0 or j > 0

		a[i] = determineOptimalOp(S,i,j) // what was the optimal choice here?

		[i,j] = updateIndices(S,i,j,a) // move to next position

}

return a

When storing the sequence of edit operations in a, use a special symbol to denote

no-ops.
'''
def compute_cost(cost_matrix,i,j): #function to compute the local cost of performing a trace-back operations
	print "i,j", i,j
	if i < 0 or j < 0:
		return -777777777
	else:
		return cost_matrix[i,j]
def get_op_name(ix, prev_ix, iy, prev_iy):
	xdiff = ix-prev_ix
	ydiff = iy-prev_iy
	if xdiff == 1 and ydiff == 0:
		return "insert"
	elif xdiff == 0 and ydiff == 1:
		return "delete"
	elif xdiff == 1 and ydiff == 1:
		return "sub"
	elif xdiff == 2 and ydiff == 2:
		return "swap"
	else:
		raise Exception("Bad diff (x = %d, y = %d" %(xdiff, ydiff))

def get_cheapestst_op(ix,iy,cost_matrix,pointer_matrix):
	prev_ix = pointer_matrix[ix, iy,0]
	prev_iy = pointer_matrix[ix,iy,1]
	cost = cost_matrix[ix,iy]

	op = get_op_name(ix, prev_ix, iy, prev_iy)

	if op  == sub and cost_matrix[i,j] == cost:
		op = "nop"
	print cost, op
	return op, prev_ix, prev_iy

def extractAlignment(cost_matrix, pointer_matrix):
	i,j = cost_matrix.shape
	i-=1
	j-=1
	a = []
	while i >0 or j>0:
		if j<-2:
			break
		op,i,j = get_cheapestst_op(i,j,cost_matrix, pointer_matrix) 
		a.append(op)
	return a

hat= extractAlignment(cost_matrix, pointer_matrix)
print hat
print cost_matrix

def sub_chain_to_string(sub_matrix, ix, iy, x):
	substring = ""
	while ix < sub_matrix.shape[0] and iy < sub_matrix.shape[1] and sub_matrix[ix,iy] == 1:#while current position is within the matrix and current cell is a 1
		print ix,iy,x
		substring+=x[ix-1]                                                                   #keep stepping diagonally and finding 1's
		sub_matrix[ix,iy] = 0                                                               #end with there are no more 1's or we reach the end of the array
		ix+=1
		iy+=1
	return substring


def commonSubstring(pointer_matrix, x, L):
	sub_matrix = np.zeros(pointer_matrix.shape[:2])# x by y copy of pointer matrix
	substring  = []
	for ix in range(1,pointer_matrix.shape[0]): #populating the submatrix with 1's in any location a sub happened. This makes tracking substrings easier
		for iy in range(1,pointer_matrix.shape[1]):#not nessicarly part of the optimal path
			prev_ix = pointer_matrix[ix,iy,0]
			prev_iy = pointer_matrix[ix,iy,0]
			if prev_ix == ix-1 and prev_iy == iy-1:
				sub_matrix[ix, iy] = 1
	print sub_matrix
	for ix in range(1,sub_matrix.shape[0]):
		for iy in range(1,sub_matrix.shape[0]):
			prev_sub_found = sub_matrix[ix,iy]
			if sub_matrix[ix,iy] == 1:
				substrings = sub_chain_to_string(sub_matrix, ix, iy, x)
			if len(substring)>=L:  #as long as the substring is long enough, then append the value in substring
				substrings.append(substring)
	return substrings
				


herp = commonSubstring(pointer_matrix,"AGA",1)
print herp
