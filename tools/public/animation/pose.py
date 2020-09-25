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

class Pose_OT_Select_Children(Operator):
	bl_idname = "pose.select_children"
	bl_label = "Select Children"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	full: BoolProperty()
	extend: BoolProperty()

	@classmethod
	def poll(self, ctx):
		return True

	def get_selected_bones(self, armature):
		return [bone for bone in armature.data.bones if bone.select]
	
	def collect_children(self, bones):
		children = []
		for bone in bones:
			for child in bone.children:
				if not child.select:
					children.append(child)
					child.select = True
		return children
	
	def execute(self, ctx):
		rigg = ctx.active_object
		selected = self.get_selected_bones(rigg)
		nsc = len(selected) # New Selected Count
		if self.full == True:
			children = selected
			while nsc != 0:
				children = self.collect_children(children)
				nsc = len(children)
		else:
			for bone in selected:
				for child in bone.children:
					child.select = True
		self.report({'INFO'},'bpy.ops.pose.select_children()')
		return{"FINISHED"}

def register_pose():
	bpy.utils.register_class(Pose_OT_Select_Children)

def unregister_pose():
	bpy.utils.unregister_class(Pose_OT_Select_Children)

if __name__ == "__main__":
	register_pose()