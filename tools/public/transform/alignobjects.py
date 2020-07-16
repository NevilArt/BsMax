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
from bpy.props import EnumProperty, BoolProperty
from mathutils import Vector, Matrix
from bpy.types import Operator
from bsmax.graphic import register_line,unregister_line,get_screen_pos

# Original Code by Ozzkar
# Edit by Nevil

def get_pos_data(obj):
	cld = []
	msh = obj.data
	if obj.type == 'MESH' and len(msh.vertices) > 0:
		cld = [obj.matrix_world @ vert.co for vert in msh.vertices]
	elif obj.type == 'CURVE' and len(msh.splines) > 0:
		for spn in msh.splines:
			cld += [obj.matrix_world @ pts.co for pts in spn.bezier_points]
	elif obj.type == 'SURFACE' and len(msh.splines) > 0:
		for spn in msh.splines:
			cld += [obj.matrix_world @ pts.co for pts in spn.points]
	elif obj.type == 'FONT' and len(msh.splines) > 0:
		for spn in msh.splines:
			cld += [obj.matrix_world @ pts.co for pts in spn.bezier_points]
	# get min/max/center/pivot data
	if len(cld) == 0 or obj.type not in {'MESH', 'CURVE', 'SURFACE', 'FONT'}:
		return obj.location.copy(), obj.location.copy(), obj.location.copy(), obj.location.copy()
	p_min = cld[0].copy()
	p_max = cld[0].copy()
	for v in cld:
		if p_min.x > v.x:
			p_min.x = v.x
		if p_min.y > v.y:
			p_min.y = v.y
		if p_min.z > v.z:
			p_min.z = v.z
		if p_max.x < v.x:
			p_max.x = v.x
		if p_max.y < v.y:
			p_max.y = v.y
		if p_max.z < v.z:
			p_max.z = v.z
	return p_min, (p_min+p_max)/2, obj.location.copy(), p_max

def store_form_data(self, ctx):
	self.pos_curs = ctx.scene.cursor.location.copy()
	self.rot_curs = ctx.scene.cursor.rotation_euler.copy()

	for obj in ctx.selected_objects:
		p_min,p_mid,p_piv,p_max = get_pos_data(obj)
		self.pos_list.append([p_min,p_mid,p_piv,p_max])
		self.rot_list.append(obj.rotation_euler.copy())
		self.scl_list.append(obj.scale.copy())

def align_object_execute(self, ctx):
	a_box = get_pos_data(ctx.active_object)
	a_rot = ctx.active_object.rotation_euler
	a_scl = ctx.active_object.scale

	# set modes
	c_id, t_id = 0, 0
	if self.c_mode == 'MID':
		c_id = 1
	if self.c_mode == 'PIV':
		c_id = 2
	if self.c_mode == 'MAX':
		c_id = 3
	if self.t_mode == 'MID':
		t_id = 1
	if self.t_mode == 'PIV':
		t_id = 2
	if self.t_mode == 'MAX':
		t_id = 3

	# check cursor to cursor
	if self.c_mode == '3DC' and self.t_mode == '3DC':
		return

	# check active object agains itself
	if len(ctx.selected_objects) == 1 and self.c_mode != '3DC' and self.t_mode != '3DC':
		return

	# set 3D cursor
	if self.c_mode == '3DC':
		# Position
		cursor = ctx.scene.cursor
		if self.pos_x:
			cursor.location[0] = a_box[t_id].x
		if self.pos_y:
			cursor.location[1] = a_box[t_id].y
		if self.pos_z:
			cursor.location[2] = a_box[t_id].z
		# rotation
		if self.rot_x:
			cursor.rotation_euler.x = a_rot.x
		if self.rot_y:
			cursor.rotation_euler.y = a_rot.y
		if self.rot_z:
			cursor.rotation_euler.z = a_rot.z
		return

	if self.t_mode == '3DC':
		scp = ctx.scene.cursor.location.copy()
		for i, obj in enumerate(ctx.selected_objects):
			# Position
			pos_list = self.pos_list
			if self.pos_x:
				obj.location.x = scp.x+(pos_list[i][2].x-pos_list[i][c_id].x)
			if self.pos_y:
				obj.location.y = scp.y+(pos_list[i][2].y-pos_list[i][c_id].y)
			if self.pos_z:
				obj.location.z = scp.z+(pos_list[i][2].z-pos_list[i][c_id].z)
			# Rotation
			if self.rot_x:
				obj.rotation_euler.x = self.rot_curs[0]
			if self.rot_y:
				obj.rotation_euler.y = self.rot_curs[1]
			if self.rot_z:
				obj.rotation_euler.z = self.rot_curs[2]
		return

	# set selection
	for i, obj in enumerate(ctx.selected_objects):
		if obj != ctx.active_object:
			# position
			pos_list = self.pos_list
			if self.pos_x:
				obj.location.x = a_box[t_id].x+(pos_list[i][2].x-pos_list[i][c_id].x)
			if self.pos_y:
				obj.location.y = a_box[t_id].y+(pos_list[i][2].y-pos_list[i][c_id].y)
			if self.pos_z:
				obj.location.z = a_box[t_id].z+(pos_list[i][2].z-pos_list[i][c_id].z)
			# rotation
			if self.rot_x:
				obj.rotation_euler.x = a_rot.x
			if self.rot_y:
				obj.rotation_euler.y = a_rot.y
			if self.rot_z:
				obj.rotation_euler.z = a_rot.z
			# scale
			if self.scl_x:
				obj.scale.x = a_scl.x
			if self.scl_y:
				obj.scale.y = a_scl.y
			if self.scl_z:
				obj.scale.z = a_scl.z

def align_reset(self, ctx):
	cursor,pos_curs,rot_curs = ctx.scene.cursor,self.pos_curs,self.rot_curs
	cursor.location = pos_curs.x,pos_curs.y,pos_curs.z
	cursor.rotation_euler = rot_curs.x,rot_curs.y,rot_curs.z

	for i, obj in enumerate(ctx.selected_objects):
		# position
		obj.location.x = self.pos_list[i][2].x
		obj.location.y = self.pos_list[i][2].y
		obj.location.z = self.pos_list[i][2].z
		# rotation
		obj.rotation_euler.x = self.rot_list[i].x
		obj.rotation_euler.y = self.rot_list[i].y
		obj.rotation_euler.z = self.rot_list[i].z
		# scale
		obj.scale.x = self.scl_list[i].x
		obj.scale.y = self.scl_list[i].y
		obj.scale.z = self.scl_list[i].z

class Align_object_Data:
	def __init__(self):
		self.px = False
		self.py = False
		self.pz = False
		self.rx = False
		self.ry = False
		self.rz = False
		self.sx = False
		self.sy = False
		self.sz = False
		self.cm = 'MIN'
		self.tm = 'MIN'
abd = Align_object_Data()

class Object_OT_Align_Selected_to_Active(Operator):
	bl_idname = "object.align_selected_to_active"
	bl_label = "Align Selected to Active object"
	bl_options = {'REGISTER','UNDO'}

	pos_curs,rot_curs = Vector((0,0,0)),Vector((0,0,0))
	pos_list,rot_list,scl_list = [],[],[]
	items = [('MIN','Minimum','Minimum'),('MID','Center','Center'),
			('PIV','Pivot','Pivot'),('MAX','Maximum','Maximum'),
			('3DC','3D Cursor','3D Cursor')]
	c_mode: EnumProperty(description='Selection alignment point',default='MIN',items=items)
	t_mode: EnumProperty(description='Target alignment point',default='MIN',items=items)
	pos_x: BoolProperty()
	pos_y: BoolProperty()
	pos_z: BoolProperty()
	rot_x: BoolProperty()
	rot_y: BoolProperty()
	rot_z: BoolProperty()
	scl_x: BoolProperty()
	scl_y: BoolProperty()
	scl_z: BoolProperty()
	
	@classmethod
	def poll(self, ctx):
		return len(ctx.selected_objects) > 0 and ctx.active_object != None

	def check(self, ctx):
		align_reset(self,ctx)
		align_object_execute(self,ctx)
		return True

	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		row = box.row()
		row.label(text = "Align Position (World):")
		row = box.row()
		row.prop(self,"pos_x",text="X Position")
		row.prop(self,"pos_y",text="Y Position")
		row.prop(self,"pos_z",text="Z Position")
		row = box.row()
		row.label(text="Current Object:")
		row.label(text="Taget Object:")
		row = box.row()
		row.prop(self,"c_mode")
		row.prop(self,"t_mode")
		box = layout.box()
		row = box.row()
		row.label(text="Align Orientation (Local):")
		row = box.row()
		row.prop(self,"rot_x",text="X Axis")
		row.prop(self,"rot_y",text="Y Axis")
		row.prop(self,"rot_z",text="Z Axis")
		box = layout.box()
		row = box.row()
		row.label(text="Match Scale:")
		row = box.row()
		row.prop(self,"scl_x",text="X Axis")
		row.prop(self,"scl_y",text="Y Axis")
		row.prop(self,"scl_z",text="Z Axis")

	def store_setting(self):
		abd.cm = self.c_mode
		abd.tm = self.t_mode
		abd.px = self.pos_x
		abd.py = self.pos_y
		abd.pz = self.pos_z
		abd.rx = self.rot_x
		abd.ry = self.rot_y
		abd.rz = self.rot_z
		abd.sx = self.scl_x
		abd.sy = self.scl_y
		abd.sz = self.scl_z
	
	def restore_setting(self):
		self.c_mode = abd.cm
		self.t_mode = abd.tm
		self.pos_x = abd.px
		self.pos_y = abd.py
		self.pos_z = abd.pz
		self.rot_x = abd.rx
		self.rot_y = abd.ry
		self.rot_z = abd.rz
		self.scl_x = abd.sx
		self.scl_y = abd.sy
		self.scl_z = abd.sz

	def execute(self, ctx):
		self.store_setting()
		# self.report({'INFO'},'bpy.ops.object.align_selected_to_active()')
		self.report({'INFO'},'bpy.ops.object.align_selected_to_target()')
		return {'FINISHED'}

	def cancel(self, ctx):
		align_reset(self, ctx)
		return None

	def invoke(self, ctx, event):
		self.restore_setting()
		self.pos_curs,self.rot_curs = Vector((0,0,0)),Vector((0,0,0))
		self.pos_list,self.rot_list,self.scl_list = [],[],[]
		store_form_data(self,ctx)
		align_object_execute(self,ctx)
		return ctx.window_manager.invoke_props_dialog(self)
	
def get_center(objs):
	location = Vector((0,0,0))
	for obj in objs:
		location += obj.matrix_world.translation
	return location / len(objs)

class Object_OT_Align_Selected_to_Target(Operator):
	bl_idname = "object.align_selected_to_target"
	bl_label = "Align Selected Objects"
	bl_options = {'REGISTER', 'UNDO'}

	center = None
	start, end, handle = None, None, None
	selected_objects = []

	@classmethod
	def poll(self, ctx):
		return len(ctx.selected_objects) > 0

	def modal(self, ctx, event):
		ctx.area.tag_redraw()
		if not event.type in {'LEFTMOUSE','RIGHTMOUSE', 'MOUSEMOVE','ESC'}:
			return {'PASS_THROUGH'}
		
		elif event.type == 'MOUSEMOVE':
			self.start = get_screen_pos(ctx,self.center)
			self.end = event.mouse_region_x, event.mouse_region_y

		elif event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				""" remove all selected and active object """
				bpy.ops.object.select_all(action='DESELECT')
				ctx.view_layer.objects.active = None
				
				""" Pick new object as target """
				coord = event.mouse_region_x, event.mouse_region_y
				bpy.ops.view3d.select(extend=False,location=coord)

				""" Ignore selected obects as target """
				if ctx.active_object in self.selected_objects:
					ctx.view_layer.objects.active = None

			if event.value =='RELEASE':

				""" Restore selection """
				for obj in self.selected_objects:
					if obj != ctx.active_object:
						obj.select_set(True)
				
				""" if target selected call the operator """
				if ctx.view_layer.objects.active != None:
					bpy.ops.object.align_selected_to_active('INVOKE_DEFAULT')
					return {'CANCELLED'}

			return {'RUNNING_MODAL'}

		elif event.type in {'RIGHTMOUSE','ESC'}:
			unregister_line(self.handle)
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		""" Store selected objects """
		self.selected_objects = ctx.selected_objects.copy()
		self.center = get_center(self.selected_objects)
		self.start = self.end = event.mouse_region_x, event.mouse_region_y
		self.handle = register_line(ctx, self, '2d', (1, 0.5, 0.5, 1))
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

classes = [Object_OT_Align_Selected_to_Active,Object_OT_Align_Selected_to_Target]

def register_alignobjects():
	[bpy.utils.register_class(c) for c in classes]

def unregister_alignobjects():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_alignobjects()