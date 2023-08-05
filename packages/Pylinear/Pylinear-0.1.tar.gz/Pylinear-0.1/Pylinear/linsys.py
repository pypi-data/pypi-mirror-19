from decimal import Decimal, getcontext
from copy import deepcopy

from Pylinear.vector import Vector
from Pylinear.lineq import Lineq

getcontext().prec = 30


class LinearSystem(object):

	NO_UNIQUE_SOLUTIONS_MSG = 'No unique solutions'

	def __init__(self, equations):
		try:
			d = equations[0].dimension
			for eq in equations:
				assert eq.dimension == d

			self.equations = equations
			self.dimension = d

		except AssertionError:
			raise Exception(self.ALL_EQUATIONS_MUST_BE_IN_SAME_DIM_MSG)


	def swap_rows(self, row1, row2):
		self[row1], self[row2] = self[row2], self[row1]

	def multiply_coefficient_and_row(self, coefficient, row):
		self[row] *= coefficient


	def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
		self[row_to_be_added_to] += coefficient * self[row_to_add]


	def indices_of_first_nonzero_terms_in_each_row(self):
		num_equations = len(self)
		num_variables = self.dimension

		indices = [-1] * num_equations

		for i,p in enumerate(self.planes):
			try:
				indices[i] = p.first_nonzero_index(p.normal_vector)
			except Exception as e:
				if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
					continue
				else:
					raise e

		return indices


	def __len__(self):
		return len(self.equations)


	def __getitem__(self, i):
		return self.equations[i]


	def __setitem__(self, i, x):
		try:
			assert x.dimension == self.dimension
			self.equations[i] = x

		except AssertionError:
			raise Exception(self.ALL_EQUATIONS_MUST_BE_IN_SAME_DIM_MSG)


	def __str__(self):
		ret = 'Linear System:\n'
		temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.equations)]
		ret += '\n'.join(temp)
		return ret

	def __deepcopy__(self, memo):
		copiedEquations = []
		for equation in self.equations:
			copiedEquation = deepcopy(equation)
			copiedEquations.append(copiedEquation)
		return LinearSystem(copiedEquations)

	def triangularForm(self):
		if len(self) < self.dimension: return False
		copied = deepcopy(self)
		for i in range(self.dimension):
			if copied[i][i]==0:
				found = False
				for j in range(i+1, copied.dimension):
					if copied[j][i] != 0:
						found = True
						break
				if not found: return False
				copied.swap_rows(i, j)
			copied[i] /= copied[i][i]
			for j in range(i+1, copied.dimension):
				copied.add_multiple_times_row_to_row(-copied[j][i], i, j)
		return copied

	def solve(self):
		triangle = self.triangularForm()
		if not triangle: return self.NO_UNIQUE_SOLUTIONS_MSG
		for i in range(triangle.dimension):
			if not triangle[i].valid(): return self.NO_UNIQUE_SOLUTIONS_MSG
		for i in range(self.dimension-1, -1, -1):
			for j in range(i):
				triangle.add_multiple_times_row_to_row(-triangle[j][i], i, j)
		result = [0] * triangle.dimension
		for i in range(triangle.dimension):
			result[i] = triangle[i].constant_term
		return result


class MyDecimal(Decimal):
	def is_near_zero(self, eps=1e-10):
		return abs(self) < eps


