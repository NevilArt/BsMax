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

class Object_OT_Select_Instance(Operator):
	bl_idname = "object.select_instance"
	bl_label = "Select Instance"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False
	
	def execute(self, ctx):
		if ctx.active_object != None and len(ctx.selected_objects) == 1:
			for obj in ctx.scene.objects:
				if ctx.active_object.data == obj.data:
					obj.select_set(True)
		self.report({'OPERATOR'},'bpy.ops.object.select_instance()')
		return{"FINISHED"}

def BsMax_ReadPrimitiveData(obj):
	params = []
	if obj != None:
		params = obj.PrimitiveData.split(' ,')
	return params

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
		matt,clss,inst,subcls = [],[],[],[]
		if ctx.active_object != None and len(ctx.selected_objects) == 1:
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
								mecls = me.data.primitivedata.classname
								objcls = obj.data.primitivedata.classname
								if mecls == objcls:
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
		if len(matt) > 0:
			for o in matt:
				o.select_set(True)
		elif len(subcls) > 0:
			for o in subcls:
				o.select_set(True)
		elif len(clss) > 0:
			for o in clss:
				o.select_set(True)
		elif len(inst) > 0:
			for o in inst:
				o.select_set(True)
		self.report({'OPERATOR'},'bpy.ops.object.select_similar()')
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
		return ctx.mode == 'OBJECT'

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
		self.report({'OPERATOR'},'bpy.ops.object.select_children()')
		return{"FINISHED"}

def select_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.select_instance")
	layout.operator("object.select_similar")
	layout.operator("object.select_children")

classes = [Object_OT_Select_Instance, Object_OT_Select_Similar, Object_OT_Select_Children]

def register_selection():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.VIEW3D_MT_select_object.append(select_menu)


def unregister_selection():
	bpy.types.VIEW3D_MT_select_object.remove(select_menu)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_selection()