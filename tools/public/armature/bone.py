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

def bone_cls(register):
	classes = [BsMax_OT_SetArmaturBoneType,BsMax_OT_BoneDevide,BsMax_OT_ArmatorEditMenu]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	bone_cls(True)

__all__ = ["bone_cls"]