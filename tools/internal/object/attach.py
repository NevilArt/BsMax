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
from bsmax.operator import PickOperator


# Error: Python: Traceback (most recent call last):
#   File "C:\Users\nevil\AppData\Roaming\Blender Foundation\Blender\3.2\scripts\addons\BsMax\bsmax\operator.py", line 183, in modal
#     self.finish(ctx, event, picked_object)
#   File "C:\Users\nevil\AppData\Roaming\Blender Foundation\Blender\3.2\scripts\addons\BsMax\bsmax\operator.py", line 272, in finish
#     self.picked(ctx, self.source, self.subsource, target, subtarget)
#   File "C:\Users\nevil\AppData\Roaming\Blender Foundation\Blender\3.2\scripts\addons\BsMax\tools\internal\object\attach.py", line 54, in picked
#     self.convert(ctx, target)
#   File "C:\Users\nevil\AppData\Roaming\Blender Foundation\Blender\3.2\scripts\addons\BsMax\tools\internal\object\attach.py", line 50, in convert
#     bpy.ops.object.modifier_apply(modifier=modifier.name)
#   File "C:\Program Files\Blender Foundation\Blender 3.2\3.2\scripts\modules\bpy\ops.py", line 115, in __call__
#     ret = _op_call(self.idname_py(), None, kw)
# RuntimeError: Error: Transform curve to mesh in order to apply constructive modifiers



class Object_OT_Attach(PickOperator):
	""" Pick an object to join with the Active object """
	bl_idname = 'object.attach'
	bl_label = 'Attach'
	bl_description = ''
	
	filters = ['AUTO']

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object:
					return ctx.mode == 'OBJECT'
		return False
	
	def pre_setup(self, ctx, event):
		if ctx.active_object:
			if ctx.active_object.type == 'MESH':
				self.filters = ['MESH', 'CURVE']
			else:
				self.filters = ['AUTO']

	def convert(self, ctx, obj):
		obj.select_set(True)
		ctx.view_layer.objects.active = obj
		
		""" Collaps Modifiers """
		for modifier in obj.modifiers:
			bpy.ops.object.modifier_apply(modifier=modifier.name)

	def picked(self, ctx, source, subsource, target, subtarget):
		bpy.ops.object.select_all(action='DESELECT')
		self.convert(ctx, target)
		
		for obj in source:
			obj.select_set(True)
			ctx.view_layer.objects.active = obj
			
			if obj.type in {'MESH', 'CURVE'}:
				""" Clear Primitive Data """
				obj.data.primitivedata.classname = ''

				""" Make Same Type if Possible """
				if target.type != obj.type:
					bpy.ops.object.convert_to(target=obj.type)
		
		target.select_set(state = True)
		bpy.ops.object.join()
		bpy.ops.ed.undo_push()
		bpy.ops.object.attach('INVOKE_DEFAULT')
		self.report({'OPERATOR'},'bpy.ops.object.attach()')



class Object_TO_Delete_Plus(Operator):
	""" Delete Plus """
	bl_idname = 'object.delete_plus'
	bl_label = 'Delete Plus'
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
	def execute(self,ctx):
		for obj in ctx.selected_objects:
			for child in obj.children:
				matrix_world = child.matrix_world.copy()
				child.parent = None
				child.matrix_world = matrix_world
		bpy.ops.object.delete({'selected_objects': ctx.selected_objects})
		return{'FINISHED'}


classes = [Object_OT_Attach, Object_TO_Delete_Plus]

def register_attach():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_attach():
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == '__main__':
	register_attach()