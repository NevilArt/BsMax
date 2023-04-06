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

from bpy.types import Menu



class BsMax_MT_geometrynode_presets(Menu):
	bl_idname = "BSMAX_MT_geometrynode_import"
	bl_label = "BsMax Presets"

	def draw(self, ctx):
		layout=self.layout
		# Distribution
		layout.operator("nodes.import_node_groupe",
						text="Probability 10").name='Probability 10'

		# Math
		layout.operator("nodes.import_node_groupe",
						text="Sum").name='Sum'



def register_gnodes():
	bpy.utils.register_class(BsMax_MT_geometrynode_presets)

def unregister_gnodes():
	bpy.utils.unregister_class(BsMax_MT_geometrynode_presets)

if __name__ == "__main__":
	register_gnodes()