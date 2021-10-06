from tools.internal.view import gride
import bpy
from bpy.types import Operator
from mathutils import Vector, geometry, Matrix, Euler
from math import pi, sin, cos
from bpy_extras.view3d_utils import (region_2d_to_location_3d,
	region_2d_to_vector_3d, region_2d_to_origin_3d)

from primitive.box import Box
from bsmax.state import is_object_mode
from bsmax.mouse import ray_cast

class Dimantion:
	def __init__(self):
		self.start = Vector((0, 0, 0))
		self.width = 0
		self.length = 0
		self.radius = 0
	
	def reset(self):
		self.start = Vector((0, 0, 0))
		self.width = 0
		self.length = 0
		self.radius = 0

class Click_Point:
	def __init__(self):
		self.location = Vector((0, 0, 0))
		self.normal = None

	def reset(self):
		self.location = Vector((0, 0, 0))
		self.normal = None


class Gride:
	def __init__(self):
		# First click location on view 3D
		self.location = Vector((0, 0, 0))
		# Gride rotation
		self.rotation = Vector((0, 0, 0))
		# Object rotaton (Direction)
		self.direction = Vector((0, 0, 0))
		# Click detector virtual mesh (Face)
		self.triangle = (Vector((0, 0, 0)), Vector((1, 0, 0)), Vector((0, 1, 0)))
	
	def reset(self):
		self.location = Vector((0, 0, 0))
		self.rotation = Vector((0, 0, 0))
		self.direction = Vector((0, 0, 0))
		self.triangle = (Vector((0, 0, 0)), Vector((1, 0, 0)), Vector((0, 1, 0)))
	
	def update(self):
		self.triangle = (Vector((0, 0, 0)), Vector((1, 0, 0)), Vector((0, 1, 0)))
		self.triangle = get_triface(self.location, self.rotation)
		
		for point in self.triangle:
			bpy.ops.object.empty_add(type='SPHERE', location=point, radius=0.1)

	def get_view_direction(self, ctx):
		view_rot = ctx.area.spaces.active.region_3d.view_matrix.to_euler()
		self.rotation = view_rot
	
	def get_normal_direction(self, normal):
		if normal:
			direction = normal.normalized()
			matrix = Matrix([direction, -direction.cross(normal), normal]).transposed()
			self.rotation = matrix.to_euler()
			self.rotation.y += pi/2
		else:
			self.rotation = Euler((0, 0, 0), 'XYZ')

	def get_vector_direction(self, start, end, normal):
		if start and end and normal:
			direction = (end - start).normalized()
			matrix = Matrix([direction, -direction.cross(normal), normal]).transposed()
			self.direction = matrix.to_euler()
		else:
			self.direction = Euler((0, 0, 0), 'XYZ')


def get_view_orientation(ctx):
	""" return = (str, str) (view_orientation, view_type) """
	r = lambda x: round(x, 2)

	orientation_dict = {
		(0, 0, 0):'TOP',
		(r(pi), 0, 0):'BOTTOM',
		(r(-pi/2), 0, 0):'FRONT',
		(r(pi/2), 0, r(-pi)):'BACK',
		(r(-pi/2), r(pi/2), 0):'LEFT',
		(r(-pi/2), r(-pi/2), 0):'RIGHT'}
	
	r3d = ctx.area.spaces.active.region_3d
	view_rot = r3d.view_matrix.to_euler()
	
	view_orientation = orientation_dict.get(tuple(map(r, view_rot)), 'USER')
	view_type = r3d.view_perspective
	
	return view_orientation, view_type



def get_triface(location, direction):

	""" Create a flat triangle on given location """
	# points = (location, location + Vector((1,0,0)), location + Vector((0,1,0)))
	# points = (Vector((0,0,0)), Vector((1,0,0)), Vector((0,1,0)))
	points = (Vector((-1,-1,0)), Vector((1,-1,0)), Vector((1,1,0)), Vector((-1,1,0)))

	""" rotate the triangle to given direction """
	cosa, sina = cos(direction.z), sin(direction.z)
	cosb, sinb = cos(direction.x), sin(direction.x)
	cosc, sinc = cos(direction.y), sin(direction.y)

	# cosa, sina = cos(direction.x), sin(direction.x)
	# cosb, sinb = cos(direction.y), sin(direction.y)
	# cosc, sinc = cos(direction.z), sin(direction.z)

	Axx = cosa*cosb
	Axy = cosa*sinb*sinc - sina*cosc
	Axz = cosa*sinb*cosc + sina*sinc

	Ayx = sina*cosb
	Ayy = sina*sinb*sinc + cosa*cosc
	Ayz = sina*sinb*cosc - cosa*sinc

	Azx = -sinb
	Azy = cosb*sinc
	Azz = cosb*cosc

	for i in range(len(points)):
		px, py, pz = points[i]
		points[i].x = Axx*px + Axy*py + Axz*pz + location.x
		points[i].y = Ayx*px + Ayy*py + Ayz*pz + location.y
		points[i].z = Azx*px + Azy*py + Azz*pz + location.z

	# transform to position #
	# for i in range(len(points)):
	# 	points[i] += location
	
	return points

def get_triangle_rotaion_for_view(view_orient):
	if view_orient == 'TOP':
		return Vector((0, 0, 0))
	if view_orient == 'BOTTOM':
		return Vector((pi, 0, 0))
	if view_orient == 'FRONT':
		return Vector((-pi/2, -pi/2, 0))
	if view_orient == 'BACK':
		return Vector((pi/2, -pi/2, 0))
	if view_orient == 'LEFT':
		return Vector((pi/2, 0, -pi/2))
	if view_orient == 'RIGHT':
		return Vector((0, -pi/2, 0))
	return Vector((0, 0, 0))

def get_triface_from_view(view_direction, location):
	x, y, z, = location
	if view_direction in {'FRONT','BACK'}:
		return ((0,y,0),(1,y,0),(0,y,1))
	if view_direction in {'LEFT','RIGHT'}:
		return ((x,0,0),(x,1,0),(x,0,1))
	return ((0,0,z),(0,1,z),(1,0,z))

def get_click_point_on_triangle(ctx, triangle, x, y):
	region = ctx.region
	region_data = ctx.space_data.region_3d
	view_matrix = region_data.view_matrix.inverted()
	ray_start = view_matrix.to_translation()
	ray_depth = view_matrix @ Vector((0, 0, -1000000)) #TODO from view
	ray_end = region_2d_to_location_3d(region, region_data, (x, y), ray_depth)
	return geometry.intersect_ray_tri(triangle[0], triangle[1], triangle[2], ray_end, ray_start, False)


def get_click_point_on_flore(ctx, view_type, flore_triangle, x, y):
	region = ctx.region
	region_data = ctx.space_data.region_3d
	if view_type in {'PERSP', 'CAMERA'}:
		return get_click_point_on_triangle(ctx, flore_triangle, x, y)
	return region_2d_to_location_3d(region, region_data, (x, y), (0, 0, 0))



class Draw_Primitive(Operator):
	bl_options = {'REGISTER','UNDO'}
	""" Subclass is Primitive object type """
	subclass = None
	""" Params = object.data.primitivedata """
	params = None
	""" click push/release count """
	step = 0
	""" first and current position of click point """	
	mouse_start, mouse_curent = Vector((0,0,0)), Vector((0,0,0))
	""" list of nececery keys """
	used_keys = ['LEFTMOUSE', 'RIGHTMOUSE', 'ESC', 'MOUSEMOVE', 'Z']
	""" keys for cancel opration """
	cancel_keys = ['RIGHTMOUSE', 'ESC']
	""" reserved for specila operators that needs more keys """
	request_key = []
	""" State (LMB is down), Draging wile LMB is down, cancel every thing """
	state, drag, kill = False, False, False
	""" keyboad S,C,A Flags """
	shift, ctrl, alt = False, False, False
	""" click point info """
	gride = Gride()
	point_start = Click_Point()
	point_current = Click_Point()
	draw_mode = 'FLOOR'
	""" """
	draw_handler = None
	
	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)
	
	def is_drawed_enough(self):
		""" Masaur mouse movment after object create start
		# to meke sure do not create tiny invisible object accidentaly """
		return abs(self.mouse_start.x - self.mouse_curent.x) + abs(self.mouse_start.y - self.mouse_curent.y) > 8
	
	def get_shift_state(self, event):
		if event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT'}:
			if event.value == 'PRESS':
				self.shift = True
			if event.value == 'RELEASE':
				self.shift = False
	
	def get_ctrl_state(self, event):
		if event.type in {'LEFT_CTRL', 'RIGHT_CTRL'}:
			if event.value == 'PRESS':
				self.ctrl = True
			if event.value == 'RELEASE':
				self.ctrl = False
	
	def get_alt_state(self, event):
		if event.type in {'LEFT_ALT', 'RIGHT_ALT'}:
			if event.value == 'PRESS':
				self.alt = True
			if event.value == 'RELEASE':
				self.alt = False
	
	def get_click_point_on_view3d(self, ctx, x, y):
		if self.draw_mode == 'VIEW':
			region = ctx.region
			region_data = ctx.space_data.region_3d
			location = ctx.scene.cursor.location
			point_on_view = region_2d_to_location_3d(region, region_data, (x, y), location)
			self.point_current.location = point_on_view
			return
		
		if self.draw_mode == 'SURFACE':
			location, normal, _, _ = ray_cast(ctx, x, y)
			self.point_current.location = location
			self.point_current.normal = normal
	
		if self.draw_mode == 'FLOOR' or not self.point_current.location:
			view_orient, view_type = get_view_orientation(ctx)
			direction = get_triangle_rotaion_for_view(view_orient)
			self.triangle = get_triface(self.gride.location, direction)
			self.point_current.location = get_click_point_on_flore(ctx, view_type, self.triangle, x, y)
	
	def get_click_point_on_gride(self, ctx, x, y):
		self.point_current.location = get_click_point_on_triangle(ctx, self.gride.triangle, x, y)

	
	def first_click(self, ctx, x, y):
		""" Get first click and initial basic setups """
		self.step = 1
		self.start = Vector((x,y,0))
		self.draw_mode = ctx.scene.primitive_setting.draw_mode

		self.get_click_point_on_view3d(ctx, x, y)

		if self.draw_mode == 'FLOOR':
			self.gride.location = Vector((0.0, 0.0, 0.0))
			# self.gride.location = self.point_current.location.copy()
		
		elif self.draw_mode == 'VIEW':
			self.gride.location = ctx.scene.cursor.location
			self.gride.get_view_direction(ctx)
		
		elif self.draw_mode == 'SURFACE':
			self.gride.location = self.point_current.location.copy()
			self.gride.get_normal_direction(self.point_current.normal)
			
		self.point_start.location = self.point_current.location.copy()

		self.gride.update()

		# """ tester """
		rotation = self.gride.rotation
		location = self.point_current.location
		bpy.ops.object.empty_add(type='ARROWS', location=location, rotation=rotation)

		self.create(ctx)
		
	def click_count(self, event, x, y):
		""" Count clicks and check movment (Draged or not) """
		if event.value == 'PRESS':
			self.state = True
		if event.value =='RELEASE':
			self.state = self.drag = False
			self.step += 1
			self.curent = Vector((x,y,0))
			self.point_start.location = self.point_current.location.copy()
	
	def reset(self):
		self.subclass.reset()
		self.gride.reset()
		self.point_start.reset()
		self.point_current.reset()
		self.step = 0

	def modal(self, ctx, event):
		""" Refresh Viewport """
		ctx.area.tag_redraw()

		""" Read ctrl, shiftm alt state """
		self.get_shift_state(event)
		self.get_ctrl_state(event)
		self.get_alt_state(event)

		""" Cancel operation if subclass not defined """
		if self.subclass == None:
			return {'CANCELLED'}
		
		""" Free non used keys """
		if not event.type in self.used_keys:
			return {'PASS_THROUGH'}
		
		""" Get mouse screen position """
		x, y = event.mouse_region_x, event.mouse_region_y
		
		""" Detect First click """
		if event.type == 'LEFTMOUSE':
			if self.step == 0:
				self.first_click(ctx, x, y)
				
			self.click_count(event, x, y)

		# if event.type in self.request_key:
		# 	self.event(event.type, event.value)
		# 	# dimantion.from_click_points(self.cpoint_a, self.cpoint_b, self.cpoint_o)	
		# 	self.update(ctx, self.step, dimantion)

		""" Check and update any movment """
		if event.type == 'MOUSEMOVE':
			if self.state:
				self.drag = True
			
			if self.step > 0:
				""" Get mouse click point virtual gride"""
				self.get_click_point_on_gride(ctx, x, y)

				""" Calculate the gride direction """
				start = self.point_start.location
				end = self.point_current.location
				normal = self.point_current.normal
				self.gride.get_vector_direction(start, end, normal)


				location = self.point_current.location
				rotation = self.gride.direction

				# print(location, rotation)
				# bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=location, rotation=rotation)


			""" finish or cancel operatoin by click count """
			if self.subclass.finishon > 0:
				
				if self.step >= self.subclass.finishon:
					""" Delete accidently drawed very tiny objects """
					if not self.is_drawed_enough():
						self.subclass.abort()
					else:
						self.finish()
						bpy.ops.ed.undo_push()

					self.reset()

		""" finish and drop the operator """
		if event.type in self.cancel_keys or self.kill:
			# RemoveCursurOveride(self.draw_handler)
			self.kill = False
			if self.step > 0:
				self.subclass.abort()
			self.reset()
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		# self.draw_handler = AddCursurOveride(self)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


class Create_OT_Box(Draw_Primitive):
	bl_idname = "create.box_test"
	bl_label = "Box test"
	subclass = Box()

	def create(self, ctx):
		self.subclass.create(ctx)
		owner = self.subclass.owner
		self.params = owner.data.primitivedata
		owner.location = self.point_start.location
		owner.rotation_euler = self.gride.rotation

	def update(self, ctx, clickcount, dimantion):
		print("updating")
		if clickcount == 1:
			pass
			# self.params.width = dimantion.width
			# self.params.length = dimantion.length
			# self.subclass.owner.location = dimantion.center
		elif clickcount == 2:
			pass
			# self.params.height = dimantion.height

		if clickcount > 0:
			self.subclass.update()

	def finish(self):
		print("finish")
		pass

# def create_menu(self, ctx):
# 	self.layout.prop(ctx.preferences.edit,'keyframe_new_interpolation_type', text='')

def delete_helpers():
	pass

def register_box():
	bpy.utils.register_class(Create_OT_Box)
	# bpy.types.VIEW3D_MT_object.append(create_menu)
	

def unregister_box():
	bpy.utils.unregister_class(Create_OT_Box)

if __name__ == '__main__':
	register_box()
	delete_helpers()