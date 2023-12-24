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
import os

from math import radians
from bpy.types import Operator



def clear_terminal():
	if os.name == "nt":
		os.system("cls") 
		return
	os.system("clear") 



class MDF:
	def __init__(self, width, length):
		self.width = width
		self.length = length
		self.front = False
		self.back = False
		self.left = False
		self.right = False
		self.count = 1
		self.owners = []
	
	def set_band(self, front, back, left, right):
		self.front = front
		self.back = back
		self.left = left
		self.right = right
	
	def get_width_band_count(self):
		count = 0
		if self.front:
			count += 1
		if self.back:
			count += 1
		return count
	
	def combine_owner(self, names):
		for name in names:
			if not name in self.owners:
				self.owners.append(name)
	
	def get_length_band_count(self):
		count = 0
		if self.left:
			count += 1
		if self.right:
			count += 1
		return count
	
	def to_string(self):
		string = str(self.width)
		string += " x "
		string += str(self.length)
		string += " * " + str(self.count)
		string += " ["
		if self.front:
			string += "F"
		if self.back:
			string += "B"
		if self.left:
			string += "L"
		if self.right:
			string += "R"
		string += "] "
		for owner in self.owners:
			string += owner + ","
		return string
	
	def get_swaped_copy(self):
		newMdf = MDF(self.length, self.width)
		newMdf.front = self.left
		newMdf.left = self.back
		newMdf.back = self.right
		newMdf.right = self.front
		return newMdf
	
	def auto_align(self):
		if self.length > self.width:
			newMdf = self.get_swaped_copy()
			self.width = newMdf.width
			self.length = newMdf.length
			self.front = newMdf.front
			self.back = newMdf.back
			self.left = newMdf.left
			self.right = newMdf.right
	
	def compar(self, target):
		acceptable = False

		if self.width == target.width and self.length == target.length:
			acceptable = True

		if self.width == target.length and self.length == target.width:
			acceptable = True
			target = target.get_swaped_copy()

		if not acceptable:
			return False
		
		if self.get_width_band_count() != target.get_width_band_count():
			return False
		
		if self.get_length_band_count() != target.get_length_band_count():
			return False
		
		return True



def conver_to_unit(ctx, length):
	length_unit = ctx.scene.unit_settings.length_unit
	if length_unit == 'CENTIMETERS':
		return round(length*100, 2)



def get_instanses(obj):
	return [target for target in bpy.data.objects if obj.data == target.data]



def corect_rotations(ctx, objs):
	bpy.ops.object.select_all(action='DESELECT')
	
	for obj in objs:
		if obj.data.primitivedata['classname'] != 'Plane':
			continue

		instanses = get_instanses(obj)

		width = float(obj.data.primitivedata.width)
		length = float(obj.data.primitivedata.length)

		if length > width:
			# swap size
			obj.data.primitivedata.width = length
			obj.data.primitivedata.length = width

			# rotate
			for inst in instanses:
				inst.select_set(True)
				ctx.view_layer.objects.active = inst
				inst.rotation_euler.rotate_axis("Z", radians(90))
				inst.select_set(False)



def get_node_modifier(obj):
	for modifier in obj.modifiers:
		if modifier.type == 'NODES':
			return modifier
	return None



def get_mdf_side_bands(nodes, mdf):
	if not nodes:
		return

	items_tree = nodes.node_group.interface.items_tree
	if 'Front' in items_tree:
		if nodes[items_tree['Front'].identifier]:
			mdf.front = True

	if 'Back' in items_tree:
		if nodes[items_tree['Back'].identifier]:
			mdf.back = True
	
	if 'Left' in items_tree:
		if nodes[items_tree['Left'].identifier]:
			mdf.left = True
	
	if 'Right' in items_tree:
		if nodes[items_tree['Right'].identifier]:
			mdf.right = True



def mdf_sort(mdfList):
	newList, widthList = [], []
	for mdf in mdfList:
		if not mdf.width in widthList:
			widthList.append(mdf.width)
	widthList.sort(reverse=True)
	for width in widthList:
		for mdf in reversed(mdfList):
			if mdf.width >= width:
				newList.append(mdf)
				mdfList.remove(mdf)
	return newList



def get_owners(obj):
	return [col.name for col in obj.users_collection]
	


def mdf_print(ctx):
	partList = []
	for mdf in ctx.selected_objects:
		if mdf.data.primitivedata['classname'] != 'Plane':
			continue
		
		width = float(mdf.data.primitivedata.width)
		length = float(mdf.data.primitivedata.length)

		width = conver_to_unit(ctx, width)
		length = conver_to_unit(ctx, length)

		newMdfPart = MDF(width, length)
		newMdfPart.auto_align()
		newMdfPart.owners = get_owners(mdf)

		geoNodes = get_node_modifier(mdf)
		get_mdf_side_bands(geoNodes, newMdfPart)

		partList.append(newMdfPart)
		
	if not partList:
		return

	printList = []
	while partList:
		part = partList[0]
		partList.remove(part)

		for mdf in reversed(partList):
			if part.compar(mdf):
				part.count += 1
				partList.remove(mdf)
				part.combine_owner(mdf.owners)

		printList.append(part)
	
	printList = mdf_sort(printList)

	clear_terminal()
	for part in printList:
		print(part.to_string())
		print("")



class Object_OT_MDF_Correct_Rotation(Operator):
	bl_idname="mdf.correct_direction"
	bl_label="MDF Correct Direction"
	
	def execute(self, ctx):
		selection = ctx.selected_objects.copy()
		corect_rotations(ctx, ctx.selected_objects)
		for obj in selection:
			obj.select_set(True)
		return {"FINISHED"}



class Object_OT_MDF_Print(Operator):
	bl_idname="mdf.print"
	bl_label="MDF Print"
	
	def execute(self, ctx):
		mdf_print(ctx)
		return {"FINISHED"}
	


classes = (
	Object_OT_MDF_Correct_Rotation,
	Object_OT_MDF_Print
)


def register_mdf():
	for c in classes:
		bpy.utils.register_class(c)



def unregister_mdf():
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == "__main__":
	register_mdf()
