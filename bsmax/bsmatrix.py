############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

from mathutils import Vector, Matrix

from math import sin, cos

#TODO collect all matrix functions and classes here

def matrix_to_array(matrix):
	"""Convert 4x4 matrix to 1D Array with 16 float value
		args:
			matrix: 4x4 matrix
		return:
			array []
	"""
	return [value for row in matrix for value in row]


def array_to_matrix(array):
	""" Conver array to 4x4 matrix

		args:
			array: 1D array with 16 float number
		return:
			mathutils 4x4 matrix
	"""

	if len(array) != 16:
		return None

	matrix = Matrix()
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


class BsMatrix:
	def __init__(self):
		self.matrix = [
			[1, 0, 0, 0],
			[0, 1, 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1]]
	
	def as_matrix(self):
		m = self.matrix
		return Matrix((
			(m[0][0], m[0][1], m[0][2], m[0][3]),
			(m[1][0], m[1][1], m[1][2], m[1][3]),
			(m[2][0], m[2][1], m[2][2], m[2][3]),
			(m[3][0], m[3][1], m[3][2], m[3][3]))) 
	
	def from_euler(self, yaw, pitch, roll):
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

		mt = self.matrix
		mt[0][0], mt[0][1], mt[0][2] = m[0][0], m[0][1], m[0][2]
		mt[1][0], mt[1][1], mt[1][2] = m[1][0], m[1][1], m[1][2]
		mt[2][0], mt[2][1], mt[2][2] = m[2][0], m[2][1], m[2][2]
