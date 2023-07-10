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


""" This file can be instaled as an stand alone add-on too """
bl_info = {
	"name": "BsMax-Shapekey",
	"description": "Drive multiple Shapekey (Blender 2.93LTS ~ 3.6LTS)",
	"author": "Matt Ebb | Blaize | Anthony Hunt | Spirou4D | Nevil",
	"version": (0, 1, 0, 2),# 2023-06-11
	"blender": (2, 93, 0),# to 3.6
	"location": "Properties/ Output/ Backbrner",
	"wiki_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"doc_url": "https://github.com/NevilArt/BsMax_2_80/wiki",
	"tracker_url": "https://github.com/NevilArt/BsMax_2_80/issues",
	"category": "Render"
}


import bpy

from bpy.types import Operator

# a-----------v----------b----------v------c
# p = (v-a)/(b-a) if v < b else (c-v)/(c-b) #zerout
# p = (v-a)/(b-a) if v < b else 1 #aditive

class MultiShapeKey:
	def __init__(self, name, value, seprator):
		self.seprator = seprator
		self.name = name
		self.values = [value]

	def append(self, value):
		if not value in self.values:
			self.values.append(value)

	def sort(self):
		self.values.sort()



class Mesh_TO_Shapekeys_Sort_by_name(Operator):
	""" Sort shape key by name order """
	bl_idname = "mesh.shapekeys_sort_by_name"
	bl_label = "Sort By Name"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.object.data.shape_keys
		
	def execute(self, ctx):
		shape_keys = ctx.object.data.shape_keys.key_blocks
		sorted_names = [key.name for key in shape_keys if key.name != 'Basis']
		sorted_names.sort()

		for index, name in enumerate(sorted_names):
			# check is mach with sorted
			if name == shape_keys[index].name:
				continue
			
			# find current place
			current_index = 0
			for i in range(index+1, len(shape_keys)):
				if name == shape_keys[i].name:
					current_index = i
					break
			
			# move each shape key to correct position
			step_count = current_index - index -1
			ctx.object.active_shape_key_index = current_index
			for i in range(step_count):
				bpy.ops.object.shape_key_move(type="UP")		

		return{"FINISHED"}


def has_integer_sufix(string, key):
	""" get underline position """
	index = string.rfind(key)
	""" seprate name from sufix """
	integer = string[index + 1:]
	name = string[:index]
	""" check if sufix integer and in range 0~100 """

	if integer.isdigit():
		val = int(integer)
		if 0 <= val <= 100:
			return name, val

	return None



def remove_shapekey_by_name(obj, shapekey_name):
	key_blocks = obj.data.shape_keys.key_blocks
	obj.active_shape_key_index = key_blocks.keys().index(shapekey_name)
	bpy.ops.object.shape_key_remove()



def get_shapekeys(ctx):
	allowedShapekeys = []
	for n in ctx.object.data.shape_keys.key_blocks:									
		if n.name == 'Basis':
			continue

		if n.name.rfind('_') > 0 or n.name.rfind('=') \
			or n.name.rfind('%') > 0 or n.name.rfind('+') :

			allowedShapekeys.append(n.name)

	return allowedShapekeys



def get_groups_by(shapekeys, key):
	multi_shapekeys = []
	for n in shapekeys:
		ret = has_integer_sufix(n, key)
		if ret != None:
			multi_shapekeys.append(ret)
	return multi_shapekeys


def devide_numeric_shapekeys_to_sub_groups(shapekeys, seprator):
	groups = []
	for sapekey in shapekeys:
		is_new = True
		for group in groups:
			if sapekey[0] == group.name:
				group.append(sapekey[1])
				is_new = False
				break

		if is_new:
			groups.append(MultiShapeKey(sapekey[0], sapekey[1], seprator))
	return groups



def create_multi_shapekey_driver(ctx):
	""" Collect names whit underline """
	shapekeys = get_shapekeys(ctx)

	""" Groupe the shape keys """
	groups = devide_numeric_shapekeys_to_sub_groups(get_groups_by(shapekeys, '_'), '_')
	groups += devide_numeric_shapekeys_to_sub_groups(get_groups_by(shapekeys, '%'), '%')
	groups += devide_numeric_shapekeys_to_sub_groups(get_groups_by(shapekeys, '+'), '+')


	""" remove groups with single value """
	for group in groups:
		if len(group.values) < 2:
			groups.remove(group)

	""" sort all group values """
	for group in groups:
		group.sort()

	""" setup drivers """
	shell =  ctx.object		
	names = [n.name for n in shell.data.shape_keys.key_blocks
										if n.name != 'Basis']

	for group in groups:
		""" Create empty shapekey for driving """
		if not group.name in names:
			shell.shape_key_add(name=group.name, from_mix=False)

		for index, val in enumerate(group.values):
			""" Set up driver to shape keys """
			shape_key = group.name + group.seprator + str(val)
			key_block = shell.data.shape_keys.key_blocks[shape_key]
			key_block.driver_remove('value')
			driver = key_block.driver_add('value')
			driver.driver.type = 'SCRIPTED'

			var = driver.driver.variables.new()
			var.name = 'v'
			var.type = 'SINGLE_PROP'
			target = var.targets[0]
			target.id_type = 'KEY'
			target.id = shell.data.shape_keys
			target.data_path = 'key_blocks["' + group.name + '"].value'

			""" Create driver script """
			# previes shapekey start value
			start = 0 if index == 0 else float(group.values[index-1]) / 100.0
			# current shapkey satrt value
			current = float(val) / 100.0
			# next shapekey satrt value if avalible
			end = float(group.values[index+1]) / 100.0 if index < len(group.values)-1 else None
			# length of a to b
			preLength = current - start
			# length of b to c  
			postLength = end - current if end else 0
			
			start, current = str(start), str(current)
			preLength, postLength = str(preLength), str(postLength)
					
			# keep on 1 previes shapekeys
			if group.seprator == '+':
				if start == '0':
					script = 'v / ' + preLength
				else:
					script = '(v - ' + start + ') / ' + preLength
				
				script += ' if v < ' + current + ' else 1'

			# zero out previes shapekeys
			elif group.seprator in ('_', '%'):
				if start == '0':
					script = 'v / ' + preLength
				else:
					script = '(v - ' + start + ') / ' + preLength
				
				script += ' if ' + start + ' < v <= ' + current + ' else '

				if end:
					end = str(end)
					script += '(' + end +' - v) / ' + postLength
					script += ' if ' + current +' < v <= ' + end + ' else '

				script += '0'
			
			""" apply script to driver """
			driver.driver.expression = script



class Mesh_TO_Create_Multi_Target_Shapekeys(Operator):
	"""Name Sequence Targets like this\n
	target_10\n
	target_25\n
	target_75\n
	The digit are percentage of the each target complet on
	"""
	bl_idname = "mesh.create_multi_target_shapekeys"
	bl_label = "Create Multi Target Shapekeys"
	bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

	@classmethod
	def poll(self, ctx):
		return ctx.object.data.shape_keys
	
	def execute(self, ctx):
		create_multi_shapekey_driver(ctx)
		return{"FINISHED"}



def shapekey_tools(self, ctx):
	if ctx.object.data.shape_keys != None:
		layout = self.layout
		box = layout.box()
		row = box.row()
		row.operator('mesh.create_multi_target_shapekeys')
		row.operator('mesh.shapekeys_sort_by_name')



classes = (
	Mesh_TO_Shapekeys_Sort_by_name,
	Mesh_TO_Create_Multi_Target_Shapekeys
)



def register_shapekey():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.DATA_PT_shape_keys.append(shapekey_tools)



def unregister_shapekey():
	bpy.types.DATA_PT_shape_keys.remove(shapekey_tools)
	for c in classes:
		bpy.utils.unregister_class(c)



def register():
	register_shapekey()



def unregister():
	unregister_shapekey()



if __name__ == "__main__":
	register_shapekey()