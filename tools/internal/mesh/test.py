import bpy

import numpy as np

from primitive.primitive import Primitive_Geometry_Class



def get_concave_vertices(vertices):
	concaveVertices = []

	# Convert the vertices to a numpy array for easier computation
	vertices = np.array(vertices)

	for i in range(len(vertices)):
		currentVertex = vertices[i].co
		prevVertex = vertices[i - 1].co
		nextVertex = vertices[(i + 1) % len(vertices)].co  # Wrap around to the first vertex
		
		# Calculate the cross product of the vectors formed by the adjacent vertices
		cross_product = np.cross(prevVertex - currentVertex, nextVertex - currentVertex)
		
		print(cross_product)
		# If the cross product is negative, it means the vertex is concave
		# if cross_product < 0:
		# 	concaveVertices.append(currentVertex)

	return concaveVertices


def get_convex_hull_vertices(vertices):
	def find_furthest_point_index(points, start_index, end_index):
		max_distance = -1
		furthest_index = -1

		for i in range(start_index, end_index):
			distance = (points[i] - points[start_index]).dot(normalized_direction)
			if distance > max_distance:
				max_distance = distance
				furthest_index = i

		return furthest_index

	def find_points_on_side(points, start_index, end_index, point_index):
		side_points = []
		direction = points[end_index] - points[start_index]
		for i in range(len(points)):
			if i != start_index and i != end_index and i != point_index:
				point_direction = points[i] - points[start_index]
				cross_product = np.cross(direction, point_direction)
				if cross_product < 0:
					side_points.append(i)

		return side_points

	def build_hull(points, start_index, end_index):
		if len(points) == 0:
			return []

		furthest_index = find_furthest_point_index(points, start_index, end_index)
		if furthest_index == -1:
			return [start_index, end_index]

		left_side_points = find_points_on_side(points, start_index, furthest_index, end_index)
		right_side_points = find_points_on_side(points, furthest_index, end_index, start_index)

		hull = []
		hull.extend(build_hull(points, start_index, furthest_index))
		hull.append(furthest_index)
		hull.extend(build_hull(points, furthest_index, end_index))

		return hull

	# Convert the vertices to a numpy array for easier computation
	points = np.array(vertices)

	# Find the leftmost and rightmost points
	leftmost_index = np.argmin(points[:, 0])
	rightmost_index = np.argmax(points[:, 0])

	# Build the hull recursively
	hull = build_hull(points, leftmost_index, rightmost_index)

	# Get the coordinates of the convex hull vertices
	convex_hull_vertices = [vertices[index] for index in hull]

	return convex_hull_vertices




def test(ctx):
	vertices = ctx.object.data.vertices
	newVertices = get_concave_vertices(vertices)
	print(newVertices)
	return newVertices, [], []



class TestConcave(Primitive_Geometry_Class):
	def init(self):
		self.classname = "Test"
		self.finishon = 1

	def create(self, ctx):
		mesh = test(bpy.context)
		# self.create_mesh(ctx, mesh, self.classname)

	def update(self):
		pass

	def abort(self):
		pass



tt = TestConcave()
tt.create(bpy.context)


def cubic_bezier_length(A, B, C, D, num_segments=100):
	def derivative(t):
		return 3 * (-A + 3 * (B - C) * t + 3 * (A - 2 * B + C) * t**2 + (D - A + 3 * (B - C)) * t**3)

	def integrand(t):
		return np.sqrt(np.sum(derivative(t)**2))

	t_values = np.linspace(0, 1, num_segments + 1)
	segment_length = 1 / num_segments

	weights = np.array([0.171324492379170, 0.360761573048139, 0.467913934572691])
	abscissas = np.array([0.932469514203152, 0.661209386466265, 0.238619186083197])

	total_length = 0.0
	for i in range(num_segments):
		segment_sum = 0.0
		for j in range(3):
			t = 0.5 * (t_values[i] + 1 + abscissas[j] * segment_length)
			segment_sum += weights[j] * integrand(t)
		
		total_length += 0.5 * segment_length * segment_sum

	return total_length
