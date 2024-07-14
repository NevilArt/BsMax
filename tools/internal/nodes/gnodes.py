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
# 2024/07/01

from bpy.types import Menu
from bpy.utils import register_class, unregister_class


class BsMax_MT_Geometry_Node_Crowds(Menu):
	bl_idname = 'BSMAX_MT_geometry_node_crowds'
	bl_label = "Crowds"

	def draw(self, ctx):
		layout = self.layout

		#TODO solve version issue
		layout.operator(
			'nodes.import_node_group',
			text="Walk on path", icon='MOD_HUE_SATURATION'
		).name = 'Crowds walk on path'
		

		layout.operator(
			'nodes.import_node_group',
			text="Chikens in Fence", icon='STICKY_UVS_LOC'
		).name='Crowds Chiken'

		layout.operator(
			'nodes.import_node_group',
			text="Studiom Audience", icon='ALIASED'
		).name='Crowds Studiom'

		layout.operator(
			'nodes.import_node_group',
			text="Talking Groups", icon='OUTLINER_DATA_POINTCLOUD'
		).name='Crowds Talkers'


class BsMax_MT_Geometry_Node_Tools(Menu):
	bl_idname = 'BSMAX_MT_geometry_node_tools'
	bl_label = "Preset"

	def draw(self, ctx):
		layout = self.layout
		# Distribution
		layout.operator(
			'nodes.import_node_group', text="Probability 10"
		).name='Probability 10'

		# Math
		layout.operator(
			'nodes.import_node_group', text="Sum"
		).name='Sum'



class BsMax_MT_Geometry_Node_Presets(Menu):
	bl_idname = 'BSMAX_MT_geometrynode_import'
	bl_label = "BsMax Presets"

	def draw(self, ctx):
		layout=self.layout
		layout.menu('BSMAX_MT_geometry_node_crowds')
		layout.menu('BSMAX_MT_geometry_node_tools')
		


classes = {
	BsMax_MT_Geometry_Node_Crowds,
	BsMax_MT_Geometry_Node_Tools,
	BsMax_MT_Geometry_Node_Presets
}


def register_gnodes():
	for cls in classes:
		register_class(cls)


def unregister_gnodes():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_gnodes()