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

import bpy, math
from bpy.props import FloatProperty, IntProperty, FloatVectorProperty
from bpy.types import PropertyGroup, Operator, Panel
from bpy.utils import register_class, unregister_class


class GRAPH_OT_Temp(Operator):
	bl_idname = "graph.temp"
	bl_label = "GRAPH"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return True
	
	def execute(self, context):
		return{'FINISHED'}


# Dope Sheet Editor Panel
class DopeSheet_PT_Toolbar(Panel):
	bl_idname = 'DOPESHEET_PT_toolbar'
	bl_label = "Tools"
	bl_space_type = "GRAPH_EDITOR"
	bl_region_type = "UI"
	bl_category = "BsMax"

	def draw(self, context):
		layout = self.layout
		box = layout.box()
		row = box.row(align=True)
		row.operator('graph.temp', text="Location")
		row.operator('graph.temp', text="Rotation")
		row.operator('graph.temp', text="Scale")
		row = box.row(align=True)
		row.operator('graph.temp', text="X")
		row.operator('graph.temp', text="Y")
		row.operator('graph.temp', text="Z")

		box = layout.box()
		col=box.column(align=True)
		row = col.row(align=True)
		row.operator('graph.temp', text="", icon='INVERSESQUARECURVE')
		row.operator('graph.temp', text="", icon='SHARPCURVE')
		row.operator('graph.temp', text="", icon='SEQ_LUMA_WAVEFORM')
		row.operator('graph.temp', text="", icon='RECORD_OFF')
		row.operator('graph.temp', text="", icon='IPO_CONSTANT')
		row.operator('graph.temp', text="", icon='IPO_LINEAR')

classes = {
	GRAPH_OT_Temp,
	DopeSheet_PT_Toolbar
}


def register_tool_bar():
	for cls in classes:
		register_class(cls)


def unregister_tool_bar():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_tool_bar()