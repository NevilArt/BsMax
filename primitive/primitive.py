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

import bpy, bmesh, bgl, gpu
from bpy.types import Operator
from mathutils import Vector
from math import sqrt
from gpu_extras.batch import batch_for_shader
from bsmax.state import is_object_mode
from bsmax.actions import link_to_scene,set_as_active_object,set_create_target,delete_objects
from bsmax.mouse import get_click_point_info, ClickPoint
from bsmax.math import get_2_point_center

class Dimantion:
	width = 0
	length = 0
	height = 0
	radius = 0
	center = Vector((0,0,0))
	orient = Vector((0,0,0))
	view = Vector((0,0,0))
	local = Vector((0, 0, 0))
	view_name = ""

	height_np = 0

	width_from_start_point = 0
	length_from_start_point = 0
	height_from_start_point = 0
	radius_from_start_point = 0

	def from_click_points(self, cpa, cpb, cpo):
		w = self.width = abs(cpa.local.x - cpb.local.x)
		l = self.length = abs(cpa.local.y - cpb.local.y)
		if cpo.view_name == 'TOP':
			height = cpb.screen.y - cpa.screen.y
		elif cpo.view_name == 'BOTTOM':
			height = cpa.screen.y - cpb.screen.y
		else:
			height = cpb.screen.z - cpa.screen.z
		self.height_np = height
		self.height = height if height > 0 else 0
		self.radius = sqrt(w * w + l * l)
		self.orient = cpa.orient
		self.center = get_2_point_center(cpa.view, cpb.view)
		self.view = cpb.view
		self.local = cpb.view
		wo = abs(cpo.local.x - cpb.local.x)
		lo = abs(cpo.local.y - cpb.local.y)
		self.radius_from_start_point = sqrt(wo * wo + lo * lo)
		self.view_name = cpo.view_name

class CreatePrimitive(Operator):
	bl_options = {'REGISTER','UNDO'}
	#bpy.ops.ed.undo_push() TODO use this for undo step by step
	subclass = None
	params = None
	step = 0
	cpoint_a = ClickPoint()
	cpoint_b = ClickPoint()
	state = False
	drag = False
	mpos = Vector((0, 0, 0))
	usedkeys = ['LEFTMOUSE', 'RIGHTMOUSE', 'ESC', 'MOUSEMOVE']
	cancelkeys = ['RIGHTMOUSE', 'ESC']
	requestkey = []
	forcefinish = False
	shift = False
	ctrl = False
	alt = False

	@classmethod
	def poll(self, ctx):
		return is_object_mode(ctx)

	def modal(self, ctx, event):
		ctx.area.tag_redraw()

		if event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT'}:
			if event.value == 'PRESS':
				self.shift = True
			if event.value == 'RELEASE':
				self.shift = False

		if self.subclass == None:
			return {'CANCELLED'}
		elif not event.type in self.usedkeys: 
			return {'PASS_THROUGH'}
		else:
			dimantion = Dimantion()
			x, y = event.mouse_region_x, event.mouse_region_y
			self.mpos = Vector((x, y, 0))
			self.cpoint_b = get_click_point_info(x, y, ctx)

			if event.type == 'LEFTMOUSE':
				if self.step == 0:
					self.step = 1
					self.cpoint_o = self.cpoint_a = self.cpoint_b
					self.create(ctx, self.cpoint_a)
					if ctx.space_data.local_view:
						self.subclass.owner.local_view_set(ctx.space_data, True)
				if event.value == 'PRESS':
					self.state = True
				if event.value =='RELEASE':
					self.state = self.drag = False
					self.step += 1
					self.cpoint_a = self.cpoint_b

			if event.type in self.requestkey:
				self.event(event.type, event.value)
				dimantion.from_click_points(self.cpoint_a, self.cpoint_b, self.cpoint_o)	
				self.update(ctx, self.step, dimantion)

			if event.type == 'MOUSEMOVE':
				if self.state:
					self.drag = True
				if self.step > 0:
					dimantion.from_click_points(self.cpoint_a, self.cpoint_b, self.cpoint_o)
					self.update(ctx, self.step, dimantion)
				if self.subclass.finishon > 0:
					if self.step >= self.subclass.finishon:
						self.step = 0
						self.finish()
						self.subclass.reset()

			if event.type in self.cancelkeys or self.forcefinish:
				self.forcefinish = False
				RemoveCursurOveride(self.drawhandler)
				if self.step > 0:
					self.subclass.abort()
				self.subclass.reset()
				return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		self.drawhandler = AddCursurOveride(self)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class PrimitiveGeometryClass:
	def create_mesh(self, ctx, meshdata, classname):
		verts,edges,faces, = meshdata
		newmesh = bpy.data.meshes.new(classname)
		newmesh.from_pydata(verts,edges,faces)
		newmesh.update(calc_edges=True)
		self.owner = bpy.data.objects.new(classname,newmesh)
		link_to_scene(ctx, self.owner)
		set_as_active_object(ctx,self.owner)
		self.data = self.owner.data
	def update_mesh(self, meshdata):
		if self.data != None and bpy.context.mode == 'OBJECT':
			verts,edges,faces, = meshdata
			# if bpy.app.version[1] == 80:
			if True:
				""" old method for V2.80 """
				orgmesh = bpy.data.meshes[self.data.name]
				tmpmesh = bpy.data.meshes.new("_NewTempMesh_")
				tmpmesh.from_pydata(verts,edges,faces)
				bm = bmesh.new()
				bm.from_mesh(tmpmesh)
				bm.to_mesh(orgmesh.id_data)
				bm.free()
				bpy.data.meshes.remove(tmpmesh)
			else:
				""" new method for V2.81 and above """
				self.data.clear_geometry()
				self.data.from_pydata(verts,edges,faces)
				""" Note this method is faster but clear the keyframes too """
				""" Ihad to skip this part till I find a solution for this """

class PrimitiveCurveClass:
	def create_curve(self, ctx, shapes, classname):
		# Create Spline
		newcurve = bpy.data.curves.new(classname, type='CURVE')
		newcurve.dimensions = '3D'
		CurveFromShapes(newcurve, shapes, self.close)
		# Create object and link to collection
		self.owner = bpy.data.objects.new(classname, newcurve)
		link_to_scene(ctx, self.owner)
		set_as_active_object(ctx, self.owner)
		self.data = self.owner.data
	def update_curve(self, shapes):
		if self.data != None and bpy.context.mode == 'OBJECT':
			curve = bpy.data.curves[self.data.name]
			CurveFromShapes(curve, shapes, self.close)

# Create Curve from Splines in the shape Data
def CurveFromShapes(Curve, Shapes, Close):
	Curve.splines.clear()
	for Shape in Shapes:
		newspline = Curve.splines.new('BEZIER')
		newspline.bezier_points.add(len(Shape) - 1)
		for i in range(len(Shape)):
			bez = newspline.bezier_points[i]
			bez.co, bez.handle_left, bez.handle_left_type, bez.handle_right, bez.handle_right_type = Shape[i]
		newspline.use_cyclic_u = Close

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
	v,f = GetCursurMesh(20,self.mpos.x, self.mpos.y)
	batch = batch_for_shader(shader,'TRIS',{"pos":v},indices=f)
	shader.bind()
	shader.uniform_float("color",(0.8,0.8,0.8,0.6))
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