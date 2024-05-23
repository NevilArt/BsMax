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
# 2024/05/21

import bpy

from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty
from bpy.utils import register_class, unregister_class

# TODO Make unique Add realize instance to geometry node before apply
# in quad menu conver to Gpencil and curves not working
# hide impossible items from convert list e.g. conver to curves for mesh objects
# add type check or filter if multiple object was selected
# 

def geometrynode_solve(obj):
	# find geo node modifiers
	# make it unique
	# find output node
	# add relize instance note
	pass


def select_objects(objects):
	for obj in objects:
		obj.select_set(True)


def set_as_active_object(ctx, obj):
	obj.select_set(True)
	if obj != ctx.active_object:
		ctx.view_layer.objects.active = obj


def rename_uvs(name, objects):
	for obj in objects:
		if len(obj.data.uv_layers) == 1:
			obj.data.uv_layers[0].name = name


def convert_to_execute(cls, ctx):
	active_object = ctx.active_object
	selected_objects = ctx.selected_objects.copy()
	bpy.ops.object.select_all(action='DESELECT')

	for obj in selected_objects:
		""" Clear primitive data """
		if obj.type in {'MESH', 'CURVE'}:
			obj.data.primitivedata.classname = ""

		""" Make unique """
		obj.data = obj.data.copy()

		""" Make GeoNode possible to apply """
		geometrynode_solve(obj)
		
		""" Set the target mode """
		if obj.type != cls.target:
			set_as_active_object(ctx, obj)
			bpy.ops.object.convert(target=cls.target)

	# convert to graspancel delete the old object an genarate new one
	if cls.target != 'GPENCIL':
		select_objects(selected_objects)
		set_as_active_object(ctx, active_object)


def uv_name_fixer(active, objs):
	names = [uvLayer.name for uvLayer in active.data.uv_layers]
	for obj in objs:
		if len(names) == len(obj.data.uv_layers):
			for i in range(len(names)):
				obj.data.uv_layers[i].name = names[i]

#TODO make instance real befor convert
def join_plus_execute(cls, ctx):
	target = ctx.active_object
		
	""" if active object not selected ignore it and pick first object """
	if not target:
		target = ctx.view_layer.objects.active = ctx.selected_objects[0]

	if not target.select_get():
		target = ctx.view_layer.objects.active = ctx.selected_objects[0]

	""" """
	if cls.convert:
		
		selected_objects = ctx.selected_objects.copy()
		bpy.ops.object.select_all(action='DESELECT')

		""" filter selection """
		leagles = ('MESH','CURVE','FONT','GPENCIL')
		selected_objects = [
			obj for obj in selected_objects if obj.type in leagles
		]

		""" if both object active and target has only one UV chanel
			make the name same """
		if cls.renameUVs:
			uv_name_fixer(target, selected_objects)
		
		""" clear primitive data """
		if target.type in {'MESH','CURVE'}:
			target.data.primitivedata.classname = ""
		
		for obj in selected_objects:

			""" Make same type as possible """
			if obj.type != target.type:
				set_as_active_object(ctx, obj)
				bpy.ops.object.convert(target=target.type)

			""" Make instanse objects unique """
			obj.data = obj.data.copy()
			
			""" Apply Modifiers """
			for modifier in obj.modifiers:
				set_as_active_object(ctx, obj)
				bpy.ops.object.modifier_apply(modifier=modifier.name)
		
			obj.select_set(False)

		""" Refine selection """
		select_objects(selected_objects)
		set_as_active_object(ctx, target)

	bpy.ops.object.join()	


def join_plus_draw(self, _):
	layout = self.layout

	row = layout.row()
	row.prop(self, 'convert')
	row.prop(self, 'renameUVs')

	if self.convert:
		layout.label(
			text="Apply Modifiers and make objects Unique befor joine"
		)

	else:
		layout.label(
			text="Don`t make any change and just call Join Operator"
		)


class Object_OT_Convert_TO(Operator):
	bl_idname = 'object.convert_to'
	bl_label = "Convert to (BsMax)"
	bl_description = "Simulate 3DsMax Convert To operator"
	bl_options = {'REGISTER', 'UNDO'}

	target: EnumProperty(
		items=[
			('MESH', "Mesh", ""),
	 		('CURVE', "Curve", ""),
			('GPENCIL', "Grease Pencil", ""),
			('CURVES', "Curves (Hair)", "")
		],
		default='MESH'
	) # type: ignore

	def execute(self, ctx):
		convert_to_execute(self, ctx)
		return{"FINISHED"}


class Object_OT_Join_Plus(Operator):
	""" Join selected objects to active object if are in same type """
	bl_idname = 'object.join_plus'
	bl_label = "Join (Plus)"
	bl_description = "attach selected object to active one"
	bl_options = {'REGISTER', 'UNDO'}

	convert: BoolProperty(name="Apply befor Join", default=True) # type: ignore
	renameUVs: BoolProperty(default=True) # type: ignore

	@classmethod
	def poll(self, ctx):
		return len(ctx.selected_objects) > 1
	
	def draw(self, ctx):
		join_plus_draw(self, ctx)

	def execute(self, ctx):
		join_plus_execute(self, ctx)
		return{"FINISHED"}

	def invoke(self, ctx, _):
		return ctx.window_manager.invoke_props_dialog(self)


classes = {
	Object_OT_Convert_TO,
	Object_OT_Join_Plus
}


def register_convert():
	for c in classes:
		register_class(c)


def unregister_convert():
	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_convert()