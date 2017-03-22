#!/usr/bin/python
import numpy as np
'''
these functions correspond to the available operations in our string alignment.
The functions define the behavior as well as the value of these operations
'''
def indel(cost_matrix, ix, iy):
	x_indel = cost_matrix[ix, iy-1]
	y_indel = cost_matrix[ix-1, iy]
	return min(x_indel, y_indel)+1


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
	return min(indel(cost_matrix, ix, iy), sub(cost_matrix, ix, iy, x, y),swap(cost_matrix, ix, iy))


def alignStrings(x, y):
	nx = len(x)
	ny = len(y)
	cost_matrix = np.zeros((nx+1, ny+1))
	for i in range(0, nx+1):
		cost_matrix[i, 0]=i
	for i in range(0, ny+1):
		cost_matrix[0, i] = i
	for ix in range (1, nx+1):
		for iy in range(1, ny+1):
			cost_matrix[ix,iy] = cost_of_op(cost_matrix, ix, iy, x, y)
	return cost_matrix

q = alignStrings("AGA","ACGT")
print(q)
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
	print ("i,j", i, j)
	if i < 0 or j < 0:
		return -777777777
	else:
		return cost_matrix[i,j]
def get_cheapestst_op(i,j,cost_matrix):
	#NEED TO ADD WEIGHTED COST VALUES FOR OPERATIONS INDEL+=1, SUB+=10 SWAP+=10*2(SUB)
	insert_cost = compute_cost(cost_matrix,i-1,j)	
	delete_cost = compute_cost(cost_matrix,i,j-1)
	sub = compute_cost(cost_matrix,i-1,j-1)
	swap = compute_cost(cost_matrix,i-2,j-2)
	ops = [(insert_cost,'insert', i-1, j),(delete_cost, 'delete', i,j-1),(sub, 'sub', i-1, j-1),(swap, 'swap', i-2, j-2)]
	cost,op,new_i, new_j = max(ops,key = lambda v:v[0])
	print(ops)
	print(cost, op, i, j)
	if op  == sub and cost_matrix[i,j] == cost:
		op = "nop"
	return op, new_i, new_j

def extractAlignment(cost_matrix):
	i,j = cost_matrix.shape
	i-=1
	j-=1
	a = []
	while i >0 or j>0:
		if j<-2:
			break
		print("=================================================")
		print(cost_matrix)
		op,i,j = get_cheapestst_op(i,j,cost_matrix) 
		print(i, j)
		a.append(op)
	return a

hat = extractAlignment(q)
print(hat)
