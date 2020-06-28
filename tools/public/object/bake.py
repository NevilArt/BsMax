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
from bpy.props import BoolProperty,EnumProperty

def bake(self,ctx,hi,low,cage,bake_type):
	bpy.ops.object.select_all(action='DESELECT')
	source, target = bpy.data.objects[hi], bpy.data.objects[low]
	source.select_set(action='SELECT')
	target.select_set(action='SELECT')
	ctx.view_layer.objects.active = target
	
	ctx.scene.render.bake.use_selected_to_active = True
	if cage != '':
		ctx.scene.render.bake.use_cage = True
		ctx.scene.render.bake.cage_object = bpy.data.objects[cage]
	ctx.scene.cycles.bake_type = bake_type

	


class Object_OT_Bake_Texture(bpy.types.Operator):
	bl_idname = "object.bake_texture"
	bl_label = "Bake Texture"
	bl_description = "Auto Texture Bake of the selected objects"
	bl_options = {'REGISTER', 'UNDO'}

	def get_source(self, ctx):
		# TODO set the heigh poly object as first item
		return [('','','')]+[(o.name,o.name,'') for o in  ctx.selected_objects if o.type == 'MESH']

	def get_target(self, ctx):
		# TODO set the low poly object as first item
		return [('','','')]+[(o.name,o.name,'') for o in  ctx.selected_objects if o.type == 'MESH']
	
	def get_cage(self, ctx):
		# TODO some how ges the cage object
		return [('','','')]+[(o.name,o.name,'') for o in  ctx.selected_objects if o.type == 'MESH']

	source: EnumProperty(items=get_source)
	target: EnumProperty(items=get_target)
	cage: EnumProperty(items=get_cage)
	
	combined: BoolProperty()
	ao: BoolProperty()
	shadow: BoolProperty()
	normal: BoolProperty()
	uv: BoolProperty()
	roughness: BoolProperty()
	emit: BoolProperty()
	environment: BoolProperty()
	diffuse: BoolProperty()
	glossy: BoolProperty()
	transmission: BoolProperty()

	# @classmethod
	# def poll(self, ctx):
	# ctx.scene.render.engine == 'CYCLES'
	# 	if 1 > len(ctx.selected_objects) < 4:
	# 		return True
	# 	return False

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self,'source')
		layout.prop(self,'target')
		layout.prop(self,'cage')
		layout.prop(self,'combined',text='Combined')
		layout.prop(self,'ao',text='Ambient Occlusion')
		layout.prop(self,'shadow',text='Shadow')
		layout.prop(self,'normal',text='Normal')
		layout.prop(self,'uv',text='UV')
		layout.prop(self,'roughness',text='Roughness')
		layout.prop(self,'emit',text='Emit')
		layout.prop(self,'environment',text='Environment')
		layout.prop(self,'diffuse',text='Diffuse')
		layout.prop(self,'glossy',text='Glossy')
		layout.prop(self,'transmission',text='Transmission')
	
	def execute(self, ctx):
		bake_types = [] 
		if self.combined:
			bake_types.append('COMBINED')
			bake_types.append('AO')
			bake_types.append('SHADOW')
			bake_types.append('NORMAL')
			bake_types.append('UV')
			bake_types.append('ROUGHNESS')
			bake_types.append('EMIT')
			bake_types.append('ENVIRONMENT')
			bake_types.append('DIFFUSE')
			bake_types.append('GLOSSY')
			bake_types.append('TRANSMISSION')
		for bake_type in bake_types:
			bake(self,ctx,self.source,self.target,self.cage,bake_type)
		self.report({'INFO'},'bpy.ops.object.texture_bake()')
		return {'FINISHED'}

	def cancel(self, ctx):
		return None

	def invoke(self, ctx, evt):
		ctx.window_manager.invoke_props_dialog(self)
		return {'RUNNING_MODAL'}

def register_bake():
	bpy.utils.register_class(Object_OT_Bake_Texture)

def unregister_bake():
	bpy.utils.unregister_class(Object_OT_Bake_Texture)

if __name__ == "__main__":
	register_bake()