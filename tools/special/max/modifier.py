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
from bsmax.actions import modifier_add
from bsmax.state import is_objects_selected

# Quick presets just like in 3ds max 
class BsMax_OT_FFD_2x2x2_Set(Operator):
	bl_idname = "modifier.ffd2x2x2set"
	bl_label = "FFD 2x2x2 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.bsmax.latticebox(res_u=2,res_v=2,res_w=2)
		return{"FINISHED"}

class BsMax_OT_FFD_3x3x3_Set(Operator):
	bl_idname = "modifier.ffd3x3x3set"
	bl_label = "FFD 3x3x3 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.bsmax.latticebox(res_u=3,res_v=3,res_w=3)
		return{"FINISHED"}

class BsMax_OT_FFD_4x4x4_Set(Operator):
	bl_idname = "modifier.ffd4x4x4set"
	bl_label = "FFD 4x4x4 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.bsmax.latticebox(res_u=4,res_v=4,res_w=4)
		return{"FINISHED"}

class BsMax_OT_BevelModifierAdd(Operator):
	bl_idname = "modifier.bevelmodifierass"
	bl_label = "Bevel (Add)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'BEVEL')
		return{"FINISHED"}

class BsMax_OT_AddLathe(Operator):
	bl_idname = "modifier.addlathe"
	bl_label = "Lathe (Add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SCREW')
		return {'FINISHED'}

class BsMax_OT_ResetXform(Operator):
	bl_idname = "bsmax.resetxform"
	bl_label = "Reset Xform"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		activeobject = ctx.active_object
		for obj in ctx.selected_objects:
			ctx.view_layer.objects.active = obj
			bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
		ctx.view_layer.objects.active = obj
		return{"FINISHED"}

class BsMax_OT_ShellModifierAdd(Operator):
	bl_idname = "modifier.shellmodifieradd"
	bl_label = "Shell (Add)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SOLIDIFY')
		return{"FINISHED"}

class BsMax_OT_TurboSmoothModifierAdd(Operator):
	bl_idname = "modifier.turbosmoothmodifieradd"
	bl_label = "TurboSmooth (Add)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SUBSURF')
		return{"FINISHED"}

classes = [BsMax_OT_BevelModifierAdd,
	BsMax_OT_FFD_2x2x2_Set,
	BsMax_OT_FFD_3x3x3_Set,
	BsMax_OT_FFD_4x4x4_Set,
	BsMax_OT_AddLathe,
	BsMax_OT_ResetXform,
	BsMax_OT_ShellModifierAdd,
	BsMax_OT_TurboSmoothModifierAdd]

def register_modifier():
	[bpy.utils.register_class(c) for c in classes]

def unregister_modifier():
	[bpy.utils.unregister_class(c) for c in classes]