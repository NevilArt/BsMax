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

import bpy
from bpy.types import Operator, Panel
from math import sin, cos, radians
from mathutils import Vector
from bsmax.curve import Curve

from primitive.primitive import PrimitiveGeometryClass

def get_triangle(width, length, location, direction, flip=False):
	# Return 3 vertexes in given location and direction
	# Face allways same do not need to return [0,1,2]
	direction = radians(direction)

	z = location[2]

	x1 = sin(direction) * length + location[0]
	y1 = cos(direction) * length + location[1]

	x2 = sin(direction-90) * (width/2) + location[0]
	y2 = cos(direction-90) * (width/2) + location[1]

	x3 = sin(direction+90) * (width/2) + location[0]
	y3 = cos(direction+90) * (width/2) + location[1]

	if flip:
		return [(x1, y1, z), (x3, y3, z), (x2, y2, z)]	
	return [(x1, y1, z), (x2, y2, z), (x3, y3, z)]

# width length feet_count step_width step_length path ground
# def get_step_mesh(width, length, feet_count, step_width, step_length, path, ground):

def get_step_mesh(walker):
	triangels = []	

	print(walker.rigg)
	if walker.rigg:
		for foot in walker.rigg.feet:
			foot.width
			foot.length
			triangels.append(get_triangle(foot.width, -foot.length, foot.offset, foot.direction, True))
			print(foot.width, foot.length, foot.offset, foot.direction)
	
	# Deform by path
	if walker.path:
		for triangel in triangels:
			pass

	# Combine
	verts, faces = [], []
	for index, triangel in enumerate(triangels):
		# join all vertexes
		verts += triangel
		# create new triangle faces
		f = 3*index
		faces.append([f, f+1, f+2])
	
	# Pick ground
	if walker.ground:
		for vert in verts:
			origin = vert
			success, location, _, _ = walker.ground.ray_cast(origin, (0,0,-1), distance=1000, depsgraph=None)
			if success:
				vert = location

	return verts, [], faces


class Steps(PrimitiveGeometryClass):
	def __init__(self, walker):
		self.classname = "Steps"
		self.finishon = 1
		self.owner = None
		self.data = None
		self.walker = walker
	
	def reset(self):
		self.__init__()
	
	def create(self, ctx):
		mesh = get_step_mesh(self.walker)
		self.create_mesh(ctx, mesh, self.classname)
		# pd = self.data.primitivedata
		# pd.classname = self.classname
	
	def update(self):
		mesh = get_step_mesh(self.walker)
		self.update_mesh(mesh)
	
	def abort(self):
		bpy.ops.object.delete({'selected_objects': [self.owner]})

class Foot:
	def __init__(self, bone, root):
		self.bone = bone
		self.root = root
		self.width = 0
		self.length = 0
		self.offset = Vector((0,0,0))
		self.direction = 0
		self.toch = 0
		self.release = 0
		self.analyze()
	
	def analyze(self):
		self.get_foot_dimantion()
		self.get_foot_offset()
	
	def get_foot_dimantion(self):
		# get foot shape dimantion
		co = self.bone.custom_shape.data.vertices[0].co
		scale = self.bone.custom_shape_scale
		if self.bone.use_custom_shape_bone_size:
			scale *= self.bone.length

		min_x, max_x = co.x*scale, co.x*scale
		min_y, max_y = co.y*scale, co.y*scale
		for vert in self.bone.custom_shape.data.vertices:
			x = vert.co.x * scale
			y = vert.co.y * scale
			if min_x > x: min_x = x
			if max_x < x: max_x = x
			if min_y > y: min_y = y
			if max_y < y: max_y = y
		self.width = max_x - min_x
		self.length = max_y - min_y
	
	def get_foot_offset(self):
		self.offset = 
		

class Rigg:
	def __init__(self, armature):
		self.armature = armature
		self.root = None
		self.feet = []
		if armature:
			self.analyze()
	
	def analyze(self):
		orig_pose_position = self.armature.data.pose_position
		self.armature.data.pose_position = 'REST'

		if 'root' in self.armature.pose.bones:
			self.root = self.armature.pose.bones['root']

		for key in {'foot_ik.L', 'foot_ik.R',
				'forefoot_ik.L', 'forefoot_ik.R',
				'hind_foot_ik.L', 'hind_foot_ik.R'}:
			if key in self.armature.pose.bones:
				foot_bone = self.armature.pose.bones[key]
				self.feet.append(Foot(foot_bone, self.root))

		# for bone in self.armature.pose.bones:
		# 	if bone.name in {'foot_ik.L', 'foot_ik.R',
		# 		'forefoot_ik.L', 'forefoot_ik.R',
		# 		'hind_foot_ik.L', 'hind_foot_ik.R'}:
		# 		self.feet.append(Foot(bone, self.root))

		# restore pose state
		self.armature.data.pose_position = orig_pose_position
			

class Path:
	def __init__(self, curve):
		self.curve = Curve(curve)
		self.spline_index = 0
		self.star_trim = 0
		self.end_trim = 0
		self.length = 0
		if curve:
			self.analyze()
	def analyze(self):
		self.length = self.curve.data.splines[self.spline_index].calc_length()

class Walker:
	def __init__(self, armature, path, ground):
		self.rigg = Rigg(armature)
		self.path = Path(path) if path else None
		self.ground = ground
		self.trim_start = 0
		self.trim_end = 0
		self.frame_start = 0
		self.frame_end = 0
		self.walk_speed = 1
		self.step_length = 1
		self.foot_step = None


""" User
UI
    Right panel
Get Spline length  
    Get spline
Trim start
    Float by metr
Trim End
    float by metr
Frame start
    integer
Frame End
    integer
Walk Speed
    M/S float
Walk length
    Metr float
Foot step Object
"""


class Anim_OT_Walker(Operator):
	bl_idname = 'anim.walker'
	bl_label = 'Walker'
	bl_description = 'Automate the walk cycle'

	@classmethod
	def poll(self, ctx):
		if ctx.active_object:
			return ctx.active_object.type == 'ARMATURE'
		return False

	def draw(self, ctx):
		pass
	
	def execute(self, ctx):
		steps = Steps(Walker(ctx.object, None, None))
		steps.create(ctx)
		return {'FINISHED'}
	
	def cancel(self, ctx):
		pass

	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self,width=200)


classes = [Anim_OT_Walker]

def register_walker():
    for c in classes:
	    bpy.utils.register_class(c)

def unregister_walker():
    for c in classes:
	    bpy.utils.unregister_class(c)

if __name__ == '__main__':
	register_walker()