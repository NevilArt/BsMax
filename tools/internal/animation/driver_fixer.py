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

from bpy.props import BoolProperty

class Anim_TO_Driver_Fixer(Operator):
	""" Solve overide library issue with drivers """
	bl_idname = "anim.driver_fixer"
	bl_label = "Driver Fixer"

	shapekey: BoolProperty(name='Shapekey', default=True)

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			return len(ctx.selected_objects) > 0
		return False

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'shapekey')
	
	def get_driver(self, obj, name):
		for driver in obj.data.shape_keys.animation_data.drivers:
			if driver.data_path[12: -8] == name:
				return driver.driver
		return None

	def fix_shapekey_drivers(self, obj):
		if obj.data.shape_keys:
			names = [n.name for n in obj.data.shape_keys.key_blocks if n.name != 'Basis']
			for name in names:
				# shapekey = obj.data.shape_keys.key_blocks[name]
				driver = self.get_driver(obj, name)
				if driver:
					for var in driver.variables:
						for target in var.targets:
							name = target.id.name
							target.id = bpy.data.objects[name]
						var.targets.update()

	def execute(self, ctx):
		for obj in ctx.selected_objects:
			if obj.type in {'MESH','CURVE'}:
				if self.shapekey:
					self.fix_shapekey_drivers(obj)
			
		return{"FINISHED"}

	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self, width=200)

classes = [Anim_TO_Driver_Fixer]

def register_driver_fixer():
	[bpy.utils.register_class(c) for c in classes]

def unregister_driver_fixer():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_driver_fixer()