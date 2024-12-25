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
# 2024/09/09

import bpy

from bpy.types import Operator
from bpy.props import FloatProperty, BoolProperty, EnumProperty
from bpy.utils import register_class, unregister_class


def pos_abs_x(cls, ctx):
	for obj in ctx.selected_objects:
		obj.location[0] = cls.pos_abs_x

def pos_abs_y(cls, ctx):
	for obj in ctx.selected_objects:
		obj.location[1] = cls.pos_abs_y

def pos_abs_z(cls, ctx):
	for obj in ctx.selected_objects:
		obj.location[2] = cls.pos_abs_z


def rot_abs_x(cls, ctx):
	for obj in ctx.selected_objects:
		obj.rotation_euler[0] = cls.rot_abs_x

def rot_abs_y(cls, ctx):
	for obj in ctx.selected_objects:
		obj.rotation_euler[1] = cls.rot_abs_y

def rot_abs_z(cls, ctx):
	for obj in ctx.selected_objects:
		obj.rotation_euler[2] = cls.rot_abs_z


def scl_abs_x(cls, ctx):
	for obj in ctx.selected_objects:
		obj.scale[0] = cls.scl_abs_x / 100.0

def scl_abs_y(cls, ctx):
	for obj in ctx.selected_objects:
		obj.scale[1] = cls.scl_abs_y / 100.0

def scl_abs_z(cls, ctx):
	for obj in ctx.selected_objects:
		obj.scale[2] = cls.scl_abs_z / 100.0

pos, rot, scl = [], [], []



def pos_off_x(cls, ctx):
	if len(ctx.selected_objects) == len(scl):
		for index, obj in enumerate(ctx.selected_objects):
			obj.location[0] = pos[index].x + cls.pos_off_x

def pos_off_y(cls, ctx):
	if len(ctx.selected_objects) == len(scl):
		for index, obj in enumerate(ctx.selected_objects):
			obj.location[1] = pos[index].y + cls.pos_off_y

def pos_off_z(cls, ctx):
	if len(ctx.selected_objects) == len(scl):
		for index, obj in enumerate(ctx.selected_objects):
			obj.location[2] = pos[index].z + cls.pos_off_z


def rot_off_x(cls, ctx):
	if len(ctx.selected_objects) == len(scl):
		for index, obj in enumerate(ctx.selected_objects):
			obj.rotation_euler[0] = rot[index].x + cls.rot_off_x

def rot_off_y(cls, ctx):
	if len(ctx.selected_objects) == len(scl):
		for index, obj in enumerate(ctx.selected_objects):
			obj.rotation_euler[1] = rot[index].y + cls.rot_off_y

def rot_off_z(cls, ctx):
	if len(ctx.selected_objects) == len(scl):
		for index, obj in enumerate(ctx.selected_objects):
			obj.rotation_euler[2] = rot[index].z + cls.rot_off_z


def scl_off_x(cls, ctx):
	if len(ctx.selected_objects) == len(scl):
		for index, obj in enumerate(ctx.selected_objects):
			obj.scale[0] = scl[index].x * cls.scl_off_x/100

def scl_off_y(cls, ctx):
	if len(ctx.selected_objects) == len(scl):
		for index, obj in enumerate(ctx.selected_objects):
			obj.scale[1] = scl[index].y * cls.scl_off_y/100

def scl_off_z(cls, ctx):
	if len(ctx.selected_objects) == len(scl):
		for index, obj in enumerate(ctx.selected_objects):
			obj.scale[2] = scl[index].z * cls.scl_off_z/100


def percent(cls, ctx):
	if len(ctx.selected_objects) == len(scl):
		for index, obj in enumerate(ctx.selected_objects):
			obj.scale[0] = scl[index][0] * cls.percent/100
			obj.scale[1] = scl[index][1] * cls.percent/100
			obj.scale[2] = scl[index][2] * cls.percent/100


def read_objects_values(cls, ctx):
	selection = ctx.selected_objects
	if len(selection) == 1:
		location = selection[0].location
		cls.pos_abs_x = location.x
		cls.pos_abs_y = location.y
		cls.pos_abs_z = location.z

		sre = selection[0].rotation_euler
		cls.rot_abs_x = sre.x
		cls.rot_abs_y = sre.y
		cls.rot_abs_z = sre.z

		scale = selection[0].scale
		cls.scl_abs_x = scale.x * 100
		cls.scl_abs_y = scale.y * 100
		cls.scl_abs_z = scale.z * 100
		cls.percent = 100

	pos.clear()
	rot.clear()
	scl.clear()

	for obj in selection:
		pos.append(obj.location.copy())
		rot.append(obj.rotation_euler.copy())
		scl.append(obj.scale.copy())



class Object_OT_Transform_Type_In(Operator):
	bl_idname = "object.transform_type_in"
	bl_label = "Transform Type-in"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}

	pos_abs_x: FloatProperty(
		name="X", unit='LENGTH', update=pos_abs_x
	) # type: ignore
	
	pos_abs_y: FloatProperty(
		name="Y", unit='LENGTH', update=pos_abs_y
	) # type: ignore
	
	pos_abs_z: FloatProperty(
		name="Z", unit='LENGTH', update=pos_abs_z
	) # type: ignore

	pos_off_x: FloatProperty(
		name="X", unit='LENGTH', update=pos_off_x
	) # type: ignore
	
	pos_off_y: FloatProperty(
		name="Y", unit='LENGTH', update=pos_off_y
	) # type: ignore

	pos_off_z: FloatProperty(
		name="Z", unit='LENGTH', update=pos_off_z
	) # type: ignore

	rot_abs_x: FloatProperty(
		name="X", unit='ROTATION', update=rot_abs_x
	) # type: ignore
	
	rot_abs_y: FloatProperty(
		name="Y", unit='ROTATION', update=rot_abs_y
	) # type: ignore
	
	rot_abs_z: FloatProperty(
		name="Z", unit='ROTATION', update=rot_abs_z
	) # type: ignore

	rot_off_x: FloatProperty(
		name="X", unit='ROTATION', update=rot_off_x
	) # type: ignore
	
	rot_off_y: FloatProperty(
		name="Y", unit='ROTATION', update=rot_off_y
	) # type: ignore
	
	rot_off_z: FloatProperty(
		name="Z", unit='ROTATION', update=rot_off_z
	) # type: ignore

	scl_abs_x: FloatProperty(
		name="X", default=100, update=scl_abs_x
	) # type: ignore
	
	scl_abs_y: FloatProperty(
		name="Y", default=100, update=scl_abs_y
	) # type: ignore
	
	scl_abs_z: FloatProperty(
		name="Z", default=100, update=scl_abs_z
	) # type: ignore

	scl_off_x: FloatProperty(
		name="X", default=100, update=scl_off_x
	) # type: ignore
	
	scl_off_y: FloatProperty(
		name="Y", default=100, update=scl_off_y
	) # type: ignore
	
	scl_off_z: FloatProperty(
		name="Z", default=100, update=scl_off_z
	) # type: ignore

	percent: FloatProperty(
		name="%", default=100, update=percent
	) # type: ignore

	squash: BoolProperty(name="Squash") # type: ignore

	def draw(self, ctx):
		
		tool = ctx.workspace.tools.from_space_view3d_mode(
			ctx.mode,create=False
		).idname

		layout = self.layout
		row = layout.row()
		box = row.box()
		col = box.column(align=True)
		col.label(text="Absolute:")

		if tool == 'builtin.move':
			col.prop(self, 'pos_abs_x')
			col.prop(self, 'pos_abs_y')
			col.prop(self, 'pos_abs_z')

		elif tool == 'builtin.rotate':
			col.prop(self, 'rot_abs_x')
			col.prop(self, 'rot_abs_y')
			col.prop(self, 'rot_abs_z')

		elif tool == 'builtin.scale':
			col.prop(self, 'scl_abs_x')
			col.prop(self, 'scl_abs_y')
			col.prop(self, 'scl_abs_z')
			box.prop(self, 'squash')

		box = row.box()
		col = box.column(align=True)
		col.label(text= 'Offset:')

		if tool == 'builtin.move':
			col.prop(self, 'pos_off_x')
			col.prop(self, 'pos_off_y')
			col.prop(self, 'pos_off_z')

		elif tool == 'builtin.rotate':
			col.prop(self, 'rot_off_x')
			col.prop(self, 'rot_off_y')
			col.prop(self, 'rot_off_z')

		elif tool == 'builtin.scale':
			col.prop(self, 'scl_off_x')
			col.prop(self, 'scl_off_y')
			col.prop(self, 'scl_off_z')
			col.prop(self, 'percent')

		read_objects_values(self, ctx)
		self.pos_off_x, self.pos_off_y, self.pos_off_z = 0, 0, 0
		self.rot_off_x, self.rot_off_y, self.rot_off_z = 0, 0, 0
		self.scl_off_x, self.scl_off_y, self.scl_off_z = 100, 100, 100
		self.percent = 100

	def execute(self, ctx):
		return {'FINISHED'}

	def cancel(self, ctx):
		return None
  
	def invoke(self, ctx, event):
		read_objects_values(self, ctx)
		return ctx.window_manager.invoke_props_dialog(self)



class Object_OT_TTI_Call(Operator):
	bl_idname = "object.tti_call"
	bl_label = "TTI Call"
	bl_description = ""
	switch: EnumProperty(
		items=[
			('none', "None", ""),
			('move', "Move", ""),
			('rotate', "Rotate", ""),
			('scale', "Scale", "")
		],
		default='none'
	) # type: ignore

	def execute(self, ctx):
		if self.switch in {'move', 'rotate', 'scale'}:
			bpy.ops.wm.tool_set_by_id(name='builtin.' + self.switch)
		bpy.ops.object.transform_type_in('INVOKE_DEFAULT')
		return {'FINISHED'}


classes = {
	Object_OT_Transform_Type_In,
	Object_OT_TTI_Call
}


def register_transform_type_in():
	for cls in classes:
		register_class(cls)


def unregister_transform_type_in():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_transform_type_in()