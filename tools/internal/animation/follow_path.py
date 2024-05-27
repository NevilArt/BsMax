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
# 2024/05/26

import bpy

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy.props import BoolProperty, EnumProperty


class FollowerData:
	def __init__(self):
		self.owner = None
		self.path = None
		self.floor = []
		self.bones = []
		self.iks = []
	
	def reset(self):
		self.owner = None
		self.path = None
		self.floor = []
		self.bones = []
		self.iks = []
	
followre_data = FollowerData()


def get_parts(cls, ctx):
	global followre_data
	if cls.type == 'PATH':
		if ctx.object.type == 'CURVE':
			followre_data.path = ctx.object

	if cls.typee == 'FLOOR':
		pass

	if cls.type == 'IKS':
		pass

	if cls.type == 'BONES':
		pass


class Anim_OT_Follower_pick(Operator):
	bl_idname = 'anim.followr_part_pickre'
	bl_label = 'Follower Parts Pickr'
	bl_options = {'REGISTER', 'UNDO'}

	type: EnumProperty(
		name="",
		items=[
			('PATH', "Path", "Curve Object as following path"),
			('FLOOR', "Ground", "Get as touching surface"),
			('IKS', "IKs", "get selected IK bons for feet on ground"),
			('BONES', "Bonees", "Get selected bone has take effect")
		],
		default="",
		description=""
	) # type: ignore

	@classmethod
	def poll(self, ctx):
		True
	
	def execute(self, ctx):
		get_parts(self, ctx)
		return{'FINISHED'}


classes ={
	Anim_OT_Follower_pick
}

def register_fallow_path():
	for cls in classes:
		register_class(cls)


def unregister_follow_path():
	for cls in classes:
		unregister_class(cls)


if __name__ == '__main__':
	register_fallow_path()