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
		if ctx.active_object != None:
			ctx.object.data.display_type = self.mode
		self.report({'OPERATOR'},'bpy.ops.armature.bone_type(mode="'+ self.mode +'")')
		return{"FINISHED"}


#TODO rename the operator
# Devide Bone by number dialog 
class Armature_OT_Bone_Devide(Operator):
	bl_idname = "armature.bone_devide"
	bl_label = "Bone Devide"
	bl_options = {'REGISTER', 'UNDO'}
	devides: IntProperty(name="Devides",default=1)
	typein: BoolProperty(name="Type In:",default=False)
	
	def draw(self, ctx):
		layout = self.layout
		layout.prop(self,"devides",text="Devides")
	
	def execute(self, ctx):
		bpy.ops.armature.subdivide(number_cuts=self.devides)
		d = 'devides='+ str(self.devides)
		t = 'typein=' + str(self.typein)
		self.report({'OPERATOR'},'bpy.ops.armature.bone_devide('+ d +','+ t +')')
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



classes = [Armature_OT_Bone_Type, Armature_OT_Bone_Devide]

def register_bone():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_bone():
	for c in classes:
		bpy.utils.unregister_class(c)