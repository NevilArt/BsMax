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
# 2024/05/19

import bpy

from bmesh import new as bmesh_new
from bgl import glEnable, glDisable, GL_BLEND
from random import random
from mathutils import Vector
from gpu import shader as gshader
from gpu_extras.batch import batch_for_shader
from bpy.types import Operator
from bpy.app import version

from bsmax.actions import link_to_scene, set_as_active_object
from .gride import Gride, Dimension, Click_Point
from bsmax.gride import LocalGride


def set_smooth_by_angel(cls):
	if version < (4, 1, 0):
		cls.data.use_auto_smooth = True
		cls.data.auto_smooth_angle = 0.523599

	elif version >= (4, 1, 0):
		#TODO find a method that work on non selected mode too
		bpy.ops.object.shade_smooth_by_angle()


def set_shading_mode(cls):
	if not cls.data:
		return
	
	if cls.shading == 'FLAT':
		cls.data.shade_flat()

	elif cls.shading == 'SMOOTH':
		cls.data.shade_smooth()
	
	elif cls.shading == 'AUTO':
		set_smooth_by_angel(cls)


def float_vector_to_color(floatVector):
	return (floatVector[0], floatVector[1], floatVector[2], 1)


def primitive_geometry_class_create_mesh(cls, ctx, meshdata, classname):
	verts,edges,faces, = meshdata
	newmesh = bpy.data.meshes.new(classname)
	newmesh.from_pydata(verts, edges, faces)
	newmesh.update(calc_edges=True)
	cls.owner = bpy.data.objects.new(classname, newmesh)
	link_to_scene(ctx, cls.owner)
	set_as_active_object(ctx, cls.owner)
	cls.data = cls.owner.data

	cls.owner.name = ctx.scene.primitive_setting.next_name
	newColor = float_vector_to_color(ctx.scene.primitive_setting.next_color)
	cls.owner.color = newColor


def primitive_geometry_class_update_mesh(cls, meshdata):
	if cls.data and bpy.context.mode == 'OBJECT':
		verts, edges, faces, = meshdata
		""" Genarate New Data """
		orgmesh = bpy.data.meshes[cls.data.name]
		tmpmesh = bpy.data.meshes.new("_NewTempMesh_")
		tmpmesh.from_pydata(verts, edges, faces)
		bm = bmesh_new()
		bm.from_mesh(tmpmesh)
		bm.to_mesh(orgmesh.id_data)
		bm.free()
		bpy.data.meshes.remove(tmpmesh)

		for f in cls.data.polygons:
			f.use_smooth = True


def primitive_curve_class_create_curve(cls, ctx, shapes, classname):
	# Create Spline
	newcurve = bpy.data.curves.new(classname, type='CURVE')
	newcurve.dimensions = '3D'
	curve_from_shapes(newcurve, shapes, cls.close)
	
	# Create object and link to collection
	cls.owner = bpy.data.objects.new(classname, newcurve)
	link_to_scene(ctx, cls.owner)
	set_as_active_object(ctx, cls.owner)
	cls.data = cls.owner.data


def primitive_curve_class_update_curve(cls, shapes):
	if cls.data != None and bpy.context.mode == 'OBJECT':
		curve = bpy.data.curves[cls.data.name]
		curve_from_shapes(curve, shapes, cls.close)


# Create Curve from Splines in the shape Data
def curve_from_shapes(curve, shapes, close):
	""" put BsMax primitive Shape Date in to Blender Curve Data """
	curve.splines.clear()
	
	for shape in shapes:
		count = len(shape)
		newspline = curve.splines.new('BEZIER')
		newspline.bezier_points.add(count - 1)
	
		for i in range(count):
			bez = newspline.bezier_points[i]
			bez.co, bez.handle_left, bez.handle_left_type, bez.handle_right, bez.handle_right_type = shape[i]
	
		newspline.use_cyclic_u = close


# Overide mouse pointer
def GetCursurMesh(size, x, y):
	shape =(
		(0.4, 0.0), (0.6, 0.0), (0.6, 0.4),
		(1.0, 0.4), (1.0, 0.6), (0.6, 0.6),
		(0.6, 1.0), (0.4, 1.0), (0.4, 0.6),
		(0.0, 0.6), (0.0, 0.4), (0.4, 0.4)
	)
	
	verts = []
	offset_x = x - size / 2
	offset_y = y - size / 2
	
	for i in range(len(shape)):
		xpos = shape[i][0] * size + offset_x
		ypos = shape[i][1] * size + offset_y
		verts.append((xpos, ypos))
	
	faces =(
		(0, 1, 11), (1, 2, 11),
		(2, 3, 5), (3, 4, 5),
		(5, 6, 7), (7, 8, 5),
		(8, 9, 11), (11, 9, 10)
	)
	
	return verts, faces


def ClearPrimitiveData(obj):
	if obj:
		obj.primitivedata.classname = ""


def draw_cursur_override(cls):
	if version < (4, 0, 0):
		glEnable(GL_BLEND)
		shader = gshader.from_builtin('UNIFORM_COLOR')
		v, f = GetCursurMesh(20, cls.mpos.x, cls.mpos.y)
		batch = batch_for_shader(shader, 'TRIS', {"pos":v}, indices=f)
		shader.bind()
		shader.uniform_float("color",(0.8, 0.8, 0.8, 0.6))
		batch.draw(shader)
		glDisable(GL_BLEND)

	else:
		shader = gshader.from_builtin('UNIFORM_COLOR')
		v, f = GetCursurMesh(20, cls.mpos.x, cls.mpos.y)
		batch = batch_for_shader(shader, 'TRIS', {"pos":v}, indices=f)
		shader.bind()
		shader.uniform_float("color", (0.8, 0.8, 0.8, 0.6))
		batch.draw(shader)


def add_curcur_override(cls):
	handle = bpy.types.SpaceView3D.draw_handler_add(
		draw_cursur_override, tuple([cls]), 'WINDOW', 'POST_PIXEL'
	)
	return handle


def RemoveCursurOveride(handle):
	bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')


def is_true_class(ctx, classname):
	if ctx.active_object:
		if classname == ctx.active_object.primitivedata.classname:
			return True
	return False


def fix_type_visablity(subclass, ctx):
	owner_type = ''

	if subclass:
		if subclass.owner:
			owner_type = subclass.owner.type

	if owner_type == '':
		return

	elif owner_type == 'MESH':
		ctx.space_data.show_object_viewport_mesh = True

	elif owner_type == 'CURVE':
		ctx.space_data.show_object_viewport_curve = True

	elif owner_type == 'SURFACE':
		ctx.space_data.show_object_viewport_surf = True

	elif owner_type == 'META':
		ctx.space_data.show_object_viewport_meta = True

	elif owner_type == 'FONT':
		ctx.space_data.show_object_viewport_font = True

	elif owner_type == 'VOLUME':
		ctx.space_data.show_object_viewport_volume = True

	elif owner_type == 'GPENCIL':
		ctx.space_data.show_object_viewport_grease_pencil = True

	elif owner_type == 'ARMATURE':
		ctx.space_data.show_object_viewport_armature = True

	elif owner_type == 'LATTICE':
		ctx.space_data.show_object_viewport_lattice = True

	elif owner_type == 'EMPTY':
		ctx.space_data.show_object_viewport_empty = True

	elif owner_type == 'LIGHT':
		ctx.space_data.show_object_viewport_light = True

	elif owner_type == 'LIGHT_PROBE':
		ctx.space_data.show_object_viewport_light_probe = True

	elif owner_type == 'CAMERA':
		ctx.space_data.show_object_viewport_camera = True

	elif owner_type == 'SPEAKER':
		ctx.space_data.show_object_viewport_speaker = True


def set_active_tool(cls, ctx):
	activeToolName = ""
	# 
	if cls.subclass:
		# TODO just temprary solution for quick update
		try:
			# if hasattr(self.subclass, 'name'):
			activeToolName = cls.subclass.classname
		except:
			activeToolName = ""
	else:
		activeToolName = ""

	primitive_setting = ctx.scene.primitive_setting
	primitive_setting.active_tool = activeToolName
	primitive_setting.next_name = activeToolName
	r, g, b = random(), random(), random()
	primitive_setting.next_color = (r, g, b)


def get_alt_ctrl_shift_state(cls, event):
	if event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT'}:
		if event.value == 'PRESS':
			cls.shift = True
		if event.value == 'RELEASE':
			cls.shift = False
	
	if event.type in {'LEFT_CTRL', 'RIGHT_CTRL'}:
		if event.value == 'PRESS':
			cls.ctrl = True
		if event.value == 'RELEASE':
			cls.ctrl = False
	
	if event.type in {'LEFT_ALT', 'RIGHT_ALT'}:
		if event.value == 'PRESS':
			cls.alt = True
		if event.value == 'RELEASE':
			cls.alt = False


def draw_primitive_acceptable(cls):
	""" Check mouse movment make sure do not create tiny invisible object"""
	xabs = abs(cls.mouse_start.x - cls.mouse_curent.x)
	yabs = abs(cls.mouse_start.y - cls.mouse_curent.y)
	length = xabs + yabs
	return length > 8 or (length == 0 and cls.use_single_click)


def draw_primitive_first_click(cls, ctx, x, y):
	""" Get first click and initial basic setups """
	cls.step = 1
	cls.mouse_start = Vector((x, y, 0))
	cls.use_surface = ctx.scene.primitive_setting.draw_mode == 'SURFACE'

	""" Create local Gride """
	cls.gride.get_coordinate(ctx, x, y)

	##########################
	# just a prototype #
	cls.localGride.matrix = cls.gride.gride_matrix
	cls.localGride.set(2, 15, None)
	cls.localGride.genarate_gride_lines()
	cls.localGride.register(ctx)
	##########################

	""" Get First Click Point """
	cls.point_current.location = cls.gride.location.copy()
	cls.point_start.location = cls.point_current.location.copy()

	""" Triger Draw mode for object """
	cls.subclass.on_draw = True

	cls.create(ctx)


def draw_primitive_click_count(cls, event, x, y):
	""" Count clicks and check movment (Draged or not) """
	if event.value == 'PRESS':
		cls.state = True
	
	if event.value =='RELEASE':
		cls.state = cls.drag = False
		cls.step += 1
		cls.curent = Vector((x, y, 0))
		cls.point_start.location = cls.point_current.location.copy()


def draw_primitive_reset(cls, ctx):
	cls.subclass.reset()
	cls.gride.reset()
	cls.point_start.reset()
	cls.point_current.reset()
	cls.step = 0
	cls.localGride.unregister()
	set_active_tool(cls, ctx)


def draw_primitive_jump_to_end(cls):
	cls.use_single_draw = False
	cls.step = cls.subclass.finishon


def draw_primitive_finish_it(cls, ctx):
	""" Delete accidently drawed very tiny objects """
	if draw_primitive_acceptable(cls):
		cls.finish()
		cls.subclass.finish()
		bpy.ops.ed.undo_push()
	else:
		cls.subclass.abort()

	draw_primitive_reset(cls, ctx)
	cls.localGride.unregister()


def draw_primitive_use_gride(cls, ctx, x, y):
	cls.point_current.location = cls.gride.get_click_point_gride(ctx, x, y)


def draw_primitive_use_surface(cls, ctx, x, y):
	cls.point_current.location = cls.gride.get_click_point_surface(ctx, x, y)
	cls.localGride.matrix = cls.gride.gride_matrix
	cls.localGride.genarate_gride_lines()


class Primitive_Public_Class:
	def __init__(self):
		self.init()
	
	def init(self):
		pass

	def reset(self):
		self.__init__()

	def update(self):
		pass

	def abort(self):
		bpy.ops.object.delete(confirm=False)
	
	def finish(self):
		pass


class Primitive_Geometry_Class:
	def __init__(self):
		self.classname = ""
		self.finishon = 0
		self.owner = None
		self.data = None
		self.ready = False
		self.shading = 'FLAT'# 'SMOOTH', 'AUTO'
		self.init()
	
	def reset(self):
		self.__init__()

	def create_mesh(self, ctx, meshdata, classname):
		primitive_geometry_class_create_mesh(self, ctx, meshdata, classname)
		set_shading_mode(self)

	def update_mesh(self, meshdata):
		primitive_geometry_class_update_mesh(self, meshdata)
		set_shading_mode(self)
	
	def update(self):
		pass

	def abort(self):
		bpy.ops.object.delete(confirm=False)
	
	def finish(self):
		self.ready = True


class Primitive_Curve_Class:
	def __init__(self):
		self.classname = ""
		self.finishon = 0
		self.owner = None
		self.data = None
		self.ready = False
		self.close = False
		self.init()
	
	def reset(self):
		self.__init__()

	def create_curve(self, ctx, shapes, classname):
		primitive_curve_class_create_curve(self, ctx, shapes, classname)

	def update_curve(self, shapes):
		primitive_curve_class_update_curve(self, shapes)
	
	def update(self):
		pass

	def abort(self):
		bpy.ops.object.delete(confirm=False)

	def finish(self):
		self.ready = True


class Draw_Primitive(Operator):
	bl_options = {'REGISTER','UNDO'}
	subclass = None # Subclass is Primitive object type
	params = None # object.data.primitivedata
	step = 0 # click push/release count
	mouse_start = Vector((0, 0, 0)) # first position of click point
	mouse_curent = Vector((0, 0, 0)) # current position of click point
	used_keys = ['LEFTMOUSE', 'RIGHTMOUSE', 'ESC', 'MOUSEMOVE', 'Z'] # list of needed keys
	cancel_keys = ['RIGHTMOUSE', 'ESC'] # keys for cancel opration
	request_key = [] # Reserved for specila operators that needs more keys
	state = False # State (LMB is down)
	drag = False # Draging wile LMB is down
	kill = False # Cancel Every Thing
	shift, ctrl, alt = False, False, False # Flag
	gride = Gride() # Click point info
	localGride = LocalGride()
	point_start = Click_Point() # 3D coordinate and info of start click point
	point_current = Click_Point() # 3D coordinate and info of current click point
	use_gride = False
	use_surface = False
	use_single_click = False
	use_single_draw = False
	changed = False
	draw_handler = None # Mouse override graphic handler
	mpos = Vector((0, 0, 0)) #TODO need to replace
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
	def jump_to_end(self):
		draw_primitive_jump_to_end(self)
	
	def check_event(self, key, action):
		pass

	def finish(self):
		pass

	def modal(self, ctx, event):
		ctx.area.tag_redraw()

		get_alt_ctrl_shift_state(self, event)

		if not self.subclass:
			return {'CANCELLED'}
		
		if not event.type in self.used_keys:
			return {'PASS_THROUGH'}

		""" Get mouse screen position """
		x, y = event.mouse_region_x, event.mouse_region_y
		self.mpos = Vector((x, y, 0))
		
		""" Call Event function """
		self.check_event(event.type, event.value)
		
		""" Detect First click """
		if event.type == 'LEFTMOUSE':
			if self.step == 0:
				draw_primitive_first_click(self, ctx, x, y)
				fix_type_visablity(self.subclass, ctx)
				
			draw_primitive_click_count(self, event, x, y)

		""" Check and update any movment """
		if event.type == 'MOUSEMOVE' or self.changed:
			if self.state:
				self.drag = True
					
			if self.step > 0:
				""" Set true if used in first drag only """
				if self.step == 1:
					self.use_single_draw = self.ctrl
				
				""" Get mouse click point virtual gride"""
				self.mouse_curent = Vector((x, y, 0))
				
				if self.use_gride:# high priority
					draw_primitive_use_gride(self, ctx, x, y)
				elif self.use_surface:# seconf priority
					draw_primitive_use_surface(self, ctx, x, y)
				else:# the only avalible option
					draw_primitive_use_gride(self, ctx, x, y)
				
				dimension = Dimension(
					self.gride,
					self.point_start.location,
					self.point_current.location
				)

				self.update(ctx, self.step, dimension)

				""" Updat Data object """
				self.subclass.update()

			""" finish or cancel operatoin by click count """
			if self.subclass.finishon > 0:
				if self.step >= self.subclass.finishon:
					draw_primitive_finish_it(self, ctx)
			else:
				if self.step == -1:
					draw_primitive_finish_it(self, ctx)

		""" abort if pointer go out of screen """
		# if self.step == 0 and out of screen:
		# 	self.kill = True

		""" finish and drop the operator """
		if event.type in self.cancel_keys or self.kill:
			RemoveCursurOveride(self.draw_handler)
			self.kill = False

			if self.step > 0:
				self.subclass.abort()

			draw_primitive_reset(self, ctx)
			ctx.scene.primitive_setting.active_tool = ""
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		set_active_tool(self, ctx)
		self.draw_handler = add_curcur_override(self)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}