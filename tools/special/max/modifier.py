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
class Modifier_OT_FFD_2x2x2_Set(Operator):
	bl_idname = "modifier.ffd_2x2x2_set"
	bl_label = "FFD 2x2x2 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.lattice.set_on_selection(res_u=2,res_v=2,res_w=2)
		self.report({'INFO'},'bpy.ops.modifier.ffd_2x2x2_set()')
		return{"FINISHED"}

class Modifier_OT_FFD_3x3x3_Set(Operator):
	bl_idname = "modifier.ffd_3x3x3_set"
	bl_label = "FFD 3x3x3 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.lattice.set_on_selection(res_u=3,res_v=3,res_w=3)
		self.report({'INFO'},'bpy.ops.modifier.ffd_3x3x3_set()')
		return{"FINISHED"}

class Modifier_OT_FFD_4x4x4_Set(Operator):
	bl_idname = "modifier.ffd_4x4x4_set"
	bl_label = "FFD 4x4x4 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.lattice.set_on_selection(res_u=4,res_v=4,res_w=4)
		self.report({'INFO'},'bpy.ops.modifier.ffd_4x4x4_set()')
		return{"FINISHED"}

class Modifier_OT_Add_Bevel(Operator):
	bl_idname = "modifier.add_bevel"
	bl_label = "Bevel (Add)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'BEVEL')
		self.report({'INFO'},'bpy.ops.modifier.add_bevel()')
		return{"FINISHED"}

class Modifier_OT_Add_Lathe(Operator):
	bl_idname = "modifier.add_lathe"
	bl_label = "Lathe (Add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SCREW')
		self.report({'INFO'},'bpy.ops.modifier.add_lathe()')
		return {'FINISHED'}

class Object_OT_Reset_Xform(Operator):
	bl_idname = "object.reset_xform"
	bl_label = "Reset Xform"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			ctx.view_layer.objects.active = obj
			bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
		ctx.view_layer.objects.active = obj
		self.report({'INFO'},'bpy.ops.object.reset_xform()')
		return{"FINISHED"}

class Modifier_OT_Add_Shell(Operator):
	bl_idname = "modifier.add_shell"
	bl_label = "Shell (Add)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SOLIDIFY',name="SHELL")
		self.report({'INFO'},'bpy.ops.modifier.add_shell()')
		return{"FINISHED"}

class Modifier_OT_Add_TurboSmooth(Operator):
	bl_idname = "modifier.add_turbosmooth"
	bl_label = "TurboSmooth (Add)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SUBSURF',name='Turbosmooth')
		self.report({'INFO'},'bpy.ops.modifier.add_turbosmooth()')
		return{"FINISHED"}

classes = [Modifier_OT_Add_Bevel,
	Modifier_OT_FFD_2x2x2_Set,
	Modifier_OT_FFD_3x3x3_Set,
	Modifier_OT_FFD_4x4x4_Set,
	Modifier_OT_Add_Lathe,
	Object_OT_Reset_Xform,
	Modifier_OT_Add_Shell,
	Modifier_OT_Add_TurboSmooth]

def register_modifier():
	[bpy.utils.register_class(c) for c in classes]

def unregister_modifier():
	[bpy.utils.unregister_class(c) for c in classes]