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



def bsmax_matt_menu(self, ctx):
	layout = self.layout
	layout.separator()
	
	if ctx.space_data.type == "NODE_EDITOR":
	
		if ctx.area.ui_type == 'GeometryNodeTree':
			layout.menu("BSMAX_MT_geometrynode_import")
		
		elif ctx.area.ui_type == 'CompositorNodeTree':
				pass
		
		elif ctx.area.ui_type == 'ShaderNodeTree':
			if ctx.space_data.shader_type == 'OBJECT':
				layout.menu("BSMAX_MT_material_import")

			elif ctx.space_data.shader_type == 'WORLD':
				pass



def register_nodes_menu():
	bpy.types.NODE_MT_add.append(bsmax_matt_menu)

def unregister_nodes_menu():
	bpy.types.NODE_MT_add.remove(bsmax_matt_menu)

if __name__ == "__main__":
	register_nodes_menu()