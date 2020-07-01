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

class Object_OT_Convert(bpy.types.Operator):
	bl_idname = "object.smart_convert"
	bl_label = "Smart Convert"
	# bl_description = ""

	target: bpy.props.EnumProperty(default='MESH',items=[('MESH','Mesh',''),('CURVE','Curve','')])

	def execute(self, ctx):
		if self.target == 'MESH':
			bpy.ops.primitive.cleardata('INVOKE_DEFAULT')
			bpy.ops.object.convert(target='MESH')
		elif self.target == 'CURVE':
			bpy.ops.primitive.cleardata('INVOKE_DEFAULT')
			bpy.ops.object.convert(target='CURVE')
		return{"FINISHED"}

def register_convert():
	bpy.utils.register_class(Object_OT_Convert)

def unregister_convert():
	bpy.utils.unregister_class(Object_OT_Convert)

if __name__ == "__main__":
	register_convert()