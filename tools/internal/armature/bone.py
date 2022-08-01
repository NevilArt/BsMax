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
from bpy.props import IntProperty, EnumProperty, BoolProperty
from bsmax.state import is_active_object



# Set Armatur bone type 
class Armature_OT_Bone_Type(Operator):
	bl_idname = "armature.bone_type"
	bl_label = "Bone Type"
	bl_options = {'REGISTER', 'UNDO'}
	
	mode: EnumProperty(name="Bone Draw type", default='BBONE',
			description='Armature Bone Draw Type',
			items=[('OCTAHEDRAL','Octahedral',''),('STICK','Stick',''),
			('BBONE','BBone',''),('ENVELOPE','Envelope',''),('WIRE','Wire','')])
	
	@classmethod
	def poll(self, ctx):
		return is_active_object(ctx, 'ARMATURE')
	
	def execute(self, ctx):
		ctx.object.data.display_type = self.mode
		return{"FINISHED"}


#TODO rename the operator
# Devide Bone by number dialog 
class Armature_OT_Bone_Devide(Operator):
	bl_idname = "armature.bone_devide"
	bl_label = "Bone Devide"
	bl_options = {'REGISTER', 'UNDO'}

	devides: IntProperty(name="Devides",default=1)
	typein: BoolProperty(name="Type In:",default=False)

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'EDIT_ARMATURE'
	
	def draw(self, ctx):
		layout = self.layout
		layout.prop(self,"devides",text="Devides")
	
	def execute(self, ctx):
		bpy.ops.armature.subdivide(number_cuts=self.devides)
		return {'FINISHED'}

	def modal(self, ctx, event):
		bpy.ops.armature.subdivide(number_cuts=self.devides)
		return {'CANCELLED'}

	def invoke(self, ctx, event):		
		if self.typein:
			wm = ctx.window_manager
			return wm.invoke_props_dialog(self, width=150)
		else:
			ctx.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}



class Armature_OT_Freeze(Operator):
	""" Freeze / Unfreeze Bones """
	bl_idname = "bone.freeze"
	bl_label = "Freeze / Unfreeze"
	bl_description = "Freeze / Unfreeze Bones"
	bl_options = {'REGISTER', 'UNDO'}

	mode: EnumProperty(default='selection',
						items=[
							('selection', 'Freeze Selection', ''),
							('unselected', 'Freeze Unselected', ''),
							('clear', 'Unfreezee All', '')
						]
			)
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode in {'POSE', 'EDIT_ARMATURE'}

	def execute(self, ctx):
		original_mode = ctx.mode
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

		if self.mode == 'selection':
			for bone in ctx.object.data.bones:
				if bone.select:
					bone.hide_select = True

		elif self.mode == 'unselected':
			for bone in ctx.object.data.bones:
				if not bone.select:
					bone.hide_select = True

		elif self.mode == 'clear':
			for bone in ctx.object.data.bones:
				bone.hide_select = False
		
		if original_mode == 'POSE':
			bpy.ops.object.mode_set(mode='POSE', toggle=False)
		else:
			bpy.ops.object.mode_set(mode='EDIT', toggle=False)

		return{"FINISHED"}



classes = (Armature_OT_Bone_Type, Armature_OT_Bone_Devide, Armature_OT_Freeze)

def register_bone():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_bone():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_bone()