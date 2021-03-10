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


class Particle_OT_Hair_Symmetry(Operator):
	bl_idname = 'particle.hair_symmetry'
	bl_label = 'Hair Symmetry'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if ctx.mode == 'OBJECT':
				if len(ctx.selected_objects) == 1:
					return ctx.object.type == 'MESH'
		return False
	
	def draw(self,ctx):
		pass

	def execute(self,ctx):
		print("done")
		self.report({'OPERATOR'},'bpy.ops.particle.hair_symmetry()')
		return{"FINISHED"}
	
	def cancel(self,ctx):
		# restore(self,ctx)
		return None

	def invoke(self,ctx,event):
		return ctx.window_manager.invoke_props_dialog(self)

def register_hair_symmetry():
	bpy.utils.register_class(Particle_OT_Hair_Symmetry)

def unregister_hair_symmetry():
	bpy.utils.unregister_class(Particle_OT_Hair_Symmetry)

if __name__ =="__main__":
	register_hair_symmetry()