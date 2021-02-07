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
from bpy.types import Operator, Panel
# a-----------v----------b----------v------c
# p = (v-a)/(b-a) if v < b else (c-v)/(c-b)

class MultiShapeKey:
	def __init__(self, name, value):
		self.name = name
		self.values = [value]
	def append(self, value):
		if not value in self.values:
			self.values.append(value)
	def sort(self):
		self.values.sort()



class Mesh_TO_Shapekeys_Sort_by_name(Operator):
	bl_idname = "mesh.shapekeys_sort_by_name"
	bl_label = "Sort By Name"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	@classmethod
	def poll(self, ctx):
		return False
	
	def execute(self,ctx):
		return{"FINISHED"}



class Mesh_TO_Create_Multi_Target_Shapekeys(Operator):
	"""Name Sequence Targets like this\ntarget_10\ntarget_25\ntarget_75\nThe digit are percentage of the each target complet on"""
	bl_idname = "mesh.create_multi_target_shapekeys"
	bl_label = "Create Multi Target Shapekeys"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.object.data.shape_keys != None

	def has_integer_sufix(self, string):
		""" get underline position """
		index = string.rfind('_')
		""" seprate name from sufix """
		integer = string[index+1:]
		name = string[:index]
		""" check if sufix integer and in range 0~100 """
		if integer.isdigit():
			val = int(integer)
			if 0 <= val <= 100:
				return name, val
		return None
	
	def remove_shapekey_by_name(self, obj, shapekey_name):
		obj.active_shape_key_index = obj.data.shape_keys.key_blocks.keys().index(shapekey_name)
		bpy.ops.object.shape_key_remove()

	def execute(self,ctx):
		""" Collect names whit underline """
		shapekeys = [n.name for n in ctx.object.data.shape_keys.key_blocks if n.name != 'Basis' and n.name.rfind('_') != -1]
	
		""" Filter names with integer end """
		multi_shapekeys = []
		for n in shapekeys:
			ret = self.has_integer_sufix(n)
			if ret != None:
				multi_shapekeys.append(ret)
	
		""" Groupe the shape keys """
		groups = []
		for sapekey in multi_shapekeys:
			is_new = True
			for group in groups:
				if sapekey[0] == group.name:
					group.append(sapekey[1])
					is_new = False
					break
			if is_new:
				groups.append(MultiShapeKey(sapekey[0], sapekey[1]))
	
		""" remove groups with single value """
		for group in groups:
			if len(group.values) < 2:
				groups.remove(group)
	
		""" sort all group values """
		for group in groups:
			group.sort()
	
		""" setup drivers """
		shell =  ctx.object
		names = [n.name for n in shell.data.shape_keys.key_blocks if n.name != 'Basis']
		for group in groups:
			""" Create empty shapekey for driving """
			if not group.name in names:
				shell.shape_key_add(name=group.name, from_mix=False)

			for index, val in enumerate(group.values):
				""" Set up driver to shape keys """
				shape_key = group.name + '_' + str(val)
				key_block = shell.data.shape_keys.key_blocks[shape_key]
				key_block.driver_remove('value')
				driver = key_block.driver_add('value')
				driver.driver.type = 'SCRIPTED'

				var = driver.driver.variables.new()
				var.name = 'v'
				var.type = 'SINGLE_PROP'
				target = var.targets[0]
				target.id = shell
				target.data_path = 'data.shape_keys.key_blocks["' + group.name + '"].value'

				""" Create driver script """
				a = 0 if index == 0 else float(group.values[index-1]) / 100.0
				b = float(val) / 100.0
				c = float(group.values[index+1]) / 100.0 if index < len(group.values)-1 else None
				l1 = b - a
				l2 = c - b if c else 0
				a, b, l1, l2 = str(a), str(b), str(l1), str(l2)
			
				if a == '0':
					script = 'v / ' + l1
				else:
					script = '(v - ' + a + ') / ' + l1
				script += ' if ' + a + ' < v <= ' + b + ' else '
				if c:
					c = str(c)
					script += '(' + c +' - v) / ' + l2
					script += ' if ' + b +' < v <= ' + c + ' else '
					script += '0'
				else:
					script += '0'
				
				""" apply script to driver """
				driver.driver.expression = script
		return{"FINISHED"}

def shapekey_tools(self, ctx):
	if ctx.object.data.shape_keys != None:
		layout = self.layout
		box = layout.box()
		row = box.row()
		row.operator('mesh.create_multi_target_shapekeys')
		row.operator('mesh.shapekeys_sort_by_name')

classes = [Mesh_TO_Shapekeys_Sort_by_name, Mesh_TO_Create_Multi_Target_Shapekeys]

def register_shapekey():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.DATA_PT_shape_keys.append(shapekey_tools)

def unregister_shapekey():
	bpy.types.DATA_PT_shape_keys.remove(shapekey_tools)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_shapekey()