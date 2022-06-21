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
from bpy.props import BoolProperty, EnumProperty, FloatProperty


def create_obj_driver(obj, chanel, subchanel, start, end):
	driver = obj.data.dof.driver_add('aperture_fstop')
	bpy.data.driver_add('aperture_fstop')
	
	driver.driver.type = 'SCRIPTED'

	var = driver.driver.variables.new()
	var.name = 's'
	var.type = 'SINGLE_PROP'
	var.targets[0].id = obj
	var.targets[0].data_path = 'empty_display_size'

	x = driver.driver.variables.new()
	x.name = 'x'
	x.type = 'TRANSFORMS'
	x.targets[0].id = obj
	x.targets[0].transform_type = 'SCALE_X'


	driver.driver.expression = 's*((x+y+z)/3)'
	# obj.
	return ""



def create_bone_driver(bone, chanel, subchanel, start, end):
	return ""



class Rigg_TO_Wire_Parameter(Operator):
	bl_idname = 'rigg.wire_parameter'
	bl_label = 'Wire Parameter'
	bl_description = ''
	bl_options = {'REGISTER', 'UNDO'}

	chanel: EnumProperty(items=[
							("LOCATION", "Location", ""),
							("ROTATION", "Rotation", ""),
							("SCALE", "Scale", "")
						]
					)
	axis: EnumProperty(items=[
							("X", "X", ""),
							("Y", "Y", ""),
							("Z", "Z", "")
						]
					)
	
	start: FloatProperty()
	end: FloatProperty()

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return ctx.active_object
		return False

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'chanel', expand=True)
		layout.prop(self, 'axis', expand=True)
		row = layout.row()
		row.prop(self, 'start')
		row.prop(self, 'end')

	def execute(self, ctx):
		if ctx.mode == 'OBJECT':
			create_obj_driver(ctx.object, self.chanel, self.axis,
								self.start, self.end)
		if ctx.mode == 'POSE':
			create_bone_driver(ctx.object, self.chanel, self.axis,
								self.start, self.end)
		return {'FINISHED'}

	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self)



def register_wire_parameter():
	bpy.utils.register_class(Rigg_TO_Wire_Parameter)

def unregister_wire_parameter():
	bpy.utils.unregister_class(Rigg_TO_Wire_Parameter)

if __name__ == '__main__':
	register_wire_parameter()
