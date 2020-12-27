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
from bsmax.operator import PickOperator

class Object_OT_Attach(PickOperator):
	bl_idname = "armature.attach"
	bl_label = "Attach"
	
	filters = ['AUTO'] #text, curve, mesh

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'OBJECT' #edit armature
		return False
	
	def convert(self, ctx, obj):
		obj.select_set(True)
		ctx.view_layer.objects.active = obj
		
		""" collaps modifiers """
		for modifier in obj.modifiers:
			bpy.ops.object.modifier_apply(modifier=modifier.name)

		# """ set the target mode """
		# bpy.ops.object.convert(target="MESH")


	def picked(self, ctx, source, subsource, target, subtarget):
        # 
		self.report({'OPERATOR'},'bpy.ops.armature.attach()')

classes = [Object_OT_Attach]

def register_attach():
	[bpy.utils.register_class(c) for c in classes]

def unregister_attach():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_attach()