from decimal import Decimal, getcontext
from Pylinear.vector import Vector
from copy import deepcopy
getcontext().prec = 30

class Lineq(object):

	NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

	def __init__(self, normal_vector, constant_term=0):
		try:
			assert type(normal_vector) == list or type(normal_vector) == tuple \
				or type(normal_vector) == Vector
		except AssertionError:
			raise AssertionError("The normal vector must be a list, tuple or vector object")
		try:
			assert type(constant_term) == int or type(constant_term) == float
		except AssertionError:
			raise AssertionError("The constant term must be a number")
		if type(normal_vector) == list or type(normal_vector) == tuple:
			normal_vector = Vector(normal_vector)
		self.dimension = normal_vector.dimension
		self.normal_vector = normal_vector
		self.constant_term = constant_term

		self.set_basepoint()

	def __add__(self, other):
		if type(other) == Lineq:
			try:
				assert self.dimension == other.dimension
			except Exception:
				raise AssertionError("The dimensions of the equations must be the same")
			new_normal_vector = self.normal_vector + other.normal_vector
			new_constant = self.constant_term + other.constant_term
			return Lineq(new_normal_vector, new_constant)

	def __radd__(self, other):
		if type(other) == Lineq:
			try:
				assert self.dimension == other.dimension
			except Exception:
				raise AssertionError("The dimensions of the equations must be the same")
			new_normal_vector = self.normal_vector + other.normal_vector
			new_constant = self.constant_term + other.constant_term
			return Lineq(new_normal_vector, new_constant)

	def __sub__(self, other):
		if type(other) == Lineq:
			try:
				assert self.dimension == other.dimension
			except Exception:
				raise AssertionError("The dimensions of the equations must be the same")
			new_normal_vector = self.normal_vector - other.normal_vector
			new_constant = self.constant_term - other.constant_term
			return Lineq(new_normal_vector, new_constant)

	def __mul__(self, other):
		if type(other) == int or type(other) == float:
			new_normal_vector = self.normal_vector * other
			new_constant = self.constant_term * other
			return Lineq(new_normal_vector, new_constant)

	def __rmul__(self, other):
		if type(other) == int or type(other) == float:
			new_normal_vector = self.normal_vector * other
			new_constant = self.constant_term * other
			return Lineq(new_normal_vector, new_constant)

	def __truediv__(self, other):
		if type(other) == int or type(other) == float:
			new_normal_vector = self.normal_vector / other
			new_constant = self.constant_term / other
			return Lineq(new_normal_vector, new_constant)

	def __len__(self):
		return len(self.normal_vector)

	def __getitem__(self, i):
		return self.normal_vector[i]

	def __setitem__(self, i, x):
		self.normal_vector[i] = x

	def __deepcopy__(self, memo):
		copiedVector = deepcopy(self.normal_vector)
		return Lineq(copiedVector, self.constant_term)

	def valid(self):
		if self.constant_term == 0: return True
		for i in range(len(self)):
			if self[i] != 0: return True
		return False

	def set_basepoint(self):
		try:
			n = self.normal_vector
			c = self.constant_term
			basepoint_coords = [0]*self.dimension

			initial_index = Lineq.first_nonzero_index(n.coordinates)
			initial_coefficient = n.coordinates[initial_index]

			basepoint_coords[initial_index] = c/initial_coefficient
			self.basepoint = Vector(basepoint_coords)

		except Exception as e:
			if str(e) == Lineq.NO_NONZERO_ELTS_FOUND_MSG:
				self.basepoint = None
			else:
				raise e

	def __eq__(self, other):
		if not type(other) == Lineq:
			raise TypeError("The parameter should be a Lineq object")
		if self.dimension != other.dimension:
			return False
		if not self.parallel(other): return False
		s = 0
		for i in range(self.dimension):
			s += other.normal_vector.coordinates[i]*self.basepoint.coordinates[i]
		return s==other.constant_term

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

		n = self.normal_vector.coordinates

		try:
			initial_index = Lineq.first_nonzero_index(n)
			terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
					 for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
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
		if not type(other) == Lineq:
			raise TypeError("The parameter should be a Lineq object")
		if self.dimension != other.dimension:
			raise TypeError("The dimensions of the equations should be the same")
		return self.normal_vector.parallel(other.normal_vector)


	@staticmethod
	def first_nonzero_index(iterable):
		for k, item in enumerate(iterable):
			if not MyDecimal(item).is_near_zero():
				return k
		raise Exception(Lineq.NO_NONZERO_ELTS_FOUND_MSG)

class MyDecimal(Decimal):
	def is_near_zero(self, eps=1e-10):
		return abs(self) < eps