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
from bpy.props import EnumProperty



class Render_OT_Quick_Render(Operator):
	bl_idname = "render.quick_render"
	bl_label = "Quick Render"

	@classmethod
	def poll(self, ctx):
		return True

	def execute(self, ctx):
		r3d = ctx.area.spaces[0].region_3d
		if r3d.view_perspective == 'CAMERA':
			bpy.ops.render.render('INVOKE_DEFAULT')
		else:
			# trick is create a camera from view and delete after render 
			# but for unknown reason 
			view_matrix = ctx.area.spaces.active.region_3d.view_matrix
			bpy.ops.object.camera_add()
			ctx.scene.camera = bpy.data.objects[ctx.active_object.name]
			cam = ctx.active_object
			cam.matrix_world = view_matrix
			bpy.ops.render.render('INVOKE_DEFAULT')
			bpy.ops.object.delete({"selected_objects": cam})
			# bpy.ops.object.delete(use_global=False, confirm=False)
		return{"FINISHED"}



class Render_OT_Set_Renderer(Operator):
	bl_idname = "render.set_renderer"
	bl_label = "Set Renderer"

	name: EnumProperty(name='Name', default='BLENDER_EEVEE',
		items=[('BLENDER_EEVEE', 'EEVEE',''),
			('BLENDER_WORKBENCH', 'Workbench',''),
			('CYCLES', 'Cycles','')])

	def execute(self, ctx):
		ctx.scene.render.engine = self.name
		return{"FINISHED"}


class Render_OT_Setting_Toggle(Operator):
	bl_idname = "render.setting_toggle"
	bl_label = "Render Setting Toggle"

	name: EnumProperty(
		name='Name', default='use_gtao',
		items=[
			('use_gtao', 'use_gtao',''),
			('use_bloom', 'use_bloom',''),
			('use_ssr', 'use_ssr',''),
			('use_motion_blur', 'use_motion_blur',''),
			('use_simplify', 'use_simplify',''),
			('use_freestyle', 'use_freestyle',''),
			('use_curves', 'use_curves',''),
			('show_backface_culling', 'show_backface_culling',''),
			('use_motion_blur', 'use_motion_blur',''),
			('show_xray', 'show_xray',''),
			('show_shadows', 'show_shadows',''),
			('show_cavity', 'show_cavity',''),
			('use_dof', 'use_dof',''),
			('show_object_outline', 'show_object_outline','')
		]
	)

	def execute(self, ctx):
		if self.name == 'use_gtao':
			ctx.scene.eevee.use_gtao = not ctx.scene.eevee.use_gtao
		elif self.name == 'use_bloom':
			ctx.scene.eevee.use_bloom = not ctx.scene.eevee.use_bloom 
		elif self.name == 'use_ssr':
			ctx.scene.eevee.use_ssr = not ctx.scene.eevee.use_ssr
		elif self.name == 'use_motion_blur':	
			ctx.scene.eevee.use_motion_blur = not ctx.scene.eevee.use_motion_blur
		elif self.name == 'use_simplify':	
			ctx.scene.render.use_simplify = not ctx.scene.render.use_simplify
		elif self.name == 'use_freestyle':
			ctx.scene.render.use_freestyle = not ctx.scene.render.use_freestyle
		elif self.name == 'use_curves':	
			ctx.scene.cycles_curves.use_curves = not ctx.scene.cycles_curves.use_curves
		elif self.name == 'show_backface_culling':	
			ctx.scene.shading.show_backface_culling = not ctx.scene.shading.show_backface_culling
		elif self.name == 'use_motion_blur':	
			ctx.scene.render.use_motion_blur = not ctx.scene.render.use_motion_blur
		elif self.name == 'show_xray':
			ctx.scene.shading.show_xray = not ctx.scene.shading.show_xray
		elif self.name == 'show_shadows':	
			ctx.scene.shading.show_shadows = not ctx.scene.shading.show_shadows
		elif self.name == 'show_cavity':	
			ctx.scene.shading.show_cavity = not ctx.scene.shading.show_cavity
		elif self.name == 'use_dof':
			ctx.scene.shading.use_dof = not ctx.scene.shading.use_dof
		elif self.name == 'show_object_outline':	
			ctx.scene.shading.show_object_outline = not ctx.scene.shading.show_object_outline

		return{"FINISHED"}




classes = (
	Render_OT_Quick_Render,
	Render_OT_Set_Renderer,
	Render_OT_Setting_Toggle
)



def register_quick_render():
	for c in classes:
		bpy.utils.register_class(c)



def unregister_quick_render():
	for c in classes:
		bpy.utils.unregister_class(c)



if __name__ == "__main__":
	register_quick_render()