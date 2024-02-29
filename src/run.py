import json
import argparse

import numpy as np

from src.problem import Problem
from src.solvers import BacktrackingSolver
from src.utils import get_values, is_full_block, is_outer_boundary, is_el_shape, pprint

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Input file path.")
parser.add_argument("--output", help="Output file path.")
parser.add_argument("-n", help="Matrix dimension.")
args = parser.parse_args() 
indir = args.input
outdir = args.output
N = int(args.n)

matrix = []
targets = {}
with open(indir, "r") as f:
	lines = f.readlines()
	lines = [line for line in lines if line.strip()]
	for i, line in enumerate(lines[2:2+N]):
		row = list(map(lambda x: int(x) if (x in "1234" and x) else 0, line[::2][:N]))
		matrix.append(row)

	for line in lines[-4:]:
		tile, target = line.split(":")
		targets[tile] = int(target.strip())

	shapes = {"EL_SHAPE": 0, "FULL_BLOCK": 0, "OUTER_BOUNDARY": 0}
	shape_lst = lines[-6].strip().strip("}").strip("{").split(", ")
	for sh in shape_lst:
		key, value = sh.split("=")
		shapes[key] = int(value)

matrix = np.array(matrix)
problem = Problem(solver=BacktrackingSolver())

def shape_count_constraint(*args):
	fb = 0
	ob = 0
	el = 0
	for arg in args:
		fb += is_full_block(arg)
		ob += is_outer_boundary(arg)
		el += is_el_shape(arg)

	return fb == shapes["FULL_BLOCK"] and \
			ob == shapes["OUTER_BOUNDARY"] and \
			 el == shapes["EL_SHAPE"]

def target_constraint(*args):
	one = 0
	two = 0
	three = 0
	four = 0

	for arg in args:
		flat = [i for row in arg for i in row]
		one += flat.count(1)
		two += flat.count(2)
		three += flat.count(3)
		four += flat.count(4)

	return one == targets["1"] and \
			two == targets["2"] and \
			three == targets["3"] and \
			four == targets["4"] 

for i in range(0,N,4):
	for j in range(0,N,4):
		temp = matrix[i:i+4,j:j+4]
		problem.addVariable(str(i) + "-" + str(j), get_values(temp))

problem.addConstraint(shape_count_constraint, problem._variables.keys())
problem.addConstraint(target_constraint, problem._variables.keys())

with open(outdir, 'w') as f:
	for sol in problem.getSolutions():
		json.dump(sol, f)
		f.write('\n')
