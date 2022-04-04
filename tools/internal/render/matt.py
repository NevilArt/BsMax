############################################################################
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

# this operator is just for test maybe change or remove in future

import bpy
from bpy.types import Operator


def set_matt(ctx, matt):
	meshes = [obj for obj in ctx.scene.objects if obj.type == 'MESH']
	
	for obj in meshes:
		for slot in obj.material_slots:
			outputs, matts = [], []
			
			for node in slot.material.node_tree.nodes:
				if node.type == 'OUTPUT_MATERIAL':
					links = node.inputs['Surface'].links 
					
					if len(links) > 0:
						if links[0].from_node.type == 'BSDF_TRANSPARENT':
							matts.append(node)
						else:
							outputs.append(node)

			if matts:
				for node in outputs:
					node.mute = matt
				for node in matts:
					node.mute = not matt


class Render_OT_Matt_Set(Operator):
	bl_idname = 'render.matt_set'
	bl_label = 'Matt Set'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		set_matt(ctx, True)
		return{'FINISHED'}

class Render_OT_Mat_Unset(Operator):
	bl_idname = 'render.matt_unset'
	bl_label = 'Matt Unset'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'

	def execute(self, ctx):
		set_matt(ctx, False)
		return{'FINISHED'}



classes = [Render_OT_Matt_Set,
	Render_OT_Mat_Unset]

def register_matt():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_matt():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	register_matt()