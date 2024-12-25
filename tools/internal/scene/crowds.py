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
# 2024/06/04

import bpy

from random import random, randint

from bpy.types import Operator, Menu
from bpy.props import EnumProperty, IntProperty, FloatProperty
from bpy.utils import register_class, unregister_class

from bpy.app import version


def get_digits(string):
	""" get string and return digits from end of string\n
		digits aftyer . that added by blender automatic renaming will ignore\n
		args :
			String: String value
		return:
			string of  last digits or None
	"""
	# Remove After dot part
	string = string.split('.')[0]

	# igonre empty strings
	if not string:
		return

	# drop not end with digit
	if not string[-1] in "0123456789":
		return

	length = 0
	for index in range(len(string)-1, -1, -1):
		if string[index] in "0123456789":
			length += 1
		else:
			break

	return string[-length:]


def get_modifier(obj, modifierClass):
	""" Find and return given modifier from object list """
	for modifier in obj.modifiers:
		if modifier.type == modifierClass:
			return modifier
	return None


def get_constraint(obj, constriantClass):
	""" Fing and return constriant by given type """
	for constraint in obj.constraints:
		if constraint.type == constriantClass:
			return constraint
	return None


def clear_collections(obj):
	""" clear all linked collection of given object """
	for collection in obj.users_collection:
		collection.objects.unlink(obj)


def get_selected_collections(ctx):
	""" Most return all selected collection\n
		But currentrly it is not possible and\n
		This function returns collections under the active one
	"""
	# Temprary solution
	return ctx.collection.children


def get_collection_parent(collection):
	""" return parent of  given collection """
	for col in bpy.data.collections:
		for child in col.children:
			if collection == child:
				return col
	return None


def clone_objects_to_new_collection(ctx, objs, parent, name):
	# Clone the collection
	newCollection = bpy.data.collections.new(name)
	if parent:
		parent.children.link(newCollection)

	# Clone objects and put in new collection
	bpy.ops.object.select_all(action='DESELECT')
	for obj in objs:
		obj.select_set(True)
	bpy.ops.object.duplicate(linked=True, mode='INIT')
	newObjs = ctx.selected_objects
	
	# Link new objects to newcollection
	for obj in newObjs:
		clear_collections(obj)
		newCollection.objects.link(obj)

	return newObjs


def collect_alembic_containers(objs):
	# Collect modifiers with Alembic file and abc cache files
	abcs, containers = [], []
	for obj in objs:
		abcModifier = get_modifier(obj, 'MESH_SEQUENCE_CACHE')
		if abcModifier:
			containers.append(abcModifier)

			abs = abcModifier.cache_file
			if not abs in abcs:
				abcs.append(abs)

		absConstraint = get_constraint(obj, 'TRANSFORM_CACHE')
		if absConstraint:
			containers.append(absConstraint)
			
			abc = absConstraint.cache_file
			if not abc in abcs:
				abcs.append(abc)

	return abcs, containers


def loop_offset_abc(abcs, length, start, speed):
	for abc in abcs:
		abc.override_frame = True
		abc.frame = 0

		#(frame * speed - start) % length
		script = "(frame * " + str(speed) + " + " + str(start) + ")"
		script += " % " + str(length)

		abc.driver_remove('frame')
		abcDriver = abc.driver_add('frame')
		abcDriver.driver.type = 'SCRIPTED'
		abcDriver.driver.expression = script


def random_loop_abcs(abcs, length, startVar=1, speedVar=0.1):
	""" loop ABC modifier and randomize speed and start time\n
		args:
			abc: cahce file of mesh sequense modifier
			length: length of alembic cache animation
			startVar: 0 no variation 1 full lenght variation
			speedVar: 0 no variation 1 double speed\n
		return:
			None
	"""
	newStart = randint(0, length*startVar)
	speedFactor = 1 + round(random()*speedVar, 3)

	loop_offset_abc(abcs, length, newStart, speedFactor)


def make_unique_abc_groupe(abcs, containers):
	for abc in abcs:
		shared = []
		# Collect Modifiers with same abc
		for container in containers:
			if container.cache_file == abc:
				shared.append(container)

		# Make a unique copy of abc
		newAbc = abc.copy()

		# Replace with others
		for container in containers:
			container.cache_file = newAbc


def clone_collection_abc(self, ctx):
	collection = ctx.collection
	if not collection:
		return

	parent = get_collection_parent(collection)
	objects = [obj for obj in collection.objects]

	for _ in range(self.count):
		newObjs = clone_objects_to_new_collection(
			ctx, objects, parent, collection.name
		)

		abcs, containers = collect_alembic_containers(newObjs)
		make_unique_abc_groupe(abcs, containers)
		random_loop_abcs(abcs, self.length, 1, self.speedVariation)


def clone_object_abc(self, ctx):
	abcModifier = get_modifier(ctx.object, 'MESH_SEQUENCE_CACHE')
	if not abcModifier:
		return
	
	random_loop_abcs([abcModifier.cache_file], self.length, 0, 0)

	collection = ctx.object.users_collection[0]
	for _ in range(self.count):
		newObj= ctx.object.copy()
		# newObj.name = ""

		newAbc = abcModifier.cache_file.copy()
		random_loop_abcs([newAbc], self.length , 1, 0.1)
		# newAbc.name = ""

		newModifier = get_modifier(newObj, 'MESH_SEQUENCE_CACHE')
		# newModifier.name = ""

		newModifier.cache_file = newAbc
		
		collection.objects.link(newObj)


def random_abc_by_objects(self, objs):
	for obj in objs:
		modifier = get_modifier(obj, 'MESH_SEQUENCE_CACHE')
		if modifier:
			random_loop_abcs(
				[modifier.cache_file],
				self.length,
				startVar= self.startVariation,
				speedVar= self.speedVariation
			)


def random_abc_by_collection(self, collections):
	for collection in collections:
		abcs, containers = collect_alembic_containers(collection.objects)
		random_loop_abcs(abcs, self.length, 1, self.speedVariation)


def clone_refrences(self, ctx):
	""" pick the clone method function """
	if self.target == 'COLLECTION':
		# TODO is active collection

		if self.method == 'ABC':
			clone_collection_abc(self, ctx)

	if self.target == 'OBJECT':
		if not ctx.object:
			return

		if self.method == 'ABC':
			clone_object_abc(self, ctx)


def random_and_loop_refrenses(self, ctx):
	if self.target == 'COLLECTION':
		if self.method == 'ABC':
			selected_collections = get_selected_collections(ctx)
			random_abc_by_collection(self, selected_collections)

	elif self.target == 'OBJECT':
		if self.method == 'ABC':
			random_abc_by_objects(self, ctx.selected_objects)


def has_name_end_zero(objs):
	for obj in objs:
		digit = get_digits(obj.name)
		if int(digit) == 0:
			return True

	return False


def unhide_stuff(objs):
	for obj in objs:
		obj.hide_viewport = False
		obj.hide_render = False


def delete_hide_stuff(objs):
	for obj in objs:
		if obj.hide_viewport and obj.hide_render:
			bpy.data.objects.remove(obj, do_unlink=True)


def shuffle_hide_stuff(objs):
	groupDic = {} #{name:[obj1, obj2]}
	for obj in objs:
		name = obj.name.split('.')[0] # Remove after dot
		digit = get_digits(name)
		if digit:
			pureName = name[:-len(digit)]
			# add or create group
			if pureName in groupDic.keys():
				groupDic[pureName].append(obj)
			else:
				groupDic[pureName] = [obj]
	
	for objGroup in groupDic.values():
		maxVal = len(objGroup)-1
		
		# if has a zero ended num add more to has chanse of hide all
		if has_name_end_zero(objGroup):
			maxVal += 1

		chosenOne = randint(0, maxVal)

		for index, obj in enumerate(objGroup):
			state = index != chosenOne
			obj.hide_viewport = state
			obj.hide_render = state


def stuff_variation(self, ctx):
	selected_collections = get_selected_collections(ctx)
	if self.method == 'HIDE':
		for collection in selected_collections:
			shuffle_hide_stuff(collection.objects)

	elif self.method == 'UNHIDE':
		for collection in selected_collections:
			unhide_stuff(collection.objects)

	elif self.method == 'DELETE':
		for collection in selected_collections:
			delete_hide_stuff(collection.objects)


class Crowds_TO_Clone_Refrenses(Operator):
	bl_idname = 'crowds.clone_refrenses'
	bl_label = "Clone Refrences (Crowds)"
	bl_options = {'REGISTER', 'UNDO'}

	target: EnumProperty(
		items=[
			(
				'COLLECTION',
				"Collection",
				"Clone active collection if contain object with Alembic"
			),
			(
				'OBJECT',
				"Object",
				"Clone active object if contain Alembic data"
			)
		],
		default = 'COLLECTION'
	) # type: ignore

	method: EnumProperty(
		items=[
			(
				'ABC',
				"Alembic",
				"Use Alembic clone and loop method"
			)
		],
		default='ABC'
	) # type: ignore

	count: IntProperty(
		default=3, min=0,
		description="Number if clones want to create"
	) # type: ignore

	length: IntProperty(
		default=100, min=1,
		description="Length of Alembic cache file"
	) # type: ignore

	speedVariation: FloatProperty(
		default=0.1, min=0,
		description="Variation of Alembic play faster 0 => 1x speed"
	) # type: ignore
	
	# @classmethod
	# def poll(self, ctx):
	# 	if ctx.area.type == 'VIEW_3D':
	# 		return ctx.active_object
	# 	return False

	def draw(self, _):
		layout = self.layout
		layout.prop(self, 'target')
		layout.prop(self, 'method')
		layout.prop(self, 'count')
		layout.prop(self, 'length')
		layout.prop(self, 'speedVariation')
	
	def execute(self, ctx):
		clone_refrences(self, ctx)
		return{'FINISHED'}

	def invoke(self, ctx, _):
		return ctx.window_manager.invoke_props_dialog(self)


class Crowds_TO_Loop_Refrenses(Operator):
	bl_idname = 'crowds.loop_refrenses'
	bl_label = "Loop Refrences (Crowds)"
	bl_options = {'REGISTER', 'UNDO'}

	target: EnumProperty(
		items=[
			(
				'COLLECTION',
				"Collection",
				"Loop and random time offset grouped collection children"
			),
			(
				'OBJECT',
				"Object",
				"Loop and random time offset selected objects sepratly"
			)
		],
		default = 'COLLECTION'
	) # type: ignore

	method: EnumProperty(
		items=[('ABC', "Alembic", "Alembic")],
		default='ABC'
	) # type: ignore

	length: IntProperty(
		default=100, min=1,
		description=""
	) # type: ignore
	
	startVariation: FloatProperty(
		default=1, min=0,
		description=""
	) # type: ignore
	
	speedVariation: FloatProperty(
		default=0.1, min=0,
		description=""
	) # type: ignore

	# @classmethod
	# def poll(self, ctx):
	# 	if ctx.area.type == 'VIEW_3D':
	# 		return ctx.active_object
	# 	return False

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'target')
		layout.prop(self, 'method')
		layout.prop(self, 'length')
		layout.prop(self, 'startVariation')
		layout.prop(self, 'speedVariation')
	
	def execute(self, ctx):
		random_and_loop_refrenses(self, ctx)
		return{'FINISHED'}

	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self)


class Crowds_TO_Stuff_Variation(Operator):
	bl_idname = 'crowds.stuff_variation'
	bl_label = "Stuff Variation (Crowds)"
	bl_options = {'REGISTER', 'UNDO'}

	method: EnumProperty(
		items=[
			(
				'HIDE',
				"Hide",
				"Randomly hide unhide parts of sub collection"
			),
			(
				'UNHIDE',
				"Unhide",
				"Unhide all objects under active colection"
			),
			(
				'DELETE',
				"Delete",
				"Delete all hiden object under active colection children"
			)
		],
		default='HIDE'
	) # type: ignore

	# @classmethod
	# def poll(self, ctx):
	# 	if ctx.area.type == 'VIEW_3D':
	# 		return ctx.mode == 'OBJECT'

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'method')
	
	def execute(self, ctx):
		stuff_variation(self, ctx)
		return{'FINISHED'}

	def invoke(self, ctx, event):
		return ctx.window_manager.invoke_props_dialog(self)


class BsMax_MT_Crowds_Tools(Menu):
	bl_idname = 'BSMAX_MT_crowdstools'
	bl_label = "Crowds"
	bl_description = ""
	# bl_context = 'objectmode'

	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'

	def draw(self, ctx):
		layout=self.layout
		icon='LIGHTPROBE_GRID' if version < (4, 1, 0) else 'LIGHTPROBE_VOLUME'
		layout.operator(
			'crowds.clone_refrenses',
			text="Clone Instanses",
			icon=icon
		)

		layout.operator(
			'crowds.loop_refrenses',
			text="Loop Instanses",
			icon='ORIENTATION_GIMBAL'
		)

		layout.operator(
			'crowds.stuff_variation',
			text="Variate Instanses",
			icon='GEOMETRY_NODES'
		)


def crowds_menu(self, _):
	self.layout.menu('BSMAX_MT_crowdstools', icon='COMMUNITY')


classes = {
	Crowds_TO_Clone_Refrenses,
	Crowds_TO_Loop_Refrenses,
	Crowds_TO_Stuff_Variation,
	BsMax_MT_Crowds_Tools
}


def register_crowds():
	for cls in classes:
		register_class(cls)
	
	bpy.types.BSMAX_MT_view3d_tools.append(crowds_menu)


def unregister_crowds():
	bpy.types.BSMAX_MT_view3d_tools.remove(crowds_menu)

	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_crowds()