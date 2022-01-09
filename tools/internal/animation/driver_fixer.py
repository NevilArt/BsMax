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

class Driver_Reconnect:
	def get_shapekey_driver(self, obj, name):
		if hasattr(obj.data.shape_keys.animation_data, 'drivers'):
			for driver in obj.data.shape_keys.animation_data.drivers:
				if driver.data_path[12: -8] == name:
					return driver.driver
		return None
	
	def fix_driver(self, driver):
		if driver:
			for var in driver.variables:
				for target in var.targets:
					if target.id:
						name = target.id.name
						# print(">>>>", target.id.type)
						if target.id.type == 'MESH':
							if name in bpy.data.objects:
								target.id = bpy.data.objects[name]
						
						elif target.id.type == 'PERSP':
							if name in bpy.data.cameras:
								target.id = bpy.data.cameras[name]
						
						elif target.id.type in {'POINT', 'SUN', 'SPOT'}:
							if name in bpy.data.lights:
								target.id = bpy.data.lights[name]
						#TODO add all other types
						
				var.targets.update()

	def fix_shapekey(self, obj):
		if hasattr(obj.data.shape_keys, 'key_blocks'):
			names = [n.name for n in obj.data.shape_keys.key_blocks if n.name != 'Basis']
			for name in names:
				driver = self.get_shapekey_driver(obj, name)
				try:
					self.fix_driver(driver)
				except:
					pass

	def update(self):
		for obj in bpy.data.objects:
			if obj.animation_data:
				for driver in obj.animation_data.drivers:
					self.fix_driver(driver.driver)
		for obj in bpy.data.objects:
			if obj.type in {'MESH','CURVE'}:
				self.fix_shapekey(obj)
	

class Anim_TO_Driver_Fixer(Operator):
	""" Solve overide library issue with drivers """
	bl_idname = "anim.driver_fixer"
	bl_label = "Driver Fixer"

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		dr = Driver_Reconnect()
		dr.update()
		return{"FINISHED"}

def register_driver_fixer():
	bpy.utils.register_class(Anim_TO_Driver_Fixer)

def unregister_driver_fixer():
	bpy.utils.unregister_class(Anim_TO_Driver_Fixer)

if __name__ == "__main__":
	register_driver_fixer()