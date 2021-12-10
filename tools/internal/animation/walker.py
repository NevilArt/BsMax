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

# from sys import path
import bpy, gpu, bgl
from math import sin, cos, atan2
from mathutils import Vector
from gpu_extras.batch import batch_for_shader

from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import (PointerProperty, FloatProperty,
	StringProperty, BoolProperty, IntProperty, EnumProperty)

from bsmax.curve import Curve
from primitive.primitive import PrimitiveGeometryClass
from primitive.update import update



def get_triangle(width, length, location, direction):
	# Return 3 vertexes in given location and direction
	# Face allways same do not need to return [0,1,2]
	# direction = radians(direction)

	z = location.z

	x1 = sin(direction) * length + location.x
	y1 = cos(direction) * length + location.y

	x2 = sin(direction-90) * (width/2) + location.x
	y2 = cos(direction-90) * (width/2) + location.y

	x3 = sin(direction+90) * (width/2) + location.x
	y3 = cos(direction+90) * (width/2) + location.y

	if length < 0:
		return [[x1, y1, z], [x3, y3, z], [x2, y2, z]]	
	return [[x1, y1, z], [x2, y2, z], [x3, y3, z]]

# width length feet_count step_width step_length path ground
# def get_step_mesh(width, length, feet_count, step_width, step_length, path, ground):

def get_step_mesh(walker):
	triangels = []	

	# ignore if no rigg defined
	if not walker.rigg:
		return [], []

	for step in range(walker.step_count):
		# 
		soy = (step * -walker.step_length) - walker.step_length/2
		step_offset = Vector((0, soy, 0))
		
		for foot in walker.rigg.feet:
			# shift left and right feet
			y = walker.step_length/4 if foot.side == 'L' else -walker.step_length/4

			# swap if Left first
			if walker.start_side == 'L':
				y *= -1
			
			# Place Footsteps on path
			if walker.path:
				length = abs(soy) + y
				size = foot.length
				location, path_normal = walker.path.get_point_on_path(length, size)
				#TODO calculate the true position by normal on the curve
				location += foot.location
			
			else:
				# Place foot steps on stright line
				side_offset = Vector((0, y, 0))
				location = foot.location + side_offset + step_offset
				path_normal = 0
			
			width = foot.width * walker.step_scale
			length = -foot.length * walker.step_scale
			direction = foot.direction + path_normal
			triangels.append(get_triangle(width, length, location, direction))


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
		for index in range(len(verts)):
			success, location, _, _ = walker.ground.ray_cast(verts[index], (0,0,-1))
			if success:
				verts[index][2] = location.z

	return verts, faces

		
class Hologram:
	def __init__(self):
		self.draw_handler = None
		self.coords = []

		self.color = (1.0, 0.0, 0.0, 1.0)
		self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR') # 3D_UNIFORM_COLOR 3D_SMOOTH_COLOR
		self.batch = batch_for_shader(self.shader, 'LINES', {"pos": self.coords})
	
	def update(self, vertices, faces):
		self.coords.clear()
		for face in faces:
			size = len(face)
			for i in range(size):
				if i < size - 1:
					self.coords.append(vertices[face[i]])
					self.coords.append(vertices[face[i+1]])
				else:
					self.coords.append(vertices[face[i]])
					self.coords.append(vertices[face[0]])
	
	def draw(self):
		bgl.glEnable(bgl.GL_BLEND)
		bgl.glLineWidth(1)
		self.shader.bind()
		self.shader.uniform_float("color", self.color)
		self.batch = batch_for_shader(self.shader, 'LINES', {"pos": self.coords})
		self.batch.draw(self.shader)
	
	def register(self):
		if not self.draw_handler:
			self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw, (), 'WINDOW', 'POST_VIEW')

	def unregister(self):
		if self.draw_handler:
			bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler,'WINDOW')
			self.draw_handler = None



class Foot:
	def __init__(self, armature, bone, root, side):
		self.owner = armature
		self.bone = bone
		self.root = root
		self.side = side
		self.length = bone.length
		self.width = bone.length / 2
		self.location = bone.tail
		self.direction = 0
		self.toch = 0
		self.release = 0
		


class Rigg:
	def __init__(self):
		self.armature = None
		self._armature = ''
		self.root = None
		self.feet = []
	
	def update(self):
		if not self.armature:
			return
		elif self.armature.name == self._armature:
			return
		
		orig_pose_position = self.armature.data.pose_position
		self.armature.data.pose_position = 'REST'

		if 'root' in self.armature.pose.bones:
			self.root = self.armature.pose.bones['root']

		for key in {'foot_ik.R', 'forefoot_ik.R', 'hind_foot_ik.R'}:
			if key in self.armature.pose.bones:
				foot_bone = self.armature.pose.bones[key]
				self.feet.append(Foot(self.armature, foot_bone, self.root, 'R'))
		
		for key in {'foot_ik.L', 'forefoot_ik.L', 'hind_foot_ik.L'}:
			if key in self.armature.pose.bones:
				foot_bone = self.armature.pose.bones[key]
				self.feet.append(Foot(self.armature, foot_bone, self.root, 'L'))

		# restore pose state
		self.armature.data.pose_position = orig_pose_position
		self._armature = self.armature.name
			


class Path:
	def __init__(self):
		self.owner = None
		self.curve = None
		self.spline_index = 0
		self.star_trim = 0
		self.end_trim = 0
		self.length = 0

	def update(self):
		if self.owner:
			self.curve = Curve(self.owner)
			self.length = self.owner.data.splines[self.spline_index].calc_length()

	def get_point_on_path(self, length, size):
		# calculate time from length and trims
		time = length / self.length
		
		# get point on curve by time
		location = self.curve.splines[self.spline_index].get_point_on_spline(time)
		
		# calculate normal from two difrent point of curve (temprary solution)
		t1 = length / (self.length - size/2)
		t2 = length / (self.length + size/2)
		p1 = self.curve.splines[self.spline_index].get_point_on_spline(t1)
		p2 = self.curve.splines[self.spline_index].get_point_on_spline(t2)
		a = p2.x - p1.x
		b = p2.y - p1.y
		normal = atan2(a, b)
		return location, normal



class Walker:
	# def __init__(self, armature, path, ground):
	def __init__(self):
		# self.rigg = Rigg(armature)
		self.rigg = Rigg()
		# self.path = Path(path) if path else None
		self.path = Path()
		# self.ground = ground
		self.ground = None
		
		self.trim_start = 0.0
		self.trim_end = 0.0
		
		self.frame_start = 0
		self.frame_end = 0
		
		self.start_side = 'R'
		self.walk_speed = 1.0
		self.step_length = 1.0
		self.steps = None
		self.step_count = 10
		self.step_scale = 3

		self.hologram = Hologram()
	
	def update(self, ctx):
		# read info frome scene walker_setting
		walker_info = ctx.scene.walker_setting

		rigg_name = walker_info.rigg

		if rigg_name == '':
			self.hologram.unregister()
			return
		else:
			self.hologram.register()
		
		path_name = walker_info.path
		ground_name = walker_info.ground

		armature = bpy.data.objects[rigg_name]
		path = bpy.data.objects[path_name] if path_name != ''  else None
		ground = bpy.data.objects[ground_name] if ground_name != '' else None

		self.rigg.armature = armature
		self.rigg.update()
		self.path.owner = path
		self.path.update()
		self.ground = ground
		
		self.trim_start = walker_info.trim_start
		self.trim_end = walker_info.trim_end
	
		self.frame_start = walker_info.frame_start
		self.frame_end = walker_info.frame_end
		
		self.start_side = walker_info.start_side
		self.walk_speed = walker_info.walk_speed
		self.step_length = walker_info.step_length
		# self.steps = walker_info.steps
		self.step_count = walker_info.step_count
		self.step_scale = walker_info.step_scale

		verts, faces = get_step_mesh(self)
		self.hologram.update(verts, faces)
		
walker = Walker()



def get_scene_objects(self, ctx, type):
	armature_list = []
	for obj in bpy.data.objects:
		if obj.type == type and obj.select_get():
			armature_list.append((obj.name, obj.name, ''))
	return armature_list



def update_wlaker(self, ctx):
	walker_info = ctx.scene.walker_setting
	walker_info.totl_time = walker_info.frame_end - walker_info.frame_start
	walker.update(ctx)



class Walker_Setting(PropertyGroup):
	rigg: EnumProperty(items = lambda self,ctx: get_scene_objects(self,ctx,'ARMATURE'))
	path: EnumProperty(items = lambda self,ctx: get_scene_objects(self,ctx,'CURVE'))
	ground: EnumProperty(items = lambda self,ctx: get_scene_objects(self,ctx,'MESH'))

	trim_start: FloatProperty(name='Trim Start', min=0, max=1, default=0, description='')
	trim_end: FloatProperty(name='Trim End', min=0, max=1, default=0,description='')

	frame_start: IntProperty(name='Frame Start', min=0, default=1, description='')
	frame_end: IntProperty(name='Frame End', min=1, default=100, description='')

	start_side: EnumProperty(items = (('LEFT', 'Left', 'Start with Left Foot'),
		('RIGHT', 'Right', 'Start with Right Food')))
	walk_speed: FloatProperty(name='Walk Speed', min=0, soft_max=5, default=1, description='')
	feet: EnumProperty(items = [])
	step_length: FloatProperty(name='Step Length', min=0.001, soft_max=10, default=1, description='')
	# steps: None
	step_count: IntProperty(name='Step Count', min=0, default=10, update=update_wlaker,
		description='')
	step_scale: FloatProperty(name='Step Scale', min=1, soft_max=10, default=3, description='')

	# Display
	totl_time: IntProperty(name='Total Time', description='')
	total_length: FloatProperty(name='Total Length',description='')



class Anim_OT_Walker(Operator):
	bl_idname = 'anim.walker'
	bl_label = 'Walker'
	bl_options = {'REGISTER', 'INTERNAL'}

	action: EnumProperty(items =(
		('UPDATE', 'Update', ''),
		('APPLY', 'Apply', '')))

	def execute(self, ctx):
		if self.action == 'UPDATE':
			walker.update(ctx)
		elif self.action == 'APPLY':
			print("Apply")
		return {'FINISHED'}



class Anim_PT_Walker(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "Walker"
	bl_idname = "VIEW3D_PT_Walker"
	bl_category = 'Animation'

	@classmethod
	def poll(self, ctx):
		return True

	def draw(self, ctx):
		layout = self.layout
		walker_info = ctx.scene.walker_setting

		box = layout.box()
		box.prop(walker_info, 'rigg', text='Rigg')
		box.prop(walker_info, 'path', text='Path')
		box.prop(walker_info, 'ground', text='Ground')
		
		box = layout.box()
		box.prop(walker_info, 'trim_start')
		box.prop(walker_info, 'trim_end')

		box.prop(walker_info, 'frame_start')
		box.prop(walker_info, 'frame_end')

		box.prop(walker_info, 'walk_speed')
		box.prop(walker_info, 'step_length')
		box.prop(walker_info, 'step_count', text='Steps')
		box.prop(walker_info, 'step_scale', text='Icon Scale')

		box = layout.box()
		box.prop(walker_info, 'start_side', text='Start')
		box.prop(walker_info, 'feet', text='Foot')

		box = layout.box()
		box.enabled = False
		box.prop(walker_info, 'totl_time')
		box.prop(walker_info, 'total_length')
		
		box = layout.box()
		row = box.row()
		row.operator('anim.walker', text='Update').action='UPDATE'
		row.operator('anim.walker', text='Apply').action='APPLY'



classes = [Walker_Setting, Anim_OT_Walker, Anim_PT_Walker]

def register_walker():
	for c in classes:
		bpy.utils.register_class(c)
		bpy.types.Scene.walker_setting = PointerProperty(type=Walker_Setting)

def unregister_walker():
	del bpy.types.Scene.walker_setting
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	register_walker()