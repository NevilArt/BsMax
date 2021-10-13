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

import bpy, numpy
from bpy.types import Operator
from mathutils import Vector, geometry, Matrix, Euler
from math import pi, sin, cos, sqrt
from bpy_extras.view3d_utils import region_2d_to_location_3d
from bsmax.state import is_object_mode
from bsmax.mouse import ray_cast
from .primitive import AddCursurOveride, RemoveCursurOveride


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



def get_rotation_of_view_orient(view_orient):
		if view_orient == 'TOP':
			return Vector((0, 0, 0))
		if view_orient == 'BOTTOM':
			return Vector((pi, 0, 0))
		if view_orient == 'FRONT':
			return Vector((pi/2, 0, 0))
		if view_orient == 'BACK':
			return Vector((-pi/2, pi, 0))
		if view_orient == 'LEFT':
			return Vector((pi/2, 0, -pi/2))
		if view_orient == 'RIGHT':
			return Vector((pi/2, 0, pi/2))
		return Vector((0, 0, 0))



def transfer_points_to(points ,location, direction):
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
	


def get_click_point_on_face(ctx, face, x, y):
		region = ctx.region
		region_data = ctx.space_data.region_3d
		_, view_type = get_view_orientation(ctx)
		if view_type in {'PERSP', 'CAMERA'}:
			region = ctx.region
			region_data = ctx.space_data.region_3d
			view_matrix = region_data.view_matrix.inverted()
			ray_start = view_matrix.to_translation()
			ray_depth = view_matrix @ Vector((0, 0, -1000000)) #TODO from view
			ray_end = region_2d_to_location_3d(region, region_data, (x, y), ray_depth)
			return geometry.intersect_ray_tri(face[0], face[1], face[2], ray_end, ray_start, False)
		return region_2d_to_location_3d(region, region_data, (x, y), (0, 0, 0))



class Dimantion:
	def __init__(self, gride, start, end):
		self.gride = gride
		self.start = start
		self.end = end
		self.location = end

		self.width = 0
		self.length = 0
		self.height = 0
		""" Distance of start and current """
		self.radius = 0
		""" Distance of gride and current """
		self.distance = 0
		self.center = Vector((0, 0, 0))
		self.calculate()
	
	def calculate(self):
		# radiue distance of start and end point
		x = self.end.x - self.start.x
		y = self.end.y - self.start.y
		z = self.end.z - self.start.z
		self.radius = sqrt(x**2 + y**2 + z**2)
		
		# distance of gride and end point
		x = self.end.x - self.gride.location.x
		y = self.end.y - self.gride.location.y
		z = self.end.z - self.gride.location.z
		self.distance = sqrt(x**2 + y**2 + z**2)
		
		# weidth length height
		theta = self.gride.rotation.z
		
		width = self.radius*cos(pi - theta)
		length = self.radius*cos(theta)
		
		self.width = abs(width)
		self.length = abs(length)
		self.height = self.radius
		
		# center
		cx = (self.start.x + self.end.x) / 2
		cy = (self.start.y + self.end.y) / 2
		cz = (self.start.z + self.end.z) / 2
		self.center = Vector((cx, cy, cz))
	

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
		self.rotation = Vector((0, 0, 0)) #orientation
		# Object rotaton (Direction)
		self.direction = Vector((0, 0, 0))
		# Floor oriantation
		self.orient = Vector((0, 0, 0))
		# Size of gride for graphic drawing
		self.size = 1
		# Click detector virtual mesh (Face) on surface
		self.face = self.get_defualt_face()
		# Click detector virtual mesh (Face) on floore
		self.floor = self.get_defualt_face()
	
	def get_defualt_face(self):
		return (Vector((-self.size, -self.size, 0)), Vector((self.size, -self.size, 0)),
			Vector((self.size, self.size, 0)), Vector((-self.size, self.size, 0)))
	
	def reset(self):
		self.location = Vector((0, 0, 0))
		self.rotation = Vector((0, 0, 0))
		self.direction = Vector((0, 0, 0))
		self.face = self.get_defualt_face()

	def genarate_face(self):
		self.face = transfer_points_to(self.get_defualt_face(), self.location, self.rotation)
	
	def genarate_floor(self):
		self.floor = transfer_points_to(self.get_defualt_face(), Vector((0, 0, 0)), Vector((0, 0, 0)))

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
			self.rotation = matrix.to_euler()
		else:
			self.rotation = Euler((0, 0, 0), 'XYZ')

	def get_click_point_gride(self, ctx, x, y):
		return get_click_point_on_face(ctx, self.face, x, y)
	
	def get_click_point_surface(self, ctx, x, y):
		point, _, _, _ = ray_cast(ctx, x, y)
		if point:
			return point
		view_orient, _ = get_view_orientation(ctx)
		self.rotation = get_rotation_of_view_orient(view_orient)
		self.genarate_face()
		return get_click_point_on_face(ctx, self.face, x, y)
	
	def get_coordinate(self, ctx, x, y):
		""" call once at first click to ganarate virtual gride """
		draw_mode = ctx.scene.primitive_setting.draw_mode
		if draw_mode == 'VIEW':
			region = ctx.region
			region_3d = ctx.space_data.region_3d
			location = ctx.scene.cursor.location

			center_x, center_y  = ctx.area.width/2, ctx.area.height/2
			point_start = region_2d_to_location_3d(region, region_3d, (center_x, center_y ), location)
			point_end = region_2d_to_location_3d(region, region_3d, (center_x+5, center_y ), location)
			view_pos = region_3d.view_matrix.to_translation()
			center_pos = point_start
			
			vector = center_pos - view_pos
			length = sqrt(vector.x**2 + vector.y**2 + vector.z**2)
			normal = Vector((vector.x/length, vector.y/length, vector.z/length))

			direction = (point_end - point_start).normalized()
			matrix = Matrix([direction, -direction.cross(normal), normal]).transposed()
			rotation = matrix.to_euler()

			self.rotation = rotation # TODO not coorect result

			self.location = region_2d_to_location_3d(region, region_3d, (x, y), location)
		
		if draw_mode == 'SURFACE':
			start, normal, _, _ = ray_cast(ctx, x, y)
			end, _, _, _ = ray_cast(ctx, x+1, y)
			self.get_vector_direction(start, end, normal)
			self.location = start
			self.direction = self.rotation.copy()
			if start:
				self.genarate_face()

		if draw_mode == 'FLOOR' or not self.location:
			view_orient, _ = get_view_orientation(ctx)
			self.rotation = get_rotation_of_view_orient(view_orient)
			self.genarate_floor()
			self.location = get_click_point_on_face(ctx, self.floor, x, y)
			self.direction = self.rotation.copy()



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
	""" 3D coordinate and info of click points """
	point_start, point_current = Click_Point(), Click_Point()
	""" flag that choos click point type use gride or not """
	use_gride = False
	use_surface = False
	use_single_click = False
	""" mouse override graphic handler """
	draw_handler = None
    # Temprary #
	mpos = Vector((0, 0, 0))
	
	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)
	
	def acceptable(self):
		""" Check mouse movment make sure do not create tiny invisible object"""
		length = abs(self.mouse_start.x - self.mouse_curent.x) + abs(self.mouse_start.y - self.mouse_curent.y)
		return length > 8 or (length == 0 and self.use_single_click)
	
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
	
	
	def first_click(self, ctx, x, y):
		""" Get first click and initial basic setups """
		self.step = 1
		self.mouse_start = Vector((x,y,0))
		self.use_surface = ctx.scene.primitive_setting.draw_mode == 'SURFACE'

		""" Create local Gride """
		self.gride.get_coordinate(ctx, x, y)

		""" Get First Click Point """
		self.point_current.location = self.gride.location.copy()
		self.point_start.location = self.point_current.location.copy()

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
		#TODO replace with Start End after all operator replace with Draw_Primitive
		self.mpos = Vector((x, y, 0))
		
		""" Detect First click """
		if event.type == 'LEFTMOUSE':
			if self.step == 0:
				self.first_click(ctx, x, y)
				
			self.click_count(event, x, y)

		""" Check and update any movment """
		if event.type == 'MOUSEMOVE':
			if self.state:
				self.drag = True
			
			if self.step > 0:
				""" Get mouse click point virtual gride"""
				self.mouse_curent = Vector((x,y,0))
				
				if self.use_gride:
					self.point_current.location = self.gride.get_click_point_gride(ctx, x, y)
				elif self.use_surface:
					self.point_current.location = self.gride.get_click_point_surface(ctx, x, y)
				else:
					self.point_current.location = self.gride.get_click_point_gride(ctx, x, y)
				
				dimantion = Dimantion(self.gride, self.point_start.location, self.point_current.location)
				self.update(ctx, self.step, dimantion)

			""" finish or cancel operatoin by click count """
			if self.subclass.finishon > 0:
				
				if self.step >= self.subclass.finishon:
					""" Delete accidently drawed very tiny objects """
					if self.acceptable():
						self.finish()
						bpy.ops.ed.undo_push()
					else:
						self.subclass.abort()
						

					self.reset()
		
		""" abort if pointer go out of screen """
		# if self.step == 0 and out of screen:
		# 	self.kill = True

		""" finish and drop the operator """
		if event.type in self.cancel_keys or self.kill:
			RemoveCursurOveride(self.draw_handler)
			self.kill = False
			if self.step > 0:
				self.subclass.abort()
			self.reset()
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		self.draw_handler = AddCursurOveride(self)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}