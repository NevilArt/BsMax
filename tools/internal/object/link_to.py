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
# 2024/04/08
# TODO need to clear function for all parenting types
# Need a better pick operator with more clear arg names

import bpy

from mathutils import Matrix
from bpy.types import Operator
from bpy.props import BoolProperty
from bpy.utils import register_class, unregister_class

from bsmax.operator import PickOperator
from bsmax.actions import link_to, freeze_transform
from bsmax.state import get_dimensions_avrage

def link_objects_to_bone(objects, armature, bone, keepHierarchy):
	matrixTranslation = Matrix.Translation(bone.tail - bone.head)
	worldMatrix = armature.matrix_world @ matrixTranslation @ bone.matrix

	if keepHierarchy:
		objects = [obj for obj in objects if not obj.parent]

	for obj in objects:
		copyWorldMatrix = obj.matrix_world.copy()
		invertMatrix = worldMatrix.inverted() @ copyWorldMatrix
		obj.matrix_parent_inverse = invertMatrix @ obj.matrix_basis.inverted()
		
		obj.parent = armature
		obj.parent_bone = bone.name
		obj.parent_type = 'BONE' 

		obj.matrix_world = copyWorldMatrix


def link_objects_to_object(objects, target, subtarget, keepHierarchy):
	if keepHierarchy:
		objects = [obj for obj in objects if not obj.parent]

	for obj in objects:
		""" unparent parent if linked to self child """
		if target.parent == obj:
			matrix_world = target.matrix_world.copy()
			target.parent = None
			target.matrix_world = matrix_world
			target.location = matrix_world.translation

		""" Unparent source objcets befor reparenting """
		matrix_world = obj.matrix_world.copy()
		obj.parent = None
		obj.matrix_world = matrix_world

		""" link to new target """
		obj.parent = target
		obj.matrix_parent_inverse = target.matrix_world.inverted()


def link_bones_to_bone(subsource, target, subtarget, keepHierarchy):
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	edit_bones = target.data.edit_bones
	for bone in subsource:
		""" Target and source[0] are same here """
		edit_bones[bone.name].parent = edit_bones[subtarget.name]
		# TODO have to keep transform
	# self.set_mode(self.mode)


def create_upnode(ctx):
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
			link_to(empty, obj.parent, False)
			link_to(obj, empty, False)
		else:
			link_to(obj, empty, False)

	# select only new created nodes
	bpy.ops.object.select_all(action='DESELECT')
	for empty in emptys:
		empty.select_set(state=True)

	ctx.scene.frame_current = frame


def has_any_parent(objects):
	for obj in objects:
		if obj.parent:
			return True
	return False


class LinkToBuffer():
	def __init__(self):
		self.source = None # Aramture or Objects
		self.sub_source = None # Bone Name list
		self.target = None # object or armature
		self.sub_target = None # bone name
	
	def reset(self):
		self.__init__()

linkToBuffer = LinkToBuffer()


class Object_OT_Link_to_Option(Operator):
	bl_idname = "object.link_to_option"
	bl_label = "Unlink"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	keepHierarchy: BoolProperty(default=False)

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'keepHierarchy')
	
	def execute(self, ctx):
		global linkToBuffer
		source = linkToBuffer.source
		subsource = linkToBuffer.sub_source
		target = linkToBuffer.target
		subtarget = linkToBuffer.sub_target

		if source and subtarget:
			link_objects_to_bone(
				source, target, subtarget, self.keepHierarchy
			)
		
		if not subsource and not subtarget:
			link_objects_to_object(
				source, target, subtarget, self.keepHierarchy
			)
		
		# TODO need new pick operator
		if subsource and subtarget:
			link_bones_to_bone(
				subsource, target, subtarget, self.keepHierarchy
			)

		linkToBuffer.reset()
		return{"FINISHED"}

	def invoke(self, ctx, event):
		objects = ctx.selected_objects
		if len(objects) > 1:
			if has_any_parent(objects):
				return ctx.window_manager.invoke_props_dialog(self)
		return self.execute(ctx)
	


class Object_OT_Link_to(PickOperator):
	""" This Class mimics the 3DsMax 'link to' operator """
	bl_idname = "object.link_to"
	bl_label = "Link to"
	bl_options = {'REGISTER'}
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.selected_objects
		return False

	def picked(self, ctx, source, subsource, target, subtarget):
		global linkToBuffer
		linkToBuffer.source = source
		linkToBuffer.sub_source = subsource
		linkToBuffer.target = target
		linkToBuffer.sub_target = subtarget
		bpy.ops.object.link_to_option('INVOKE_DEFAULT')


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
		create_upnode(ctx)
		return{'FINISHED'}


def linkto_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.link_to")
	layout.operator('object.create_upnode')


classes = (
	Object_OT_Link_to,
	Object_OT_Link_to_Option,
	Object_OT_Unlink,
	Object_OT_Create_up_node
)


def register_link_to():
	for c in classes:
		register_class(c)

	bpy.types.VIEW3D_MT_object_parent.append(linkto_menu)


def unregister_link_to():
	bpy.types.VIEW3D_MT_object_parent.remove(linkto_menu)

	for c in classes:
		unregister_class(c)


if __name__ == "__main__":
	register_link_to()