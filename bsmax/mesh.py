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



def get_selected_verts(mesh):
	""" get list of selected vertecis

		args:
			mesh: object.data
		return:
			array of selected vertecis
	"""
	return [vert for vert in mesh.vertices if vert.select]


# def create_sphere_mapped_cube(size, segments):
# 	vertices, faces = create_cube(size, segments)

# 	center = [0, 0, 0]
# 	vertices = [list(vertex) for vertex in vertices]
# 	for i, vertex in enumerate(vertices):
# 		length = math.sqrt(sum([(vertex[j] - center[j])**2 for j in range(3)]))
# 		if length != 0:
# 			for j in range(3):
# 				vertices[i][j] = (vertex[j] - center[j]) / length * size/2 + center[j]

# 	return vertices, faces