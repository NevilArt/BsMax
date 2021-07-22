############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################
import bpy

class Camera_PT_Panel(bpy.types.Panel):
	bl_label = "Target / Tools"
	bl_idname = "DATA_PT_Camera"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"
	bl_options = {'DEFAULT_CLOSED'}

	@classmethod
	def poll(cls,ctx):
		return ctx.object.type == 'CAMERA'

	def draw(self, ctx):
		layout = self.layout
		row = layout.row()
		row.operator('camera.create_target', text='Create Target')
		row.operator('camera.select_target', text='Select Target')
		row.operator('camera.clear_targte', text='Clear Target')
		row = layout.row()
		row.operator('camera.create_dof_target', text='Create DOF Target')
		row.operator('camera.select_dof_target', text='Select DOF Target')

classes = [Camera_PT_Panel]

def register_panel():
	[bpy.utils.register_class(c) for c in classes]

def unregister_panel():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_panel()