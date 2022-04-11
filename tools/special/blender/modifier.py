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
from bsmax.actions import modifier_add
from bsmax.state import is_objects_selected

# this operator use to add modifier to selected objects from search box



class Modifier_OT_DATA_TRANSFER_Add(Operator):
	bl_idname = "modifier.add_data_transform"
	bl_label = "Data Transfer (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'DATA_TRANSFER')
		return {'FINISHED'}



class Modifier_OT_MESH_CACHE_Add(Operator):
	bl_idname = "modifier.add_mesh_cache"
	bl_label = "Mesh Cache (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MESH_CACHE')
		return {'FINISHED'}



class Modifier_OT_MESH_SEQUENCE_CACHE_Add(Operator):
	bl_idname = "modifier.add_mesh_sequence_cache"
	bl_label = "Mesh Sequence Cache (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MESH_SEQUENCE_CACHE')
		return {'FINISHED'}



class Modifier_OT_NORMAL_EDIT_Add(Operator):
	bl_idname = "modifier.add_normal_edit"
	bl_label = "Normal Edit (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'NORMAL_EDIT')
		return {'FINISHED'}



class Modifier_OT_WEIGHTED_NORMAL_Add(Operator):
	bl_idname = "modifier.add_weighted_normal"
	bl_label = "Weighted Normal (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'WEIGHTED_NORMAL')
		return {'FINISHED'}



class Modifier_OT_UV_PROJECT_Add(Operator):
	bl_idname = "modifier.add_uv_project"
	bl_label = "UV Project (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'UV_PROJECT')
		return {'FINISHED'}



class Modifier_OT_UV_WARP_Add(Operator):
	bl_idname = "modifier.add_uvwarp"
	bl_label = "UV Warp (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'UV_WARP')
		return {'FINISHED'}



class Modifier_OT_VERTEX_WEIGHT_EDIT_Add(Operator):
	bl_idname = "modifier.add_vertex_weight_edit"
	bl_label = "Vertex Weight Edit (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'VERTEX_WEIGHT_EDIT')
		return {'FINISHED'}



class Modifier_OT_VERTEX_WEIGHT_MIX_Add(Operator):
	bl_idname = "modifier.add_vertex_weight_mix"
	bl_label = "Vertex Weight Mix (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'VERTEX_WEIGHT_MIX')
		return {'FINISHED'}



class Modifier_OT_VERTEX_WEIGHT_PROXIMITY_Add(Operator):
	bl_idname = "modifier.add_vertex_weight_proximity"
	bl_label = "Vertex Weight Proximity (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod

	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'VERTEX_WEIGHT_PROXIMITY')
		return {'FINISHED'}



class Modifier_OT_ARRAY_Add(Operator):
	bl_idname = "modifier.add_array"
	bl_label = "Array (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'ARRAY')
		return {'FINISHED'}



class Modifier_OT_BEVEL_Add(Operator):
	bl_idname = "modifier.add_bevel"
	bl_label = "Bevel (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'BEVEL')
		return {'FINISHED'}



class Modifier_OT_BOOLEAN_Add(Operator):
	bl_idname = "modifier.add_boolean"
	bl_label = "Boolean (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'BOOLEAN')
		return {'FINISHED'}



class Modifier_OT_BUILD_Add(Operator):
	bl_idname = "modifier.add_build"
	bl_label = "Build (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'BUILD')
		return {'FINISHED'}



class Modifier_OT_DECIMATE_Add(Operator):
	bl_idname = "modifier.add_decimate"
	bl_label = "Decimate (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'DECIMATE')
		return {'FINISHED'}



class Modifier_OT_EDGE_SPLIT_Add(Operator):
	bl_idname = "modifier.add_edgesplit"
	bl_label = "Edge Split (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'EDGE_SPLIT')
		return {'FINISHED'}



class Modifier_OT_Mask_Add(Operator):
	bl_idname = "modifier.add_mask"
	bl_label = "Mask (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MASK')
		return {'FINISHED'}



class Modifier_OT_MIRROR_Add(Operator):
	bl_idname = "modifier.add_mirror"
	bl_label = "Mirror (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MIRROR')
		return {'FINISHED'}



class Modifier_OT_MULTIRES_Add(Operator):
	bl_idname = "modifier.add_multires"
	bl_label = "Multires (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MULTIRES')
		return {'FINISHED'}



class Modifier_OT_REMESH_Add(Operator):
	bl_idname = "modifier.add_remesh"
	bl_label = "Remesh (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'REMESH')
		return {'FINISHED'}



class Modifier_OT_Screw_Add(Operator):
	bl_idname = "modifier.add_screw"
	bl_label = "Screw (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SCREW')
		return {'FINISHED'}



class Modifier_OT_SKIN_Add(Operator):
	bl_idname = "modifier.add_skin"
	bl_label = "Skin (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SKIN')
		return {'FINISHED'}



class Modifier_OT_SOLIDIFY_Add(Operator):
	bl_idname = "modifier.add_solidify"
	bl_label = "Solidify (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SOLIDIFY')
		return {'FINISHED'}



class Modifier_OT_SUBSURF_Add(Operator):
	bl_idname = "modifier.add_subsurf"
	bl_label = "Subsurf (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SUBSURF')
		return {'FINISHED'}



class Modifier_OT_TRIANGULATE_Add(Operator):
	bl_idname = "modifier.add_triangulate"
	bl_label = "Triangulate (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'TRIANGULATE')
		return {'FINISHED'}



class Modifier_OT_WIREFRAME_Add(Operator):
	bl_idname = "modifier.add_wireframe"
	bl_label = "Wireframe (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'WIREFRAME')
		return {'FINISHED'}



class Modifier_OT_ARMATURE_Add(Operator):
	bl_idname = "modifier.add_armature"
	bl_label = "Armature (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'ARMATURE')
		return {'FINISHED'}



class Modifier_OT_CAST_Add(Operator):
	bl_idname = "modifier.add_cast"
	bl_label = "Cast (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'CAST')
		return {'FINISHED'}



class Modifier_OT_CURVE_Add(Operator):
	bl_idname = "modifier.add_curve"
	bl_label = "Curve (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'CURVE')
		return {'FINISHED'}



class Modifier_OT_DISPLACE_Add(Operator):
	bl_idname = "modifier.add_displace"
	bl_label = "Displace (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'DISPLACE')
		return {'FINISHED'}



class Modifier_OT_HOOK_Add(Operator):
	bl_idname = "modifier.add_hook"
	bl_label = "Hook (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'HOOK')
		return {'FINISHED'}



class Modifier_OT_LAPLACIANDEFORM_Add(Operator):
	bl_idname = "modifier.add_laplaciandeform"
	bl_label = "Laplacian Deform (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'LAPLACIANDEFORM')
		return {'FINISHED'}



class Modifier_OT_LATTICE_Add(Operator):
	bl_idname = "modifier.add_lattice"
	bl_label = "Lattice (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'LATTICE')
		return {'FINISHED'}



class Modifier_OT_MESH_DEFORM_Add(Operator):
	bl_idname = "modifier.add_meshdeform"
	bl_label = "Mesh Deform (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MESH_DEFORM')
		return {'FINISHED'}



class Modifier_OT_SHRINKWRAP_Add(Operator):
	bl_idname = "modifier.add_shrinkwarp"
	bl_label = "Shrink Warp (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SHRINKWRAP')
		return {'FINISHED'}



class Modifier_OT_SIMPLE_DEFORM_Add(Operator):
	bl_idname = "modifier.add_simpledeform"
	bl_label = "Simple Deform (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SIMPLE_DEFORM')
		return {'FINISHED'}



class Modifier_OT_SMOOTH_Add(Operator):
	bl_idname = "modifier.add_smooth"
	bl_label = "Smooth (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SMOOTH')
		return {'FINISHED'}



class Modifier_OT_CORRECTIVE_SMOOTH_Add(Operator):
	bl_idname = "modifier.add_correctivesmooth"
	bl_label = "Corrective Smooth (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'CORRECTIVE_SMOOTH')
		return {'FINISHED'}



class Modifier_OT_LAPLACIANSMOOTH_Add(Operator):
	bl_idname = "modifier.add_laplaciansmooth"
	bl_label = "Laplacian Smooth (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'LAPLACIANSMOOTH')
		return {'FINISHED'}



class Modifier_OT_SURFACE_DEFORM_Add(Operator):
	bl_idname = "modifier.add_surfacedeform"
	bl_label = "Surface Deform (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SURFACE_DEFORM')
		return {'FINISHED'}



class Modifier_OT_WARP_Add(Operator):
	bl_idname = "modifier.add_warp"
	bl_label = "Warp (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'WARP')
		return {'FINISHED'}



class Modifier_OT_WAVE_Add(Operator):
	bl_idname = "modifier.add_wave"
	bl_label = "Wave (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'WAVE')
		return {'FINISHED'}



class Modifier_OT_CLOTH_Add(Operator):
	bl_idname = "modifier.add_cloth"
	bl_label = "Cloth (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'CLOTH')
		return {'FINISHED'}



class Modifier_OT_COLLISION_Add(Operator):
	bl_idname = "modifier.add_collision"
	bl_label = "Collision (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'COLLISION')
		return {'FINISHED'}



class Modifier_OT_DYNAMIC_PAINT_Add(Operator):
	bl_idname = "modifier.add_dynamicpaint"
	bl_label = "Dynamic Paint (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'DYNAMIC_PAINT')
		self.report({'OPERATOR'},'bpy.ops.modifier.add_dynamicpaintadd()')
		return {'FINISHED'}



class Modifier_OT_EXPLODE_Add(Operator):
	bl_idname = "modifier.add_explode"
	bl_label = "Explode (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'EXPLODE')
		return {'FINISHED'}



class Modifier_OT_FLUID_SIMULATION_Add(Operator):
	bl_idname = "modifier.add_fluidsimulation"
	bl_label = "Fluid Simulation (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'FLUID_SIMULATION')
		return {'FINISHED'}



class Modifier_OT_OCEAN_Add(Operator):
	bl_idname = "modifier.add_ocean"
	bl_label = "Ocean (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'OCEAN')
		return {'FINISHED'}



class Modifier_OT_PARTICLE_INSTANCE_Add(Operator):
	bl_idname = "modifier.add_particleinstance"
	bl_label = "Particle Instance (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'PARTICLE_INSTANCE')
		return {'FINISHED'}



class Modifier_OT_PARTICLE_SYSTEM_Add(Operator):
	bl_idname = "modifier.add_particlesysteme"
	bl_label = "Particle System (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'PARTICLE_SYSTEM')
		return {'FINISHED'}



class Modifier_OT_SMOKE_Add(Operator):
	bl_idname = "modifier.add_smoke"
	bl_label = "Smoke (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SMOKE')
		return {'FINISHED'}



class Modifier_OT_SOFT_BODY_Add(Operator):
	bl_idname = "modifier.add_softbody"
	bl_label = "Soft Body (add)"
	bl_options = {'REGISTER','UNDO'}

	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)

	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SOFT_BODY')
		return {'FINISHED'}



classes = [
		Modifier_OT_DATA_TRANSFER_Add,
		Modifier_OT_MESH_CACHE_Add,
		Modifier_OT_MESH_SEQUENCE_CACHE_Add,
		Modifier_OT_NORMAL_EDIT_Add,
		Modifier_OT_WEIGHTED_NORMAL_Add,
		Modifier_OT_UV_PROJECT_Add,
		Modifier_OT_UV_WARP_Add,
		Modifier_OT_VERTEX_WEIGHT_EDIT_Add,
		Modifier_OT_VERTEX_WEIGHT_MIX_Add,
		Modifier_OT_VERTEX_WEIGHT_PROXIMITY_Add,
		Modifier_OT_ARRAY_Add,
		Modifier_OT_BEVEL_Add,
		Modifier_OT_BOOLEAN_Add,
		Modifier_OT_BUILD_Add,
		Modifier_OT_DECIMATE_Add,
		Modifier_OT_EDGE_SPLIT_Add,
		Modifier_OT_Mask_Add,
		Modifier_OT_MIRROR_Add,
		Modifier_OT_MULTIRES_Add,
		Modifier_OT_REMESH_Add,
		Modifier_OT_Screw_Add,
		Modifier_OT_SKIN_Add,
		Modifier_OT_SOLIDIFY_Add,
		Modifier_OT_SUBSURF_Add,
		Modifier_OT_TRIANGULATE_Add,
		Modifier_OT_WIREFRAME_Add,
		Modifier_OT_ARMATURE_Add,
		Modifier_OT_CAST_Add,
		Modifier_OT_CURVE_Add,
		Modifier_OT_DISPLACE_Add,
		Modifier_OT_HOOK_Add,
		Modifier_OT_LAPLACIANDEFORM_Add,
		Modifier_OT_LATTICE_Add,
		Modifier_OT_MESH_DEFORM_Add,
		Modifier_OT_SHRINKWRAP_Add,
		Modifier_OT_SIMPLE_DEFORM_Add,
		Modifier_OT_SMOOTH_Add,
		Modifier_OT_CORRECTIVE_SMOOTH_Add,
		Modifier_OT_LAPLACIANSMOOTH_Add,
		Modifier_OT_SURFACE_DEFORM_Add,
		Modifier_OT_WARP_Add,
		Modifier_OT_WAVE_Add,
		Modifier_OT_CLOTH_Add,
		Modifier_OT_COLLISION_Add,
		Modifier_OT_DYNAMIC_PAINT_Add,
		Modifier_OT_EXPLODE_Add,
		Modifier_OT_FLUID_SIMULATION_Add,
		Modifier_OT_OCEAN_Add,
		Modifier_OT_PARTICLE_INSTANCE_Add,
		Modifier_OT_PARTICLE_SYSTEM_Add,
		Modifier_OT_SMOKE_Add,
		Modifier_OT_SOFT_BODY_Add
]
		
def register_modifier():
	for c in classes:
		bpy.utils.register_class(c)

def unregister_modifier():
	for c in classes:
		if hasattr(bpy.types, eval("bpy.ops." + c.bl_idname + ".idname()")):
			bpy.utils.unregister_class(c)