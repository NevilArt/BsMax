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
from bsmax.operator import PickOperator
from bsmax.actions import link_to_scene

class Armature_OT_Attach(PickOperator):
	bl_idname = "armature.attach"
	bl_label = "Attach"
	bl_options = {'REGISTER', 'UNDO'}
	filters = ['ARMATURE','MESH','FONT','CURVE']
	
	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode in {'EDIT_ARMATURE', 'POSE'}
		return False
	
	def create_empty_mesh_object(self, ctx):
		newmesh = bpy.data.meshes.new("temp_mesh")
		newmesh.from_pydata([],[],[])
		newmesh.update(calc_edges=True)
		owner = bpy.data.objects.new("Blabla",newmesh)
		link_to_scene(ctx, owner)
		return owner
	
	def picked(self, ctx, source, subsource, target, subtarget):
		if target.type == 'ARMATURE':
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
			target.select_set(state = True)
			bpy.ops.object.join()
			bpy.ops.object.mode_set(mode='EDIT', toggle=False)
			bpy.ops.armature.attach('INVOKE_DEFAULT')
		
		elif target.type in {'MESH','FONT','CURVE'}:
			mode = ctx.mode if ctx.mode == 'POSE' else 'EDIT'
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
			armature = source[0]
			
			""" select target and convert to mesh """
			bpy.ops.object.select_all(action = 'DESELECT')
			target.select_set(state = True)
			ctx.view_layer.objects.active = target
			bpy.ops.object.convert(target='MESH')
			bpy.ops.object.select_all(action = 'DESELECT')

			for bone in subsource:
				""" Get Mesh data if avalible """
				old_mesh = bpy.data.objects[bone.custom_shape.data.name_full].data if bone.custom_shape else None
				new_mesh = self.create_empty_mesh_object(ctx)
				if old_mesh:
					new_mesh.data = old_mesh

				new_mesh.location = armature.matrix_world @ armature.data.bones.active.head_local
				new_mesh.rotation_euler = armature.data.bones.active.matrix_local.to_euler()
				new_mesh.scale = armature.data.bones.active.matrix_local.to_scale()

				bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

				bpy.ops.object.select_all(action = 'DESELECT')
				new_mesh.select_set(state = True)
				ctx.view_layer.objects.active = new_mesh
				
				target.select_set(state = True)
				bpy.ops.object.join()
	
				bpy.ops.object.delete({"selected_objects": [new_mesh]})

			""" Restor default selection set """
			bpy.ops.object.select_all(action='DESELECT')
			for obj in source:
				if obj.type == 'ARMATURE':
					obj.select_set(state = True)
					ctx.view_layer.objects.active = obj
			if ctx.active_object.type == 'ARMATURE':
				bpy.ops.object.mode_set(mode=mode, toggle=False)

		self.report({'OPERATOR'},'bpy.ops.armature.attach()')

classes = [Armature_OT_Attach]

def register_attach():
	[bpy.utils.register_class(c) for c in classes]

def unregister_attach():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_attach()