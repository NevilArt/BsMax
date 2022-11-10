############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

import numpy
from math import sqrt, sin, cos
from mathutils import Vector, Matrix

from .math import dot



def matrix_to_array(matrix):
	"""Convert 4x4 matrix to 1D Array with 16 float value
		args:
			matrix: 4x4 matrix or BsMatrix
		return:
			array []
	"""
	if isinstance(matrix, BsMatrix):
		return [value for row in matrix.matrix for value in row]
	else:
		return [value for row in matrix for value in row]



def array_to_matrix(array, cls=None):
	""" Convert array to 4x4 matrix

		args:
			array: 1D array with 16 float number
		return:
			mathutils 4x4 matrix
	"""

	if len(array) != 16:
		return None

	# if cls is BsMatrix use it else create new one
	matrix = cls.matrix if cls else Matrix()

	matrix[0][0] = array[0]
	matrix[0][1] = array[1]
	matrix[0][2] = array[2]
	matrix[0][3] = array[3]

	matrix[1][0] = array[4]
	matrix[1][1] = array[5]
	matrix[1][2] = array[6]
	matrix[1][3] = array[7]

	matrix[2][0] = array[8]
	matrix[2][1] = array[9]
	matrix[2][2] = array[10]
	matrix[2][3] = array[11]

	matrix[3][0] = array[12]
	matrix[3][1] = array[13]
	matrix[3][2] = array[14]
	matrix[3][3] = array[15]

	return matrix



def bsmatrix_to_matrix(cls):
	""" convert BsMarix class to mathutils.matrix

		args:
			cls: BsMatrix
		return:
			mathutils.matrix
	"""
	m = cls.matrix
	return Matrix((
		(m[0][0], m[0][1], m[0][2], m[0][3]),
		(m[1][0], m[1][1], m[1][2], m[1][3]),
		(m[2][0], m[2][1], m[2][2], m[2][3]),
		(m[3][0], m[3][1], m[3][2], m[3][3]))) 


def matrix_to_bsmatrix(cls, matrix):
	""" Get BsMatrix from other matrix types
		args:
			cls: BsMatrix
			matrix: any other matrix type
		return:
			None
	"""
	m, n = cls.matrix, matrix

	m[0][0] = n[0][0]
	m[0][1] = n[0][1]
	m[0][2] = n[0][2]
	m[0][3] = n[0][3]

	m[1][0] = n[1][0]
	m[1][1] = n[1][1]
	m[1][2] = n[1][2]
	m[1][3] = n[1][3]

	m[2][0] = n[2][0]
	m[2][1] = n[2][1]
	m[2][2] = n[2][2]
	m[2][3] = n[2][3]

	m[3][0] = n[3][0]
	m[3][1] = n[3][1]
	m[3][2] = n[3][2]
	m[3][3] = n[3][3]



def euler_to_matrix(matrix, yaw, pitch, roll):
	""" BsMatrix rotation from eulr elements

		args:
			matrix: BsMatrix class or mathutils Matrix
			yaw: float radian Euler rotaion X
			pitch: float radian Euler rotaion Y
			roll: float radian Euler rotaion Z
		return:
			mathutils Matrix
	"""
	sy, cy = sin(yaw), cos(yaw)
	Rz_yaw = (
		Vector((cy, -sy, 0)),
		Vector((sy,  cy, 0)),
		Vector((0,	0, 1)))

	sp, cp = sin(pitch), cos(pitch)
	Ry_pitch = (
		Vector(( cp, 0, sp)),
		Vector((  0, 1, 0)),
		Vector((-sp, 0, cp)))

	sr, cr = sin(roll), cos(roll) 
	Rx_roll = (
		Vector((1,  0,   0)),
		Vector((0, cr, -sr)),
		Vector((0, sr,  cr)))
		
	m = numpy.dot(Rz_yaw, numpy.dot(Ry_pitch, Rx_roll))

	# use bsmatrix if matrix type is Bsmatrix else create new matrix and return
	mt = matrix.matrix if isinstance(matrix, BsMatrix) else matrix
	mt[0][0], mt[0][1], mt[0][2] = m[0][0], m[0][1], m[0][2]
	mt[1][0], mt[1][1], mt[1][2] = m[1][0], m[1][1], m[1][2]
	mt[2][0], mt[2][1], mt[2][2] = m[2][0], m[2][1], m[2][2]

	return mt



def matrix_from_quaternion(matrix , quaternion):
	""" Get matrix rotation from quaternion

		args:
			matrix: BsMatrix class or mathutils Matrix
			quaternion: quaternion rotation ot 4x Vector or array
		return:
			mathutils Matrix
	"""
	x, y, z, w = quaternion
	mt = matrix.matrix if isinstance(matrix, BsMatrix) else matrix
	# [1, 0, 0] Xv
	mt[0][0] = 1 - 2*y*y - 2*z*z
	mt[0][1] = 2*x*y - 2*z*w
	mt[0][2] = 2*x*z + 2*y*w

	# [0, 1, 0] Yv
	mt[1][0] = 2*x*y + 2*z*w
	mt[1][1] = 1 - 2*x*x - 2*z*z
	mt[1][2] = 2*y*z - 2*x*w

	# [0, 0, 1] Zv
	mt[2][0] = 2*x*z - 2*y*w
	mt[2][1] = 2*y*z + 2*x*w
	mt[2][2] = 1 - 2*x*x - 2*y*y

	return mt


def matrix_to_quaternion(matrix):
	""" Get Quaternion rotation from matrix

		args:
			matrix: BsMatrix class or mathutils Matrix
		return:
			numpy.quaternion
	"""
	q = numpy.quaternion()
	m = matrix.matrix if isinstance(matrix, BsMatrix) else matrix
	trace = m[0][0] + m[1][1] + m[2][2]
	if trace > 0 :
		s = 0.5 / sqrt(trace + 1)
		q.w = 0.25 / s
		q.x = (m[2][1] - m[1][2] ) * s
		q.y = (m[0][2] - m[2][0] ) * s
		q.z = (m[1][0] - m[0][1] ) * s

	else:
		if m[0][0] > m[1][1] and m[0][0] > m[2][2]:
			s = 2 * sqrt(1 + m[0][0] - m[1][1] - m[2][2])
			q.w = (m[2][1] - m[1][2]) / s
			q.x = 0.25 * s
			q.y = (m[0][1] + m[1][0] ) / s
			q.z = (m[0][2] + m[2][0] ) / s

		elif m[1][1] > m[2][2]:
			s = 2 * sqrt( 1 + m[1][1] - m[0][0] - m[2][2])
			q.w = (m[0][2] - m[2][0] ) / s
			q.x = (m[0][1] + m[1][0] ) / s
			q.y = 0.25 * s
			q.z = (m[1][2] + m[2][1] ) / s

		else:
			s = 2 * sqrt( 1 + m[2][2] - m[0][0] - m[1][1] )
			q.w = (m[1][0] - m[0][1] ) / s
			q.x = (m[0][2] + m[2][0] ) / s
			q.y = (m[1][2] + m[2][1] ) / s
			q.z = 0.25 * s

	return q


def matrix_to_scale(matrix):
	""" Extract Scale from matrix

		args:
			matrix: BsMatrix class or mathutils Matrix
		return:
			Vector3
	"""
	m = matrix.matrix if isinstance(matrix, BsMatrix) else matrix
	x = sqrt(m[0][0]*m[0][0] + m[0][1]*m[0][1] + m[0][2]*m[0][2])
	y = sqrt(m[1][0]*m[1][0] + m[1][1]*m[1][1] + m[1][2]*m[1][2])
	z = sqrt(m[2][0]*m[2][0] + m[2][1]*m[2][1] + m[2][2]*m[2][2])

	return Vector(x, y, z)



def matrix_from_elements(location, euler_rotation, scale, bsmatrix=None):
	""" Combine parts and make a transform matrix

		args:
			location: Vector(3) translation
			euler_rotation:
			scale: Vector3 scale
			bsmatrix: BsMatrix class
		return:
			mathutils Matrix
			None if bsmatrix given
	"""
	roll, pitch, yaw = euler_rotation

	Rz_yaw = numpy.array([
		[cos(yaw), -sin(yaw), 0],
		[sin(yaw), cos(yaw), 0],
		[0, 0, 1]])
	
	Ry_pitch = numpy.array([
		[cos(pitch), 0, sin(pitch)],
		[0, 1, 0],
		[-sin(pitch), 0, cos(pitch)]])

	Rx_roll = numpy.array([
		[1, 0, 0],
		[0, cos(roll), -sin(roll)],
		[0, sin(roll), cos(roll)]])

	m = numpy.dot(Rz_yaw, numpy.dot(Ry_pitch, Rx_roll))

	# Convert Arry to Matrix and apply location and scale
	lx, ly, lz = location
	sx, sy, sz = scale

	if bsmatrix:
		bm = bsmatrix.matrix
		bm[0][0], bm[0][1], bm[0][2], bm[0][3] = m[0][0]*sx, m[0][1]*sy, m[0][2]*sz, lx
		bm[1][0], bm[1][1], bm[1][2], bm[1][3] = m[1][0]*sx, m[1][1]*sy, m[1][2]*sz, ly
		bm[2][0], bm[2][1], bm[2][2], bm[2][3] = m[2][0]*sx, m[2][1]*sy, m[2][2]*sz, lz
		bm[3][0], bm[3][1], bm[3][2], bm[3][3] = 0, 0, 0, 1

		return None

	else:
		matrix = Matrix((
			(m[0][0]*sx, m[0][1]*sy, m[0][2]*sz, lx),
			(m[1][0]*sx, m[1][1]*sy, m[1][2]*sz, ly),
			(m[2][0]*sx, m[2][1]*sy, m[2][2]*sz, lz),
			(0, 0, 0, 1)))

		return matrix



def matrix_inverse(matrix):
	""" Invers the matrix

		args:
			matrix: BsMatrix class or mathutils Matrix

		return:
			mathutils Matrix			
	"""
	m = matrix.matrix if isinstance(matrix, BsMatrix) else matrix

	n = Matrix((
		(1, 0, 0, -m[0][3]),
		(0, 1, 0, -m[1][3]),
		(0, 0, 1, -m[2][3]),
		(0, 0, 0, 1)))

	m00, m01, m02, _ = m[0]
	m10, m11, m12, _ = m[1]
	m20, m21, m22, _ = m[2]
	
	a1 = m00*m11*m22 + m01*m12*m20 + m02*m10*m21
	a2 = m20*m11*m02 + m21*m12*m00 + m22*m10*m01
	a = 1/(a1-a2)

	n[0][0] =  (m11*m22 - m12*m21) * a
	n[1][0] = -(m10*m22 - m12*m20) * a
	n[2][0] =  (m10*m21 - m11*m20) * a

	n[0][1] = -(m01*m22 - m02*m21) * a
	n[1][1] =  (m00*m22 - m02*m20) * a
	n[2][1] = -(m00*m21 - m01*m20) * a

	n[0][2] =  (m01*m22 - m02*m21) * a
	n[1][2] = -(m00*m12 - m02*m10) * a
	n[2][2] =  (m00*m11 - m01*m10) * a

	return n


def points_to_local_matrix(points, matrix):
	""" transform points to new matrix

		args:
			point: Vector3 or Array of Vector3
			matrix: Matrix of destenation transform

		return:
			same type as given point argoment
	"""
	# calculate one for all
	translation = matrix.translation
	euler = matrix.to_euler()
	ys, yc = sin(-euler.z), cos(-euler.z)
	ps, pc = sin(-euler.x), cos(-euler.x)
	rs, rc = sin(-euler.y), cos(-euler.y)
	scale = matrix.to_scale()
	s = Vector((1/scale.x, 1/scale.y, 1/scale.z))

	if isinstance(points, list):
		new_points = []
		for point in points:
			# Untranslating
			p = point - matrix.translation
			# UnYawing
			p = Vector((p.x*yc - p.y*ys, p.y*yc + p.x*ys, p.z))
			# Unpinching
			p = Vector((p.x, p.y*pc - p.z*ps, p.z*pc + p.y*ps))
			# Unrolling
			p = Vector((p.x*rc + p.z*rs, p.y, p.z*rc - p.x*rs))
			# UnScaling and collect
			new_points.append(Vector((p.x*s.x, p.y*s.y, p.z*s.z)))

		return new_points
	
	else:
		# Untranslating
		p = points - translation
		# UnYawing
		p = Vector((p.x*yc - p.y*ys, p.y*yc + p.x*ys, p.z))
		# Unpinching
		p = Vector((p.x, p.y*pc - p.z*ps, p.z*pc + p.y*ps))
		# Unrolling
		p = Vector((p.x*rc + p.z*rs, p.y, p.z*rc - p.x*rs))
		# UnScaling and return
		return Vector((p.x*s.x, p.y*s.y, p.z*s.z))



# temprary function
def transfer_points_to(points ,location, direction):
	""" Temprary function for transfer point3 to new location and rotation
		
		args:
			points: Vector3
			location: Vectore3
			direction: Vector3
		return:
			Vector3 point in new location
	"""
	xa, ya, za = direction
	rx = numpy.matrix([[1, 0, 0], [0, cos(xa),-sin(xa)], [0, sin(xa), cos(xa)]])
	ry = numpy.matrix([[cos(ya), 0, sin(ya)], [0, 1, 0], [-sin(ya), 0, cos(ya)]])
	rz = numpy.matrix([[cos(za), -sin(za), 0], [sin(za), cos(za) ,0], [0, 0, 1]])
	tr = rx * ry * rz

	for i in range(len(points)):
		px, py, pz = points[i]
		points[i].x = px*tr.item(0) + py*tr.item(1) + pz*tr.item(2) + location.x
		points[i].y = px*tr.item(3) + py*tr.item(4) + pz*tr.item(5) + location.y
		points[i].z = px*tr.item(6) + py*tr.item(7) + pz*tr.item(2) + location.z

	return points


def transform_point_to_matrix(point, matrix):
	""" Get Point location on other matrix

		args:
			point: aray or Vector3
			matrix: matrix or bsmatrix
		return:
			point: same type of entry in local coordinate
	"""
	m = matrix.matrix if isinstance(matrix, BsMatrix) else matrix
	rxv = Vector((m[0][0], m[0][1], m[0][2]))
	ryv = Vector((m[1][0], m[1][1], m[1][2]))
	rzv = Vector((m[2][0], m[2][1], m[2][2]))
	tv  = Vector((m[0][3], m[1][3], m[2][3]))
	if isinstance(point, list) or isinstance(point, tuple):
		new_points = []
		for pv in point:
			x = dot(pv, rxv) + tv.x
			y = dot(pv, ryv) + tv.y
			z = dot(pv, rzv) + tv.z
			new_points.append(Vector((x, y, z)))
		return new_points
	else:
		x = dot(point, rxv) + tv.x
		y = dot(point, ryv) + tv.y
		z = dot(point, rzv) + tv.z
		return Vector((x, y, z))



class BsMatrix:
	""" All transform function (I know python has all of this but this is about learning)\n
		[1, 0, 0, 0]\n
		[0, 1, 0, 0]\n
		[0, 0, 1, 0]\n
		[0, 0, 0, 1]
	"""
	def __init__(self):
		self.matrix = [
			[1, 0, 0, 0],
			[0, 1, 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1]
		]

	def from_matrix(self, matrix):
		"""conver regular matrix to BsMatrix"""
		matrix_to_bsmatrix(self, matrix)

	def to_matrix(self):
		"""Get regular matrix of BsMatrix"""
		return bsmatrix_to_matrix(self)

	def from_array(self, array):
		"""Conver 4x4 matrix to BsMatrix"""
		array_to_matrix(array, cls=self)
	
	def to_array(self):
		"""Convert to 4X4 matrix"""
		return matrix_to_array(self.matrix)

	def from_translation(self, location):
		"""get translation from vector3"""
		m = self.matrix
		m[0][3], m[1][3], m[2][3] = location

	def to_translation(self):
		"""return traslation as vector3"""
		m = self.matrix
		return Vector(m[0][3], m[1][3], m[2][3])

	def from_euler(self, euler):
		"""get rotation from euler XYZ
			TODO Add other euler types too
		"""
		euler_to_matrix(self, euler.x, euler.y, euler.z)
	
	def to_euler(self):
		"""TODO return rotation as euler"""
		return []

	def from_quaternion(self, quaternion):
		"""get rotation from quaternion rotation"""
		matrix_from_quaternion(self, quaternion)

	def to_quaternion(self):
		"""return rotation as quaterion"""
		return matrix_to_quaternion(self)

	def from_axis_angle(self, order):
		"""TODO get rotation from axis angle"""
		pass

	def to_axis_angle(self):
		"""TODO return rotation as axis angle"""
		return Vector(0, 0, 0)

	def from_scale(self, scale):
		"""TODO get scale from vector3"""
		pass

	def to_scale(self):
		"""return scale as vector3"""
		return matrix_to_scale(self)

	def inverse(self):
		"""return invers of the matrix"""
		return matrix_inverse(self)
	
	def point_to_local(self, points):
		"""put point in a local matrix of the current"""
		return points_to_local_matrix(points, self.matrix)

	def point_to_world(self, points):
		"""put point in world matrix"""
		return points_to_local_matrix(points, self.inverse())

	def from_string(self):
		"""TODO get BsMatrix from string"""
		pass

	def to_string(self):
		"""TODO conver BsMatrix to string"""
		return ""