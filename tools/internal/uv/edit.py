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
from bsmax.actions import set_as_active_object,link_to_scene

class UV_OT_Turn(Operator):
	bl_idname = "uv.turn"
	bl_label = "Turn"
	bl_options = {'REGISTER', 'UNDO'}
	
	ccw: BoolProperty(name="CCW")

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		value = 1.5708 if self.ccw else -1.5708
		bpy.ops.transform.rotate(value=value,orient_axis='Z',orient_type='VIEW',
						orient_matrix=((-1,-0,-0),(-0,-1,-0),(-0,-0,-1)),
						orient_matrix_type='VIEW',mirror=True,
						use_proportional_edit=False,proportional_edit_falloff='SMOOTH',
						proportional_size=1,use_proportional_connected=False,
						use_proportional_projected=False)
		self.report({'OPERATOR'},'bpy.ops.uv.turn()')
		return{"FINISHED"}

# not done yet
class UV_OT_Plane_Projection(Operator):
	bl_idname = "uv.plane_projection"
	bl_label = "Plane Projection"
	bl_options = {'REGISTER', 'UNDO'}
	
	quick: BoolProperty(name="Quick",default=True)

	@classmethod
	def poll(self, ctx):
		return False # ctx.mode == 'EDIT'

	def execute(self, ctx):
		# working on not complete yet
		obj = ctx.active_object
		mod = obj.modifiers.new(name="BoxUVProjector", type='UV_PROJECT')
		bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
		gizmo = ctx.active_object
		# mod.object = gizmo
		bpy.context.object.object = bpy.data.objects["Empty"]
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="BoxUVProjector")
		bpy.ops.object.delete({"selected_objects":[gizmo]})
		set_as_active_object(ctx,obj)
		bpy.ops.object.mode_set(mode='EDIT')

		self.report({'OPERATOR'},'bpy.ops.uv.plane_projection()')
		return{"FINISHED"}

classes = [UV_OT_Turn,UV_OT_Plane_Projection]

def register_edit():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_edit():
	for c in classes:
		bpy.utils.unregister_class(c)