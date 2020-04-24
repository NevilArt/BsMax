############################################################################
#	BsMax, 3D apps inteface simulator and tools pack for Blender
#	Copyright (C) 2020  Naser Merati (Nevil)
#
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
class BsMax_OT_SetArmaturBoneType(Operator):
	bl_idname = "bmax.armaturebonetype"
	bl_label = "Armature Bone Type"
	mode: EnumProperty(name="Bone Draw type", default='BBONE',
			description='Armature Bone Draw Type',
			items=[('OCTAHEDRAL','Octahedral',''),('STICK','Stick',''),
			('BBONE','BBone',''),('ENVELOPE','Envelope',''),('WIRE','Wire','')])
	@classmethod
	def poll(self, ctx):
		return is_active_object(ctx, 'ARMATURE')
	def execute(self, ctx):
		if ctx.active_object != None:
			ctx.object.data.display_type = self.mode
		return{"FINISHED"}

# Devide Bone by number dialog 
class BsMax_OT_BoneDevide(Operator):
	bl_idname = "bmax.bonedevide"
	bl_label = "Bone Devide"
	devides: IntProperty(name="Devides",default=1)
	typein: BoolProperty(name="Type In:",default=False)
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

class BsMax_OT_ArmatorEditMenu(Operator):
	bl_idname = "bmax.armatoreditmenu"
	bl_label = "Armator Edit Menu"
	def execute(self, contecxt):
		bpy.ops.wm.call_menu(name=CM_ArmatorEdit_Menue.bl_idname)
		return{"FINISHED"}

classes = [BsMax_OT_SetArmaturBoneType,BsMax_OT_BoneDevide,BsMax_OT_ArmatorEditMenu]

def register_bone():
	[bpy.utils.register_class(c) for c in classes]

def unregister_bone():
	[bpy.utils.unregister_class(c) for c in classes]