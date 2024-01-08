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

from bpy.types import Operator



# Act like Convert to in 3ds Max
class BsMax_OT_ClearPrimitiveData(Operator):
	# TODO replace this with a smart convert tool
	bl_idname="primitive.cleardata"
	bl_label="Clear Primitive Data"
	def execute(self, ctx):
		for obj in ctx.selected_objects:
			obj.data.primitivedata.classname = ""
		return {"FINISHED"}


def BsMax_MT_PrimitiveDataCleanerMenu(self, ctx):
	self.layout.separator()
	self.layout.operator("primitive.cleardata")

def register_ui():
	bpy.utils.register_class(BsMax_OT_ClearPrimitiveData)

def unregister_ui():
	bpy.utils.unregister_class(BsMax_OT_ClearPrimitiveData)