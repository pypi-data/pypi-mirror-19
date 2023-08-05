from decimal import Decimal, getcontext

from Pylinear.vector import Vector

getcontext().prec = 30


class Line(object):

	NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

	def __init__(self, normal_vector=None, constant_term=None):
		self.dimension = 2
		if not normal_vector:
			all_zeros = [0]*self.dimension
			normal_vector = Vector(all_zeros)

		if type(normal_vector)==list or type(normal_vector)==tuple:
			normal_vector = Vector(normal_vector)

		self.normal_vector = normal_vector

		if not constant_term:
			constant_term = 0
		self.constant_term = constant_term

		try:
			assert not (normal_vector.coordinates[0]==0 and normal_vector.coordinates[1]==0 and constant_term!=0)
		except AssertionError:
			raise AssertionError("The line does not exist")

		self.set_basepoint()

	def __eq__(self, other):
		if not type(other) == Line:
			raise TypeError("The parameter should be a line object")
		if not self.parallel(other): return False
		s = other.normal_vector.coordinates[0]*self.basepoint.coordinates[0] \
			+ other.normal_vector.coordinates[1]*self.basepoint.coordinates[1]
		return s==other.constant_term

	def set_basepoint(self):
		try:
			n = self.normal_vector
			c = self.constant_term
			basepoint_coords = [0]*self.dimension

			initial_index = Line.first_nonzero_index(n.coordinates)
			initial_coefficient = n.coordinates[initial_index]

			basepoint_coords[initial_index] = c/initial_coefficient
			self.basepoint = Vector(basepoint_coords)

		except Exception as e:
			if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
				self.basepoint = None
			else:
				raise e


	def __str__(self):

		num_decimal_places = 3

		def write_coefficient(coefficient, is_initial_term=False):
			coefficient = round(coefficient, num_decimal_places)
			if coefficient % 1 == 0:
				coefficient = int(coefficient)

			output = ''

			if coefficient < 0:
				output += '-'
			if coefficient > 0 and not is_initial_term:
				output += '+'

			if not is_initial_term:
				output += ' '

			if abs(coefficient) != 1:
				output += '{}'.format(abs(coefficient))

			return output

		n = self.normal_vector

		try:
			initial_index = Line.first_nonzero_index(n.coordinates)
			terms = [write_coefficient(n.coordinates[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
					 for i in range(self.dimension) if round(n.coordinates[i], num_decimal_places) != 0]
			output = ' '.join(terms)

		except Exception as e:
			if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
				output = '0'
			else:
				raise e

		constant = round(self.constant_term, num_decimal_places)
		if constant % 1 == 0:
			constant = int(constant)
		output += ' = {}'.format(constant)

		return output

	def parallel(self, other):
		if not type(other) == Line:
			raise TypeError("The parameter should be a line object")
		return self.normal_vector.parallel(other.normal_vector)


	@staticmethod
	def first_nonzero_index(iterable):
		for k, item in enumerate(iterable):
			if not MyDecimal(item).is_near_zero():
				return k
		raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
	def is_near_zero(self, eps=1e-10):
		return abs(self) < eps
