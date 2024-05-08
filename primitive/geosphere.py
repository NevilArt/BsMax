############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################

from math import sqrt

def create_geodesic_sphere(radius, subdivision_level):
	vertices = []
	indices = []
	
	# Golden ratio
	phi = (1 + sqrt(5)) / 2
	
	# Vertices of the icosahedron
	vertices.extend([
		(-1, phi, 0), (1, phi, 0), (-1, -phi, 0), (1, -phi, 0),
		(0, -1, phi), (0, 1, phi), (0, -1, -phi), (0, 1, -phi),
		(phi, 0, -1), (phi, 0, 1), (-phi, 0, -1), (-phi, 0, 1)
	])
	
	# Faces of the icosahedron
	indices.extend([
		(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
		(1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
		(3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
		(4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)
	])
	
	# Subdivide faces
	for _ in range(subdivision_level):
		new_indices = []
		for i1, i2, i3 in indices:
			v1 = vertices[i1]
			v2 = vertices[i2]
			v3 = vertices[i3]
			
			# Compute midpoints
			midpoints = [
				((v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2, (v1[2] + v2[2]) / 2),
				((v2[0] + v3[0]) / 2, (v2[1] + v3[1]) / 2, (v2[2] + v3[2]) / 2),
				((v3[0] + v1[0]) / 2, (v3[1] + v1[1]) / 2, (v3[2] + v1[2]) / 2)
			]
			
			# Normalize midpoints
			midpoints = [
				tuple(
					v / sqrt(v[0]**2 + v[1]**2 + v[2]**2) * radius for v in m
				) for m in midpoints
			]
		
			# Add new vertices
			vertices.extend(midpoints)
			i4, i5, i6 = range(len(vertices) - 3, len(vertices))
			
			# Add new indices
			new_indices.extend([
				(i1, i4, i6), (i4, i2, i5), (i4, i5, i6), (i6, i5, i3)
			])
		indices = new_indices
	
	return vertices