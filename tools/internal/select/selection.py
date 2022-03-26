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
from bpy.types import Operator
from bpy.props import BoolProperty
from bpy.props import EnumProperty, FloatProperty, FloatVectorProperty, BoolProperty



class Object_OT_Select_Similar(Operator):
	bl_idname = "object.select_similar"
	bl_label = "Select Similar"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False
	
	def execute(self, ctx):
		matt, clss, inst, subcls = [], [], [], []

		if ctx.active_object and len(ctx.selected_objects) == 1:

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
							if me.data.primitivedata.classname != "":
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
			for o in matt:
				o.select_set(True)
		elif subcls:
			for o in subcls:
				o.select_set(True)
		elif clss:
			for o in clss:
				o.select_set(True)
		elif inst:
			for o in inst:
				o.select_set(True)

		return{"FINISHED"}



class Object_OT_Select_Children(Operator):
	bl_idname = "object.select_children"
	bl_label = "Select Children"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	full: BoolProperty()
	extend: BoolProperty()

	@classmethod
	def poll(self, ctx):
		if ctx.mode == 'OBJECT':
			return len(ctx.selected_objects) > 0
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
		selected = ctx.selected_objects
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
		items=[('GREATER', 'Greater then', ''),
			('LESS', 'Less than', ''),
			('EQUAL', 'Equal to', '')])
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



def select_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.select_similar")
	layout.operator("object.select_children")



classes = [Object_OT_Select_by_Dimensions,
	Object_OT_Select_Similar,
	Object_OT_Select_Children]

def register_selection():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.VIEW3D_MT_select_object.append(select_menu)


def unregister_selection():
	bpy.types.VIEW3D_MT_select_object.remove(select_menu)
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_selection()