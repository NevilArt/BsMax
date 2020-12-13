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
from bpy.props import BoolProperty, EnumProperty

class Pose_OT_Select_Hierarchy_Plus(Operator):
	bl_idname = "pose.select_hierarchy_plus"
	bl_label = "Select Hierarchy (Plus)"
	bl_description = ""
	bl_options = {'REGISTER', 'UNDO'}
	
	full: BoolProperty(default=False)
	extend: BoolProperty(default=False)
	direction: EnumProperty(name='Direction', items=[('PARENT','Parent',''),('CHILDREN','Children','')], default='CHILDREN')

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
		
		if self.direction == 'CHILDREN':
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
					if not self.extend:
						bone.select = False
		
		elif self.direction == 'PARENT':
			child_less = []
			for bone in selected:
				if len(bone.children) == 0:
					child_less.append(bone)
				if bone.parent != None:
					bone.parent.select = True
				if not self.extend:
					bone.select = False
			if not self.extend:
				for bone in child_less:
					bone.select = False

		self.report({'OPERATOR'},'bpy.ops.pose.select_hierarchy_plus()')
		return{"FINISHED"}

def register_pose():
	bpy.utils.register_class(Pose_OT_Select_Hierarchy_Plus)

def unregister_pose():
	bpy.utils.unregister_class(Pose_OT_Select_Hierarchy_Plus)

if __name__ == "__main__":
	register_pose()