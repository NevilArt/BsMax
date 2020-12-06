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

class Armature_OT_Attach(PickOperator):
	bl_idname = "armature.attach"
	bl_label = "Attach"
	bl_options = {'REGISTER', 'UNDO'}
	filters = ['ARMATURE']

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'EDIT_ARMATURE'
		return False

	def picked(self, ctx, source, subsource, target, subtarget):
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		target.select_set(state = True)
		bpy.ops.object.join()
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		bpy.ops.armature.attach('INVOKE_DEFAULT')
		self.report({'OPERATOR'},'bpy.ops.armature.attach()')

classes = [Armature_OT_Attach]

def register_attach():
	[bpy.utils.register_class(c) for c in classes]

def unregister_attach():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_attach()