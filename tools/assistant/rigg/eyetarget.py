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
from mathutils import Vector
from bsmax.math import get_distance
from bsmax.actions import link_to,set_create_target,freeze_transform
from primitive.rectangle import Rectangle

def create_rectangle(ctx, location, width, length):
	rec = Rectangle()
	rec.create(ctx)
	rec.data.primitivedata.width = width
	rec.data.primitivedata.length = length
	rec.data.primitivedata.chamfer1 = length*0.45
	#rec.owner.delta_rotation_euler = Vector(rec.owner.delta_rotation_euler) + Vector((1.5708,0,0))
	rec.owner.rotation_euler = Vector(rec.owner.rotation_euler) + Vector((1.5708,0,0))
	rec.owner.location = location
	return rec.owner

def create_target(ctx, location, radius, frame):
	bpy.ops.object.empty_add(type='CIRCLE', location=location)
	targ = ctx.active_object
	targ.empty_display_size = radius
	link_to(targ, frame)
	return targ

def create_holder(ctx, location, radius, target):
	bpy.ops.object.empty_add(type='CUBE',location=location)
	holder = ctx.active_object
	holder.empty_display_size = radius
	set_create_target(holder, target)
	return holder

class BsMax_TO_EyeTargetCreator(Operator):
	bl_idname = "bsmax.eyetargetcreator"
	bl_label = "Eye Target Creator"
	bl_description = "Create Eyetarget For 2 Selected Objects"

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.selected_objects) == 2:
				return True
		return False

	def execute(self, ctx):
		objs = ctx.selected_objects

		if objs[0].location.x > objs[1].location.x:
			eyel,eyer = objs[0],objs[1]
		else:
			eyel,eyer = objs[1],objs[0]

		diml,dimr = eyel.dimensions,eyer.dimensions
		radl,radr = (diml.x*diml.y)/4,(dimr.x*dimr.y)/4
		radius = max(radl,radr)
		border = radius/8
		length = radius*2+border
		distance = get_distance(eyel.location,eyer.location)
		width = distance+radius*2+border
		location = (eyer.location + eyel.location) / 2
		frame = create_rectangle(ctx, location, width, length)
		frame.name = "eye_target_frame"
		targl = create_target(ctx, eyel.location, radl, frame)
		targl.name = "eye_target_L"
		targr = create_target(ctx, eyer.location, radr, frame)
		targr.name = "eye_target_R"
		freeze_transform([targl,targr])
		frame.location.y = -radius * 5
		holderl = create_holder(ctx, eyel.location, radius, targl)
		holderl.name = "eye_parent_L"
		holderr = create_holder(ctx, eyer.location, radius, targr)
		holderr.name = "eye_parent_R"
		# temprary solution
		#link_to(eyel, holderl)
		#link_to(eyer, holderr)
		bpy.ops.object.select_all(action='DESELECT')
		eyel.select_set(True)
		holderl.select_set(True)
		ctx.view_layer.objects.active = holderl
		bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
		bpy.ops.object.select_all(action='DESELECT')
		eyer.select_set(True)
		holderr.select_set(True)
		ctx.view_layer.objects.active = holderr
		bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
		return {"FINISHED"}

def register_eyetarget():
	bpy.utils.register_class(BsMax_TO_EyeTargetCreator)

def unregister_eyetarget():
	bpy.utils.unregister_class(BsMax_TO_EyeTargetCreator)