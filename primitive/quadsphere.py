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

import bpy
from primitive.primitive import Primitive_Geometry_Class, Draw_Primitive



# def create_cube(size, segments):
# 	vertices = []
# 	faces = []

# 	segment_size = size / segments

# 	for x in range(segments+1):
# 		for y in range(segments+1):
# 			for z in range(segments+1):
# 				vertex = (x*segment_size - size/2, y*segment_size - size/2, z*segment_size - size/2)
# 				vertices.append(vertex)
				
# 	for x in range(segments):
# 		for y in range(segments):
# 			for z in range(segments):
# 				base_index = x + y*(segments+1) + z*(segments+1)**2
# 				vertex_indices = [base_index,
# 									base_index + 1,
# 									base_index + (segments+1),
# 									base_index + (segments+1) + 1,
# 									base_index + (segments+1)**2,
# 									base_index + (segments+1)**2 + 1,
# 									base_index + (segments+1)**2 + (segments+1),
# 									base_index + (segments+1)**2 + (segments+1) + 1]
# 				if x == 0: #Bottom
# 					faces.append((vertex_indices[0], vertex_indices[2], vertex_indices[6], vertex_indices[4]))
# 				if x == segments - 1: #TOP
# 					faces.append((vertex_indices[5], vertex_indices[7], vertex_indices[3], vertex_indices[1]))
# 				if y == 0: #Front
# 					faces.append((vertex_indices[4], vertex_indices[5], vertex_indices[1], vertex_indices[0]))
# 				if y == segments - 1: #Back
# 					faces.append((vertex_indices[2], vertex_indices[3], vertex_indices[7], vertex_indices[6]))
# 				if z == 0: #left
# 					faces.append((vertex_indices[0], vertex_indices[1], vertex_indices[3], vertex_indices[2]))
# 				if z == segments - 1: #Right
# 					faces.append((vertex_indices[6], vertex_indices[7], vertex_indices[5], vertex_indices[4]))

# 	return vertices, faces



def get_quadsphere_mesh(radius, segments, percent):
	verts, faces = [], []
	
	segSize = radius * 2 / segments
	radiusB = ((radius**2) + (radius**2) + (radius**2))**0.5
	scale = radiusB / radius if radius != 0 else 1
	
	for x in range(segments+1):
		for y in range(segments+1):
			for z in range(segments+1):
				vertex = (x*segSize - radius, y*segSize - radius, z*segSize - radius)
				
				length = ((vertex[0]**2) + (vertex[1]**2) + (vertex[2]**2))**0.5		
				factor = radius / length * scale if length != 0 else 1
				factor = 1 - percent * (1 - factor) # switch factor
				vertex = (vertex[0] * factor, vertex[1] * factor, vertex[2] * factor)
				verts.append(vertex)
				
	for x in range(segments):
		for y in range(segments):
			for z in range(segments):
				base_index = x + y*(segments+1) + z*(segments+1)**2
				vertIndex = [
							base_index,
							base_index + 1,
							base_index + (segments+1),
							base_index + (segments+1) + 1,
							base_index + (segments+1)**2,
							base_index + (segments+1)**2 + 1,
							base_index + (segments+1)**2 + (segments+1),
							base_index + (segments+1)**2 + (segments+1) + 1
				]
				if x == 0: #Bottom
					faces.append((vertIndex[0], vertIndex[2], vertIndex[6], vertIndex[4]))
				if x == segments - 1: #TOP
					faces.append((vertIndex[5], vertIndex[7], vertIndex[3], vertIndex[1]))
				if y == 0: #Front
					faces.append((vertIndex[4], vertIndex[5], vertIndex[1], vertIndex[0]))
				if y == segments - 1: #Back
					faces.append((vertIndex[2], vertIndex[3], vertIndex[7], vertIndex[6]))
				if z == 0: #left
					faces.append((vertIndex[0], vertIndex[1], vertIndex[3], vertIndex[2]))
				if z == segments - 1: #Right
					faces.append((vertIndex[6], vertIndex[7], vertIndex[5], vertIndex[4]))

	return verts, [], faces



class QuadSphere(Primitive_Geometry_Class):
	def __init__(self):
		self.classname = "QuadSphere"
		self.finishon = 2

	def create(self, ctx):
		mesh = get_quadsphere_mesh(0, 6, 1)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.wsegs, pd.bias_np = 6, 1

	def update(self):
		pd = self.data.primitivedata
		mesh = get_quadsphere_mesh(pd.radius1, pd.wsegs, pd.bias_np)
		self.update_mesh(mesh)

	def abort(self):
		bpy.ops.object.delete(confirm=False)



class Create_OT_QuadSphere(Draw_Primitive):
	bl_idname = "create.quadsphere"
	bl_label = "Quad Sphere"
	subclass = QuadSphere()
	use_gride = True

	def create(self, ctx):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = self.gride.location
		self.subclass.owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimension):
		if clickcount == 1:
			self.params.radius1 = dimension.radius
		if clickcount > 0:
			self.subclass.update()



def register_quadsphere():
	bpy.utils.register_class(Create_OT_QuadSphere)

def unregister_quadsphere():
	bpy.utils.unregister_class(Create_OT_QuadSphere)

if __name__ == '__main__':
	register_quadsphere()

	# obj = QuadSphere()
	# obj.create(bpy.context)
	# obj.data.primitivedata.radius1 = 1
	# obj.data.primitivedata.wsegs = 6
	# obj.data.primitivedata.bias_np = 1
	# obj.update()
	# bpy.ops.primitive.cleardata()