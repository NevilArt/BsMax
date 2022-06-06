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

from mathutils import Matrix
from bpy.types import Operator

from bsmax.operator import PickOperator
from bsmax.actions import link_to, freeze_transform
from bsmax.state import get_dimensions_avrage



class Object_OT_Link_to(PickOperator):
	""" This Class mimics the 3DsMax 'link to' operator """
	bl_idname = "object.link_to"
	bl_label = "Link to"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.selected_objects
		return False

	def link_to_bone(self, obj, armature, bone):
		t = Matrix.Translation(bone.tail - bone.head)
		tmw = armature.matrix_world @ t @ bone.matrix
		cmw = obj.matrix_world.copy()

		cml = tmw.inverted() @ cmw
		obj.matrix_parent_inverse = cml @ obj.matrix_basis.inverted()
		
		obj.parent = armature
		obj.parent_bone = bone.name
		obj.parent_type = 'BONE' 

		obj.matrix_world = cmw

	def picked(self, ctx, source, subsource, target, subtarget):
		if not subsource:
			""" Object -> Object """
			for sobj in source:
				""" unparent parent if linked to self child """
				if target.parent == sobj:
					matrix_world = target.matrix_world.copy()
					target.parent = None
					target.matrix_world = matrix_world
					target.location = matrix_world.translation
				""" Unparent source objcets befor reparenting """
				matrix_world = sobj.matrix_world.copy()
				sobj.parent = None
				sobj.matrix_world = matrix_world
				""" link to new target """
				sobj.parent = target
				sobj.matrix_parent_inverse = target.matrix_world.inverted()
		
				""" Object -> Bone """
				if subtarget:
					self.link_to_bone(sobj, target, subtarget)
		
		if not subsource and not subtarget:
			bpy.ops.object.select_all(action='DESELECT')
			target.select_set(True)
			ctx.view_layer.objects.active = target
			bpy.ops.ed.undo_push()
			bpy.ops.object.link_to('INVOKE_DEFAULT')

		""" Bone -> Bone """
		if subsource and subtarget:
			bpy.ops.object.mode_set(mode='EDIT', toggle=False)
			edit_bones = target.data.edit_bones
			for bone in subsource:
				""" Target and source[0] are same here """
				edit_bones[bone.name].parent = edit_bones[subtarget.name]
				# TODO have to keep transform
			# self.set_mode(self.mode)



class Object_OT_Unlink(Operator):
	bl_idname = "object.unlink"
	bl_label = "Unlink"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			matrix_world = obj.matrix_world.copy()
			obj.parent = None
			obj.matrix_world = matrix_world
		return{"FINISHED"}



class Object_OT_Create_up_node(Operator):
	bl_idname = 'object.create_upnode'
	bl_label = 'Create Upnode'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.selected_objects
		return False
	
	def execute(self, ctx):
		""" get current state info """
		objs = ctx.selected_objects.copy()
		bpy.ops.object.select_all(action='DESELECT')
		emptys = []
		frame = ctx.scene.frame_current
		ctx.scene.frame_current = 0
		for obj in objs:
			bpy.ops.object.empty_add(type='PLAIN_AXES')
			empty = ctx.active_object
			emptys.append(empty)
			size = get_dimensions_avrage(obj, True, True, False)
			empty.empty_display_size = size
			empty.name = obj.name + "_root_node"

			empty.matrix_world = obj.matrix_world
			freeze_transform([obj])

			if obj.parent:
				link_to(empty, obj.parent)
				link_to(obj, empty)
			else:
				link_to(obj, empty)

		# select only new created nodes
		bpy.ops.object.select_all(action='DESELECT')
		for empty in emptys:
			empty.select_set(state=True)

		ctx.scene.frame_current = frame

		return{'FINISHED'}



def linkto_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.link_to")
	layout.operator('object.create_upnode')

classes = [Object_OT_Link_to, Object_OT_Unlink, Object_OT_Create_up_node]


def register_link_to():
	for c in classes:
		bpy.utils.register_class(c)

	bpy.types.VIEW3D_MT_object_parent.append(linkto_menu)


def unregister_link_to():
	bpy.types.VIEW3D_MT_object_parent.remove(linkto_menu)

	for c in classes:
		bpy.utils.unregister_class(c)


if __name__ == "__main__":
	register_link_to()