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

from bpy.types import Operator, PropertyGroup
from bpy.props import (EnumProperty, FloatProperty, FloatVectorProperty,
						BoolProperty, PointerProperty)



class Object_OT_Select_All(Operator):
	""" Select all Objects + Pose Bones """
	bl_idname = "object.select_all_plus"
	bl_label = "Select All (+Bones)"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		bpy.ops.object.select_all(action='SELECT')
		for obj in ctx.selected_objects:
			if obj.type == "ARMATURE":
				for bone in obj.data.bones:
					bone.select = True
		return{"FINISHED"}



class Object_OT_Select_Similar(Operator):
	""" Select similar object to the currently selected object """
	bl_idname = "object.select_similar"
	bl_label = "Select Similar"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.selected_objects
		return False
	
	def execute(self, ctx):
		matt, clss, inst, subcls = [], [], [], []

		if not (ctx.active_object and len(ctx.selected_objects)):
			return{"FINISHED"}

		me = ctx.active_object
		for obj in ctx.scene.objects:
			if me != obj:
				# Collect instances
				if me.data == obj.data:
					inst.append(obj)

				# type and sub types
				if me.type == obj.type:
					clss.append(obj)

					if me.type in ['MESH','CURVE']:
						# check for primitive objects
						if me.data.primitivedata.classname:
							my_cls = me.data.primitivedata.classname
							obj_cls = obj.data.primitivedata.classname
							if my_cls == obj_cls:
								subcls.append(obj)

						# Material
						if me.data.materials == obj.data.materials:
							matt.append(obj)	

					if me.type == 'EMPTY':
						if me.empty_display_type == obj.empty_display_type:
							subcls.append(obj)

					if me.type == 'LIGHT':
						if me.data.type == obj.data.type:
							subcls.append(obj)

		# Chose Selection type by preiroty 
		if matt:
			for obj in matt:
				obj.select_set(True)

		elif subcls:
			for obj in subcls:
				obj.select_set(True)

		elif clss:
			for obj in clss:
				obj.select_set(True)

		elif inst:
			for obj in inst:
				obj.select_set(True)

		return{"FINISHED"}



class Object_OT_Select_Children(Operator):
	""" Select selected objects children """
	bl_idname = "object.select_children"
	bl_label = "Select Children"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	full: BoolProperty(name="Select all subtrees")
	extend: BoolProperty(name="Select Extended")
	active_only: BoolProperty(name="Only active object subtrees", default=True)

	@classmethod
	def poll(self, ctx):
		if ctx.mode == 'OBJECT':
			return ctx.selected_objects
		return False

	def collect_children(self, objs):
		children = []
		for obj in objs:
			for child in obj.children:
				if not child in objs:
					children.append(child)
					child.select_set(state = True)

		return children
	
	def execute(self, ctx):
		bpy.ops.view3d.select(extend=True)
		selected = [ctx.active_object] if self.active_only \
		 								else ctx.selected_objects

		nsc = len(selected) # New Selected Count

		if self.full == True:
			children = selected
			while nsc != 0:
				children = self.collect_children(children)
				nsc = len(children)

		else:
			for obj in selected:
				for child in obj.children:
					child.select_set(state = True)

		return{"FINISHED"}



#TODO this operator re write the object dimention
# maybe system undo couse that need to take control of it in report the bug
class Object_OT_Select_by_Dimensions(Operator):
	bl_idname = "object.select_by_dimensions"
	bl_label = "Select by Dimensions"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}

	by: EnumProperty(name='By', default='GREATER',
					items=[
							('GREATER', 'Greater then', ''),
							('LESS', 'Less than', ''),
							('EQUAL', 'Equal to', '')
						]
					)

	dimensions: FloatVectorProperty(name='Dimension', subtype='TRANSLATION')
	tolerans: FloatProperty(name='Tolerance', default=0)

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'

	def draw(self, ctx):
		layout = self.layout
		row = layout.row()
		row.prop(self, 'by', expand=True)
		col = layout.column(align=True)
		col.prop(self, 'dimensions')
		if self.by == 'EQUAL':
			layout.prop(self, 'tolerans')
	
	def execute(self, ctx):
		if self.by == 'GREATER':
			for obj in bpy.data.objects:
				if obj.dimensions.x > self.dimensions.x or \
					obj.dimensions.y > self.dimensions.y or \
					obj.dimensions.z > self.dimensions.z:

					obj.select_set(state=True)

		elif self.by == 'LESS':
			for obj in bpy.data.objects:
				if obj.dimensions.x < self.dimensions.x or \
					obj.dimensions.y < self.dimensions.y or \
					obj.dimensions.z < self.dimensions.z:

					obj.select_set(state=True)

		elif self.by == 'EQUAL':
			tol = self.tolerans/2
			for obj in bpy.data.objects:
				odim = obj.dimensions.copy()
				sdim = self.dimensions
				if sdim.x - tol < odim.x < sdim.x + tol or \
					sdim.y - tol < odim.y < sdim.y + tol or \
					sdim.z - tol < odim.z < sdim.z + tol:

					obj.select_set(state=True)

		return{'FINISHED'}



class Selection_lock_Property(PropertyGroup):
	locked: BoolProperty(name='Lock Selection', default=False,
		description='Lock Selection')



class Selection_Type_State:
	def __init__(self):
		self.select_mesh = True
		self.select_curve = True
		self.select_surf = True
		self.select_meta = True
		self.select_font = True
		self.select_pointcloud = True
		self.select_volume = True
		self.select_grease_pencil = True
		self.select_armature = True
		self.select_lattice = True
		self.select_empty = True
		self.select_light = True
		self.select_light_probe = True
		self.select_camera = True
		self.select_speaker = True

	def store_state(self, ctx):
		""" Store Current State """
		space_data = ctx.space_data
		self.select_mesh = space_data.show_object_select_mesh
		self.select_curve = space_data.show_object_select_curve
		self.select_surf = space_data.show_object_select_surf
		self.select_meta = space_data.show_object_select_meta
		self.select_font = space_data.show_object_select_font
		self.select_pointcloud = space_data.show_object_select_pointcloud
		self.select_volume = space_data.show_object_select_volume
		self.select_grease_pencil = space_data.show_object_select_grease_pencil
		self.select_armature = space_data.show_object_select_armature
		self.select_lattice = space_data.show_object_select_lattice
		self.select_empty = space_data.show_object_select_empty
		self.select_light = space_data.show_object_select_light
		self.select_light_probe = space_data.show_object_select_light_probe
		self.select_camera = space_data.show_object_select_camera
		self.select_speaker = space_data.show_object_select_speaker

	def restore_state(self, ctx):
		space_data = ctx.space_data
		space_data.show_object_select_mesh = self.select_mesh
		space_data.show_object_select_curve = self.select_curve
		space_data.show_object_select_surf = self.select_surf
		space_data.show_object_select_meta = self.select_meta
		space_data.show_object_select_font = self.select_font
		space_data.show_object_select_pointcloud = self.select_pointcloud
		space_data.show_object_select_volume = self.select_volume
		space_data.show_object_select_grease_pencil = self.select_grease_pencil
		space_data.show_object_select_armature = self.select_armature
		space_data.show_object_select_lattice = self.select_lattice
		space_data.show_object_select_empty = self.select_empty
		space_data.show_object_select_light = self.select_light
		space_data.show_object_select_light_probe = self.select_light_probe
		space_data.show_object_select_camera = self.select_camera
		space_data.show_object_select_speaker = self.select_speaker
		ctx.scene.selection_lock.locked = False

	def is_lock(self, ctx):
		return ctx.scene.selection_lock.locked
	
	def set_lock(self, ctx):
		space_data = ctx.space_data
		space_data.show_object_select_mesh = False
		space_data.show_object_select_curve = False
		space_data.show_object_select_surf = False
		space_data.show_object_select_meta = False
		space_data.show_object_select_font = False
		space_data.show_object_select_pointcloud = False
		space_data.show_object_select_volume = False
		space_data.show_object_select_grease_pencil = False
		space_data.show_object_select_armature = False
		space_data.show_object_select_lattice = False
		space_data.show_object_select_empty = False
		space_data.show_object_select_light = False
		space_data.show_object_select_light_probe = False
		space_data.show_object_select_camera = False
		space_data.show_object_select_speaker = False
		ctx.scene.selection_lock.locked = True

selection_type_state = Selection_Type_State()



class Object_OT_Lock_Selection_Toggle(Operator):
	""" Lock Selection Toggle """
	bl_idname = "object.lock_selection_toggle"
	bl_label = "Lock Selection Toggle"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		global selection_type_state

		if selection_type_state.is_lock(ctx):
			selection_type_state.restore_state(ctx)

		else:
			selection_type_state.store_state(ctx)
			selection_type_state.set_lock(ctx)

		return{"FINISHED"}




def prepend_select_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.select_all_plus", text="All + Bones")



def append_select_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.select_similar")
	layout.operator("object.select_children")
	# layout.operator("object.select_by_dimensions")



classes = (
	Object_OT_Select_All,
	Selection_lock_Property,
	Object_OT_Select_by_Dimensions,
	Object_OT_Select_Similar,
	Object_OT_Select_Children,
	Object_OT_Lock_Selection_Toggle
)



def register_selection():
	for c in classes:
		bpy.utils.register_class(c)

	bpy.types.VIEW3D_MT_select_object.prepend(prepend_select_menu)
	bpy.types.VIEW3D_MT_select_object.append(append_select_menu)
	
	bpy.types.Scene.selection_lock = PointerProperty(type=Selection_lock_Property)


def unregister_selection():
	bpy.types.VIEW3D_MT_select_object.remove(prepend_select_menu)
	bpy.types.VIEW3D_MT_select_object.remove(append_select_menu)
	
	del bpy.types.Scene.selection_lock

	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_selection()