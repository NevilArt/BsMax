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
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty
from math import radians

# TODO
# fix coordinate system
# add randomize option

def BsMax_Clone_Reset(self, ctx):
	for N in self.NewNds:
		for O in N:
			bpy.data.objects.remove(O, do_unlink = True)
	self.NewNds = []

def BsMax_Clone_Create(self, ctx):
	self.NewNds = []
	bpy.ops.object.select_all(action = 'DESELECT')
	for p in self.parents:
		p.select_set(True)
	for i in range(self.count):
		bpy.ops.object.duplicate(linked = self.makeinstance, mode = 'INIT')
		Nodes = []
		for O in ctx.selected_objects:
			Nodes.append(O)
		self.NewNds.append(Nodes)
	for p in self.parents:
		p.select_set(True)

def BsMax_Clone_SetTransform(self, ctx):
	px, py, pz = [], [], []
	rx, ry, rz = [], [], []
	sx, sy, sz = [], [], []
	for p in self.parents:
		px.append(p.location.x)
		py.append(p.location.y)
		pz.append(p.location.z)
		rx.append(p.rotation_euler[0])
		ry.append(p.rotation_euler[1])
		rz.append(p.rotation_euler[2])
		sx.append(p.scale.x)
		sy.append(p.scale.y)
		sz.append(p.scale.z)

	offset_scale,rotate_scale,scale_scale = 1.0,1.0,1.0
	if self.offset_abs:
		offset_scale = 1.0/self.count
	if self.rotate_abs:
		rotate_scale = 1.0/self.count
	if self.scale_abs:
		scale_scale = 1.0/self.count

	for i in range(len(self.NewNds)):
		N = self.NewNds[i]
		for j in range(len(N)):
			# TODO calculate position depend on coorsys
			# Set Postion
			N[j].location.x = px[j]+self.offset_x*offset_scale*(i+1)
			N[j].location.y = py[j]+self.offset_y*offset_scale*(i+1)
			N[j].location.z = pz[j]+self.offset_z*offset_scale*(i+1)

			# TODO set rotation depend on coorsys
			# Set Rotaton
			N[j].rotation_euler[0] = rx[j]+radians(self.rotate_x*(i+1)*rotate_scale)
			N[j].rotation_euler[1] = ry[j]+radians(self.rotate_y*(i+1)*rotate_scale)
			N[j].rotation_euler[2] = rz[j]+radians(self.rotate_z*(i+1)*rotate_scale)

			# Set Scale
			N[j].scale.x = sx[j]+(self.scale_x/100.0 - 1)*(i+1)*scale_scale
			N[j].scale.y = sy[j]+(self.scale_y/100.0 - 1)*(i+1)*scale_scale
			N[j].scale.z = sz[j]+(self.scale_z/100.0 - 1)*(i+1)*scale_scale

			# Set Mirror
			if self.mirror_x and i % 2 == 0:
				N[j].scale.x = -N[j].scale.x
			if self.mirror_y and i % 2 == 0:
				N[j].scale.y = -N[j].scale.y
			if self.mirror_z and i % 2 == 0:
				N[j].scale.z = -N[j].scale.z

class Object_OT_Clone_Array(bpy.types.Operator):
	bl_idname = "object.clone"
	bl_label = "Clone / Array"
	bl_description = "Clone object dialog box"
	bl_options = {'REGISTER', 'UNDO'}

	new_name: StringProperty(default="Default")
	makeinstance: BoolProperty(default=True)
	mirror_x: BoolProperty()
	mirror_y: BoolProperty()
	mirror_z: BoolProperty()
	offset_x: FloatProperty()
	offset_y: FloatProperty()
	offset_z: FloatProperty()
	offset_abs: BoolProperty()
	rotate_x: FloatProperty()
	rotate_y: FloatProperty()
	rotate_z: FloatProperty()
	rotate_abs: BoolProperty()
	scale_x: FloatProperty(default=100)
	scale_y: FloatProperty(default=100)
	scale_z: FloatProperty(default=100)
	scale_abs: BoolProperty()
	count: IntProperty(default=1,min=1,max=99999999)
	num = 0 # keep old value for check has update or not
	parents,NewNds = [],[]

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False
	
	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		row = box.row()
		row.prop(self,"new_name",text="Name")
		row = box.row()
		row.prop(self,"makeinstance",text="Instance")
		box = layout.box()
		row = box.row()
		row.label(text="Mirror")
		row.prop(self,"mirror_x",text="X")
		row.prop(self,"mirror_y",text="Y")
		row.prop(self,"mirror_z",text="Z")
		box = layout.box()
		row = box.row(align=True)
		row.label(text="Move")
		row.prop(self,"offset_x",text="X")
		row.prop(self,"offset_y",text="Y")
		row.prop(self,"offset_z",text="Z")
		row.prop(self,"offset_abs",text="")
		row = box.row(align=True)
		row.label(text="Rotate")
		row.prop(self,"rotate_x",text="X")
		row.prop(self,"rotate_y",text="Y")
		row.prop(self,"rotate_z",text="Z")
		row.prop(self,"rotate_abs",text="")
		row = box.row(align=True)
		row.label(text="Scale")
		row.prop(self,"scale_x",text="X")
		row.prop(self,"scale_y",text="Y")
		row.prop(self,"scale_z",text="Z")
		row.prop(self,"scale_abs",text="")
		box = layout.box()
		row = box.row()
		row.label(text="Count")
		row.prop(self,"count")
	
	def check(self, ctx):
		if self.count != self.num:
			BsMax_Clone_Reset(self, ctx)
			BsMax_Clone_Create(self, ctx)
			self.num = self.count
		BsMax_Clone_SetTransform(self, ctx)

	def execute(self, ctx):
		self.report({'OPERATOR'},'bpy.ops.object.clone()')
		return {'FINISHED'}

	def cancel(self, ctx):
		BsMax_Clone_Reset(self, ctx)

	def invoke(self, ctx, evt):
		if ctx.active_object != None:
			self.new_name = ctx.active_object.name
		self.parents = ctx.selected_objects
		ctx.window_manager.invoke_props_dialog(self)
		return {'RUNNING_MODAL'}

def object_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.clone")

def register_cloneobject():
	bpy.utils.register_class(Object_OT_Clone_Array)
	bpy.types.VIEW3D_MT_object.append(object_menu)

def unregister_cloneobject():
	bpy.types.VIEW3D_MT_object.remove(object_menu)
	bpy.utils.unregister_class(Object_OT_Clone_Array)