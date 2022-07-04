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
import bmesh
import bgl
import gpu

from gpu_extras.batch import batch_for_shader
from bpy.types import Operator
from mathutils import Vector

from bsmax.actions import link_to_scene, set_as_active_object
from .gride import Gride, Dimension, Click_Point
from bsmax.gride import Local_Gride



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
		pass
	
	def finish(self):
		pass



class Primitive_Geometry_Class:
	def __init__(self):
		self.classname = ""
		self.finishon = 0
		self.owner = None
		self.data = None
		self.ready = False
		self.init()
	
	def reset(self):
		self.__init__()

	def create_mesh(self, ctx, meshdata, classname):
		verts,edges,faces, = meshdata
		newmesh = bpy.data.meshes.new(classname)
		newmesh.from_pydata(verts,edges, faces)
		newmesh.update(calc_edges=True)
		self.owner = bpy.data.objects.new(classname, newmesh)
		link_to_scene(ctx, self.owner)
		set_as_active_object(ctx, self.owner)
		self.data = self.owner.data
		self.data.use_auto_smooth = True

	def update_mesh(self, meshdata):
		if self.data != None and bpy.context.mode == 'OBJECT':
			verts,edges,faces, = meshdata
			""" Genarate New Data """
			orgmesh = bpy.data.meshes[self.data.name]
			tmpmesh = bpy.data.meshes.new("_NewTempMesh_")
			tmpmesh.from_pydata(verts, edges, faces)
			bm = bmesh.new()
			bm.from_mesh(tmpmesh)
			bm.to_mesh(orgmesh.id_data)
			bm.free()
			bpy.data.meshes.remove(tmpmesh)
			for f in self.data.polygons:
				f.use_smooth = True
	
	def update(self):
		pass

	def abort(self):
		pass
	
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
		# Create Spline
		newcurve = bpy.data.curves.new(classname, type='CURVE')
		newcurve.dimensions = '3D'
		curve_from_shapes(newcurve, shapes, self.close)
		# Create object and link to collection
		self.owner = bpy.data.objects.new(classname, newcurve)
		link_to_scene(ctx, self.owner)
		set_as_active_object(ctx, self.owner)
		self.data = self.owner.data

	def update_curve(self, shapes):
		if self.data != None and bpy.context.mode == 'OBJECT':
			curve = bpy.data.curves[self.data.name]
			curve_from_shapes(curve, shapes, self.close)
	
	def update(self):
		pass

	def abort(self):
		pass

	def finish(self):
		self.ready = True



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



def ClearPrimitiveData(obj):
	if obj != None:
		obj.primitivedata.classname = ""



# Overide mouse pointer
def GetCursurMesh(size, x, y):
	shape =((0.4, 0.0), (0.6, 0.0), (0.6, 0.4),
			(1.0, 0.4), (1.0, 0.6), (0.6, 0.6),
			(0.6, 1.0), (0.4, 1.0), (0.4, 0.6),
			(0.0, 0.6), (0.0, 0.4), (0.4, 0.4))
	verts = []
	offset_x = x - size / 2
	offset_y = y - size / 2
	for i in range(len(shape)):
		xpos = shape[i][0] * size + offset_x
		ypos = shape[i][1] * size + offset_y
		verts.append((xpos, ypos))
	faces =((0, 1, 11), (1, 2, 11),
			(2, 3, 5), (3, 4, 5),
			(5, 6, 7), (7, 8, 5),
			(8, 9, 11), (11, 9, 10))
	return verts, faces



def DrawCursurOveride(self):
	bgl.glEnable(bgl.GL_BLEND)
	shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
	v,f = GetCursurMesh(20, self.mpos.x, self.mpos.y)
	batch = batch_for_shader(shader, 'TRIS', {"pos":v}, indices=f)
	shader.bind()
	shader.uniform_float("color",(0.8, 0.8, 0.8, 0.6))
	batch.draw(shader)
	bgl.glDisable(bgl.GL_BLEND)



def AddCursurOveride(self):
	SV3D = bpy.types.SpaceView3D
	handle = SV3D.draw_handler_add(DrawCursurOveride, tuple([self]), 
						'WINDOW', 'POST_PIXEL')
	return handle



def RemoveCursurOveride(handle):
	bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')



def is_true_class(ctx, classname):
	if ctx.active_object != None:
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
	local_gride = Local_Gride()
	""" 3D coordinate and info of click points """
	point_start, point_current = Click_Point(), Click_Point()
	""" flag that choos click point type use gride or not """
	use_gride = False
	use_surface = False
	use_single_click = False
	use_single_draw = False
	changed = False
	""" mouse override graphic handler """
	draw_handler = None
	# need to replace
	mpos = Vector((0, 0, 0))
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
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
		self.mouse_start = Vector((x, y, 0))
		self.use_surface = ctx.scene.primitive_setting.draw_mode == 'SURFACE'

		""" Create local Gride """
		self.gride.get_coordinate(ctx, x, y)

		##########################
		# just a prototype #
		self.local_gride.matrix = self.gride.gride_matrix
		self.local_gride.set(2, 15, None)
		self.local_gride.genarate_gride_lines()
		self.local_gride.register(ctx)
		##########################

		""" Get First Click Point """
		self.point_current.location = self.gride.location.copy()
		self.point_start.location = self.point_current.location.copy()

		""" Triger Draw mode for object """
		self.subclass.on_draw = True

		self.create(ctx)
		
	def click_count(self, event, x, y):
		""" Count clicks and check movment (Draged or not) """
		if event.value == 'PRESS':
			self.state = True
		
		if event.value =='RELEASE':
			self.state = self.drag = False
			self.step += 1
			self.curent = Vector((x, y, 0))
			self.point_start.location = self.point_current.location.copy()
	
	def reset(self):
		self.subclass.reset()
		self.gride.reset()
		self.point_start.reset()
		self.point_current.reset()
		self.step = 0
		self.local_gride.unregister()
	
	def jump_to_end(self):
		self.use_single_draw = False
		self.step = self.subclass.finishon
	
	def finish_it(self):
		""" Delete accidently drawed very tiny objects """
		if self.acceptable():
			self.finish()
			self.subclass.finish()
			bpy.ops.ed.undo_push()
		else:
			self.subclass.abort()
		self.reset()
		self.local_gride.unregister()
	
	def check_event(self, key, action):
		pass
	
	def finish(self):
		pass

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
		self.mpos = Vector((x, y, 0))
		
		""" Call Event function """
		self.check_event(event.type, event.value)
		
		""" Detect First click """
		if event.type == 'LEFTMOUSE':
			if self.step == 0:
				self.first_click(ctx, x, y)
				fix_type_visablity(self.subclass, ctx)
				
			self.click_count(event, x, y)

		""" Check and update any movment """
		if event.type == 'MOUSEMOVE' or self.changed:
			if self.state:
				self.drag = True
					
			if self.step > 0:
				""" Set true if used in first drag only """
				if self.step == 1:
					self.use_single_draw = self.ctrl
				
				""" Get mouse click point virtual gride"""
				self.mouse_curent = Vector((x,y,0))
				
				if self.use_gride:
					self.point_current.location = self.gride.get_click_point_gride(ctx, x, y)
				elif self.use_surface:
					self.point_current.location = self.gride.get_click_point_surface(ctx, x, y)
					################
					self.local_gride.matrix = self.gride.gride_matrix
					self.local_gride.genarate_gride_lines()
					################
				else:
					self.point_current.location = self.gride.get_click_point_gride(ctx, x, y)
				
				dimension = Dimension(self.gride, self.point_start.location, self.point_current.location)
				self.update(ctx, self.step, dimension)

				""" Updat Data object """
				self.subclass.update()

			""" finish or cancel operatoin by click count """
			if self.subclass.finishon > 0:
				if self.step >= self.subclass.finishon:
					self.finish_it()
			else:
				if self.step == -1:
					self.finish_it()
				
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