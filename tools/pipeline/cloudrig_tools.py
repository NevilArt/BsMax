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

def add_bone_collection(armature_obj, collection_name):
	"""
	Adds a Bone Collection with the given name to the armature object
	and moves it to the top of the collection list.
	If a collection with that name already exists, returns it as is.
	"""
	collections = armature_obj.data.collections

	existing = collections.get(collection_name)
	if existing:
		return existing

	new_coll = collections.new(name=collection_name)
	collections.move(new_coll.index, 0)
	return new_coll

def add_bones_to_collection(bone_names, collection_name):
	"""
	Assigns the given bones (by name) to a Bone Collection (by name)
	on the active armature.
	"""
	armature = bpy.context.object.data
	bone_collection = armature.collections.get(collection_name)

	for bone_name in bone_names:
		bone = armature.bones.get(bone_name)
		if bone:
			bone_collection.assign(bone)

def get_bone_names():
	return (
		"root", "Properties_Character_Human",
		"P-STR-Head1",
		"FK-Head", "FK-Neck",
		"CHST-Spine", "TORSO-Spine",
		"FK-Shoulder.L", "FK-Shoulder.R",
		"FK-UpperArm.L", "FK-UpperArm.R",
		"FK-Forearm.L", "FK-Forearm.R",
		"FK-Hand.L", "FK-Hand.R",
		"POLE-Arm.L", "POLE-Arm.R",
		"IK-Hand.L", "IK-Hand.R",
		"IK-Foot.L", "IK-Foot.R",
		"POLE-Leg.L", "POLE-Leg.R",
		"ROLL-M-Foot.L", "ROLL-M-Foot.R",
		"FK-Toes.L", "FK-Toes.R"
	)

class CLOUDRIG_OT_basic_setup(Operator):
	"""Cloudrig Basic Setup"""
	bl_idname = "cloudrig.basic_setup"
	bl_label = "Cloudrig Basic Setup"
	bl_options = {'REGISTER', 'UNDO'}
 
	@classmethod
	def poll(cls, context):
		if not context.object:
			return False
		return context.active_object.type == 'ARMATURE'
 
	def execute(self, context):
		armature_obj = context.object
		add_bone_collection(armature_obj, "Custom")
		add_bones_to_collection(get_bone_names(), "Custom")
		return {'FINISHED'}


classes = (
	CLOUDRIG_OT_basic_setup,
)

def register_cloudrig_tools():
	for cls in classes:
		bpy.utils.register_class(cls)
 
def unregister_cloudrig_tools():
	for cls in classes:
		bpy.utils.unregister_class(cls)
 
if __name__ == "__main__":
	register_cloudrig_tools()