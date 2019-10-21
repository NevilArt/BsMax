import bpy
from bpy.types import Operator
from bsmax.actions import modifier_add
from bsmax.state import is_objects_selected

class BsMax_OT_Lattice_2x2x2_Set(Operator):
	bl_idname = "modifier.lattice2x2x2set"
	bl_label = "Lattice 2x2x2 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.bsmax.latticebox(res_u=2,res_v=2,res_w=2)
		return{"FINISHED"}

class BsMax_OT_Lattice_3x3x3_Set(Operator):
	bl_idname = "modifier.lattice3x3x3set"
	bl_label = "Lattice 3x3x3 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.bsmax.latticebox(res_u=3,res_v=3,res_w=3)
		return{"FINISHED"}

class BsMax_OT_Lattice_4x4x4_Set(Operator):
	bl_idname = "modifier.lattice4x4x4set"
	bl_label = "Lattice 4x4x4 (Set)"
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		bpy.ops.bsmax.latticebox(res_u=4,res_v=4,res_w=4)
		return{"FINISHED"}

class BsMax_OT_DATA_TRANSFER_Add(Operator):
	bl_idname = "modifier.datatransformadd"
	bl_label = "Data Transfer (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'DATA_TRANSFER')
		return {'FINISHED'}

class BsMax_OT_MESH_CACHE_Add(Operator):
	bl_idname = "modifier.meshcacheadd"
	bl_label = "Mesh Cache (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MESH_CACHE')
		return {'FINISHED'}

class BsMax_OT_MESH_SEQUENCE_CACHE_Add(Operator):
	bl_idname = "modifier.meshsequencecacheadd"
	bl_label = "Mesh Sequence Cache (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MESH_SEQUENCE_CACHE')
		return {'FINISHED'}

class BsMax_OT_NORMAL_EDIT_Add(Operator):
	bl_idname = "modifier.normaleditadd"
	bl_label = "Normal Edit (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'NORMAL_EDIT')
		return {'FINISHED'}

class BsMax_OT_WEIGHTED_NORMAL_Add(Operator):
	bl_idname = "modifier.weightednormaladd"
	bl_label = "Weighted Normal (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'WEIGHTED_NORMAL')
		return {'FINISHED'}

class BsMax_OT_UV_PROJECT_Add(Operator):
	bl_idname = "modifier.uvprojectadd"
	bl_label = "UV Project (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'UV_PROJECT')
		return {'FINISHED'}

class BsMax_OT_UV_WARP_Add(Operator):
	bl_idname = "modifier.uvwarpadd"
	bl_label = "UV Warp (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'UV_WARP')
		return {'FINISHED'}

class BsMax_OT_VERTEX_WEIGHT_EDIT_Add(Operator):
	bl_idname = "modifier.vertexweighteditadd"
	bl_label = "Vertex Weight Edit (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'VERTEX_WEIGHT_EDIT')
		return {'FINISHED'}

class BsMax_OT_VERTEX_WEIGHT_MIX_Add(Operator):
	bl_idname = "modifier.vertexweightmixadd"
	bl_label = "Vertex Weight Mix (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'VERTEX_WEIGHT_MIX')
		return {'FINISHED'}

class BsMax_OT_VERTEX_WEIGHT_PROXIMITY_Add(Operator):
	bl_idname = "modifier.vertexweightproximityadd"
	bl_label = "Vertex Weight Proximity (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'VERTEX_WEIGHT_PROXIMITY')
		return {'FINISHED'}

class BsMax_OT_ARRAY_Add(Operator):
	bl_idname = "modifier.arrayadd"
	bl_label = "Array (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'ARRAY')
		return {'FINISHED'}

class BsMax_OT_BEVEL_Add(Operator):
	bl_idname = "modifier.beveladd"
	bl_label = "Bevel (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'BEVEL')
		return {'FINISHED'}

class BsMax_OT_BOOLEAN_Add(Operator):
	bl_idname = "modifier.booleanadd"
	bl_label = "Boolean (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'BOOLEAN')
		return {'FINISHED'}

class BsMax_OT_BUILD_Add(Operator):
	bl_idname = "modifier.buildadd"
	bl_label = "Build (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'BUILD')
		return {'FINISHED'}

class BsMax_OT_DECIMATE_Add(Operator):
	bl_idname = "modifier.decimateadd"
	bl_label = "Decimate (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'DECIMATE')
		return {'FINISHED'}

class BsMax_OT_EDGE_SPLIT_Add(Operator):
	bl_idname = "modifier.edgesplitadd"
	bl_label = "Edge Split (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'EDGE_SPLIT')
		return {'FINISHED'}

class BsMax_OT_Mask_Add(Operator):
	bl_idname = "modifier.maskadd"
	bl_label = "Mask (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MASK')
		return {'FINISHED'}

class BsMax_OT_MIRROR_Add(Operator):
	bl_idname = "modifier.mirroradd"
	bl_label = "Mirror (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MIRROR')
		return {'FINISHED'}

class BsMax_OT_MULTIRES_Add(Operator):
	bl_idname = "modifier.multiresadd"
	bl_label = "Multires (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MULTIRES')
		return {'FINISHED'}

class BsMax_OT_REMESH_Add(Operator):
	bl_idname = "modifier.remeshadd"
	bl_label = "Remesh (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'REMESH')
		return {'FINISHED'}

class BsMax_OT_Screw_Add(Operator):
	bl_idname = "modifier.screwadd"
	bl_label = "Screw (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SCREW')
		return {'FINISHED'}

class BsMax_OT_SKIN_Add(Operator):
	bl_idname = "modifier.skinadd"
	bl_label = "Skin (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SKIN')
		return {'FINISHED'}

class BsMax_OT_SOLIDIFY_Add(Operator):
	bl_idname = "modifier.solidifyadd"
	bl_label = "Solidify (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SOLIDIFY')
		return {'FINISHED'}

class BsMax_OT_SUBSURF_Add(Operator):
	bl_idname = "modifier.subsurfadd"
	bl_label = "Subsurf (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SUBSURF')
		return {'FINISHED'}

class BsMax_OT_TRIANGULATE_Add(Operator):
	bl_idname = "modifier.triangulateadd"
	bl_label = "Triangulate (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'TRIANGULATE')
		return {'FINISHED'}

class BsMax_OT_WIREFRAME_Add(Operator):
	bl_idname = "modifier.wireframeadd"
	bl_label = "Wireframe (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'WIREFRAME')
		return {'FINISHED'}

class BsMax_OT_ARMATURE_Add(Operator):
	bl_idname = "modifier.armatureadd"
	bl_label = "Armature (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'ARMATURE')
		return {'FINISHED'}

class BsMax_OT_CAST_Add(Operator):
	bl_idname = "modifier.castadd"
	bl_label = "Cast (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'CAST')
		return {'FINISHED'}

class BsMax_OT_CURVE_Add(Operator):
	bl_idname = "modifier.curveadd"
	bl_label = "Curve (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'CURVE')
		return {'FINISHED'}

class BsMax_OT_DISPLACE_Add(Operator):
	bl_idname = "modifier.displaceadd"
	bl_label = "Displace (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'DISPLACE')
		return {'FINISHED'}

class BsMax_OT_HOOK_Add(Operator):
	bl_idname = "modifier.hookadd"
	bl_label = "Hook (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'HOOK')
		return {'FINISHED'}

class BsMax_OT_LAPLACIANDEFORM_Add(Operator):
	bl_idname = "modifier.laplaciandeformadd"
	bl_label = "Laplacian Deform (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'LAPLACIANDEFORM')
		return {'FINISHED'}

class BsMax_OT_LATTICE_Add(Operator):
	bl_idname = "modifier.latticeadd"
	bl_label = "Lattice (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'LATTICE')
		return {'FINISHED'}

class BsMax_OT_MESH_DEFORM_Add(Operator):
	bl_idname = "modifier.meshdeformadd"
	bl_label = "Mesh Deform (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'MESH_DEFORM')
		return {'FINISHED'}

class BsMax_OT_SHRINKWRAP_Add(Operator):
	bl_idname = "modifier.shrinkwarpadd"
	bl_label = "Shrink Warp (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SHRINKWRAP')
		return {'FINISHED'}

class BsMax_OT_SIMPLE_DEFORM_Add(Operator):
	bl_idname = "modifier.simpledeformadd"
	bl_label = "Simple Deform (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SIMPLE_DEFORM')
		return {'FINISHED'}

class BsMax_OT_SMOOTH_Add(Operator):
	bl_idname = "modifier.smoothadd"
	bl_label = "Smooth (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SMOOTH')
		return {'FINISHED'}

class BsMax_OT_CORRECTIVE_SMOOTH_Add(Operator):
	bl_idname = "modifier.correctivesmoothadd"
	bl_label = "Corrective Smooth (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'CORRECTIVE_SMOOTH')
		return {'FINISHED'}

class BsMax_OT_LAPLACIANSMOOTH_Add(Operator):
	bl_idname = "modifier.laplaciansmoothadd"
	bl_label = "Laplacian Smooth (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'LAPLACIANSMOOTH')
		return {'FINISHED'}

class BsMax_OT_SURFACE_DEFORM_Add(Operator):
	bl_idname = "modifier.surfacedeformadd"
	bl_label = "Surface Deform (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SURFACE_DEFORM')
		return {'FINISHED'}

class BsMax_OT_WARP_Add(Operator):
	bl_idname = "modifier.warpadd"
	bl_label = "Warp (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'WARP')
		return {'FINISHED'}

class BsMax_OT_WAVE_Add(Operator):
	bl_idname = "modifier.waveadd"
	bl_label = "Wave (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'WAVE')
		return {'FINISHED'}

class BsMax_OT_CLOTH_Add(Operator):
	bl_idname = "modifier.clothadd"
	bl_label = "Cloth (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'CLOTH')
		return {'FINISHED'}

class BsMax_OT_COLLISION_Add(Operator):
	bl_idname = "modifier.collisionadd"
	bl_label = "Collision (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'COLLISION')
		return {'FINISHED'}

class BsMax_OT_DYNAMIC_PAINT_Add(Operator):
	bl_idname = "modifier.dynamicpaintadd"
	bl_label = "Dynamic Paint (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'DYNAMIC_PAINT')
		return {'FINISHED'}

class BsMax_OT_EXPLODE_Add(Operator):
	bl_idname = "modifier.explodeadd"
	bl_label = "Explode (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'EXPLODE')
		return {'FINISHED'}

class BsMax_OT_FLUID_SIMULATION_Add(Operator):
	bl_idname = "modifier.fluidsimulationadd"
	bl_label = "Fluid Simulation (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'FLUID_SIMULATION')
		return {'FINISHED'}

class BsMax_OT_OCEAN_Add(Operator):
	bl_idname = "modifier.oceanadd"
	bl_label = "Ocean (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'OCEAN')
		return {'FINISHED'}

class BsMax_OT_PARTICLE_INSTANCE_Add(Operator):
	bl_idname = "modifier.particleinstanceadd"
	bl_label = "Particle Instance (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'PARTICLE_INSTANCE')
		return {'FINISHED'}

class BsMax_OT_PARTICLE_SYSTEM_Add(Operator):
	bl_idname = "modifier.particlesystemeadd"
	bl_label = "Particle System (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'PARTICLE_SYSTEM')
		return {'FINISHED'}

class BsMax_OT_SMOKE_Add(Operator):
	bl_idname = "modifier.smokeadd"
	bl_label = "Smoke (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SMOKE')
		return {'FINISHED'}

class BsMax_OT_SOFT_BODY_Add(Operator):
	bl_idname = "modifier.softbodyadd"
	bl_label = "Soft Body (add)"
	bl_options = {'REGISTER','UNDO'}
	@classmethod
	def poll(self, ctx):
		return is_objects_selected(ctx)
	def execute(self, ctx):
		modifier_add(ctx,ctx.selected_objects,'SOFT_BODY')
		return {'FINISHED'}

def modifier_cls(register):
	classes = [BsMax_OT_Lattice_2x2x2_Set,
			BsMax_OT_Lattice_3x3x3_Set,
			BsMax_OT_Lattice_4x4x4_Set,
			BsMax_OT_DATA_TRANSFER_Add,
			BsMax_OT_MESH_CACHE_Add,
			BsMax_OT_MESH_SEQUENCE_CACHE_Add,
			BsMax_OT_NORMAL_EDIT_Add,
			BsMax_OT_WEIGHTED_NORMAL_Add,
			BsMax_OT_UV_PROJECT_Add,
			BsMax_OT_UV_WARP_Add,
			BsMax_OT_VERTEX_WEIGHT_EDIT_Add,
			BsMax_OT_VERTEX_WEIGHT_MIX_Add,
			BsMax_OT_VERTEX_WEIGHT_PROXIMITY_Add,
			BsMax_OT_ARRAY_Add,
			BsMax_OT_BEVEL_Add,
			BsMax_OT_BOOLEAN_Add,
			BsMax_OT_BUILD_Add,
			BsMax_OT_DECIMATE_Add,
			BsMax_OT_EDGE_SPLIT_Add,
			BsMax_OT_Mask_Add,
			BsMax_OT_MIRROR_Add,
			BsMax_OT_MULTIRES_Add,
			BsMax_OT_REMESH_Add,
			BsMax_OT_Screw_Add,
			BsMax_OT_SKIN_Add,
			BsMax_OT_SOLIDIFY_Add,
			BsMax_OT_SUBSURF_Add,
			BsMax_OT_TRIANGULATE_Add,
			BsMax_OT_WIREFRAME_Add,
			BsMax_OT_ARMATURE_Add,
			BsMax_OT_CAST_Add,
			BsMax_OT_CURVE_Add,
			BsMax_OT_DISPLACE_Add,
			BsMax_OT_HOOK_Add,
			BsMax_OT_LAPLACIANDEFORM_Add,
			BsMax_OT_LATTICE_Add,
			BsMax_OT_MESH_DEFORM_Add,
			BsMax_OT_SHRINKWRAP_Add,
			BsMax_OT_SIMPLE_DEFORM_Add,
			BsMax_OT_SMOOTH_Add,
			BsMax_OT_CORRECTIVE_SMOOTH_Add,
			BsMax_OT_LAPLACIANSMOOTH_Add,
			BsMax_OT_SURFACE_DEFORM_Add,
			BsMax_OT_WARP_Add,
			BsMax_OT_WAVE_Add,
			BsMax_OT_CLOTH_Add,
			BsMax_OT_COLLISION_Add,
			BsMax_OT_DYNAMIC_PAINT_Add,
			BsMax_OT_EXPLODE_Add,
			BsMax_OT_FLUID_SIMULATION_Add,
			BsMax_OT_OCEAN_Add,
			BsMax_OT_PARTICLE_INSTANCE_Add,
			BsMax_OT_PARTICLE_SYSTEM_Add,
			BsMax_OT_SMOKE_Add,
			BsMax_OT_SOFT_BODY_Add]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)
	return classes

if __name__ == '__main__':
	modifier_cls(True)

__all__ = ["modifier_cls"]