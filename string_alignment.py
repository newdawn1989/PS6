
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
	ops = [(insert_cost, ix-1, iy),(delete_cost, ix,iy-1),(sub_cost, ix-1, iy-1),(swap_cost, ix-2, iy-2)]# is a table with the cost of and index of operation
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

	for ix in xrange (1, nx+1): #generates cost matrix for string alignment and pointer matrix to track the optimal path
		for iy in xrange(1, ny+1):
			cost,prev_ix, prev_iy = cost_of_op(cost_matrix,ix,iy, x, y)
			cost_matrix[ix,iy] = cost
			pointer_matrix[ix,iy,0] = prev_ix 
			pointer_matrix[ix,iy,1] = prev_iy 
	return cost_matrix, pointer_matrix


def compute_cost(cost_matrix,i,j): #function to compute the local cost of performing a trace-back operations setting neg indicies to large neg cost
	print "i,j", i,j
	if i < 0 or j < 0:
		return -777777777
	else:
		return cost_matrix[i,j]

def get_op_name(ix, prev_ix, iy, prev_iy):# uses pointer behafiov (relitive positions in the pointer matrix) to determin the operation
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

def get_cheapestst_op(ix,iy,cost_matrix,pointer_matrix): #pulls the pointer out of the pointer matrix, gets the cost and determins if the op is a nop
	prev_ix = pointer_matrix[ix, iy,0]
	prev_iy = pointer_matrix[ix,iy,1]
	cost = cost_matrix[ix,iy]
	op = get_op_name(ix, prev_ix, iy, prev_iy)
	if op  == "sub" and cost_matrix[ix,iy] == cost:
		op = "nop"
	print cost, op
	return op, prev_ix, prev_iy

def extractAlignment(cost_matrix, pointer_matrix): #returning vector of instrictions for optimal path
	i,j = cost_matrix.shape
	i-=1
	j-=1
	a = []
	while i >0 or j>0:
		if j<-2:
			break
		op,i,j = get_cheapestst_op(i,j,cost_matrix, pointer_matrix) 
		a.append(op)
	return a[::-1]

def costPathToStrings(cost_path, x): #converst numeric value of optimal path to corresponding string in common substring
	substrings = ['']
	cur_cost = cost_path[0][0]
	for i, (cost, ix) in enumerate(cost_path[1:]):
		if cur_cost == cost:
			substrings[-1]+=x[int(ix)-1]
		else:
			substrings.append("")
		cur_cost = cost
	return substrings

def commonSubstring(pointer_matrix,cost_matrix, x, L): #finds runs of nops to determin where the strings share characters
	optimal_cost_path=[]
	ix = cost_matrix.shape[0]-1
	iy = cost_matrix.shape[1]-1
	while not(ix <0 or iy <0):   #get pointer out of pointer matrix
		optimal_cost_path.append((cost_matrix[ix, iy],ix))
		prev_ix = pointer_matrix[ix, iy, 0]
		prev_iy = pointer_matrix[ix, iy, 1]
		ix = prev_ix
		iy = prev_iy

	optimal_cost_path =  optimal_cost_path[::-1]
			
	return costPathToStrings(optimal_cost_path, x)
				

