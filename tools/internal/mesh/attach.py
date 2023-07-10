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

from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator

from bsmax.operator import PickOperator



class Mesh_OT_Attach(PickOperator):
	bl_idname = 'mesh.attach'
	bl_label = 'Attach'
	
	filters = ['MESH', 'CURVE', 'FONT']

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object:
					return ctx.mode == 'EDIT_MESH'
		return False

	def convert(self, ctx, obj):
		bpy.ops.object.select_all(action='DESELECT')

		obj.select_set(True)
		ctx.view_layer.objects.active = obj

		""" Collaps Modifiers """
		for modifier in obj.modifiers:
			bpy.ops.object.modifier_apply(modifier=modifier.name)

		""" Set The Target Mode """
		bpy.ops.object.convert(target='MESH')

	def picked(self, ctx, source, subsource, target, subtarget):
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

		self.convert(ctx, target)
		
		for obj in source:
			obj.select_set(True)
			ctx.view_layer.objects.active = obj

			if obj.type in {'MESH', 'CURVE'}:
				""" Clear Primitive Data """
				obj.data.primitivedata.classname = ""

				""" Make Same Type if Possible """
				if target.type != obj.type:
					bpy.ops.object.convert_to(target=obj.type)

		target.select_set(state = True)
		bpy.ops.object.join()
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		bpy.ops.ed.undo_push()
		bpy.ops.mesh.attach('INVOKE_DEFAULT')



class Mesh_OT_Attach_List(Operator):
	bl_idname = 'mesh.attach_list'
	bl_label = 'Attach List'
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'EDIT_MESH'
		return False

	def execute(self, ctx):
		# print("Attach by list working on progress")
		return{'FINISHED'}



# Store Detach operator setting and restore on next time
class Mesh_Detach_Data:
	def __init__(self):
		self.element = True
		self.clone = False

mdd = Mesh_Detach_Data()



class Mesh_OT_Detach(Operator):
	""" Create new Object/Element form selection """
	bl_idname = 'mesh.detach'
	bl_label = 'Detach'

	element: BoolProperty(description='linked mesh on this object')
	name: StringProperty(name='Name', description='Name of New Object')
	clone: BoolProperty(description='keep original one and make a fresh copy')

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def draw(self, ctx):
		layout = self.layout
		box = layout.box()
		row = box.column()
		row.prop(self, 'element', text='Detach To Element')
		if not self.element:
			row.prop(self, 'name', text='')
		row.prop(self, 'clone', text='Detach as clone')

	def execute(self, ctx):
		global mdd
		mdd.element = self.element
		mdd.clone = self.clone

		if self.clone:
			bpy.ops.mesh.duplicate()
		
		if self.element:
			bpy.ops.mesh.split('INVOKE_DEFAULT')
		else:
			# get mesh objects list befor detach
			list_before = [ob for ob in bpy.data.objects if ob.type == 'MESH']
			bpy.ops.mesh.separate(type='SELECTED')
			# get objects list after detach
			list_after = [ob for ob in bpy.data.objects if ob.type == 'MESH']
			# remove befor list from after list 
			for i in list_before:
				list_after.remove(i)
			# rename new created object
			list_after[0].name = self.name
		
		return{'FINISHED'}

	def invoke(self, ctx, event):
		global mdd
		self.element = mdd.element
		self.clone = mdd.clone
		if ctx.active_object:
			self.name = ctx.active_object.name
		return ctx.window_manager.invoke_props_dialog(self, width=200)



classes = (
	Mesh_OT_Attach,
	Mesh_OT_Detach
	#Mesh_OT_Attach_List
)



def register_attach():
	for c in classes:
		bpy.utils.register_class(c)



def unregister_attach():
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == '__main__':
	register_attach()
