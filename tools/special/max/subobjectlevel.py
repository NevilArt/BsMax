import bpy
from bpy.types import Operator
from bpy.props import IntProperty

def set(mode):
	bpy.ops.object.mode_set(mode=mode)
def mesh(ctx,v,e,f):
	ctx.tool_settings.mesh_select_mode = v,e,f

class BsMax_OT_SubobjectLevel(Operator):
	bl_idname = "bsmax.subobjectlevel"
	bl_label = "Subobject Level"
	level: IntProperty(name="SubobjectLevel")

	@classmethod
	def poll(self, ctx):
		return ctx.active_object != None

	def execute(self, ctx):  
		activeobj = ctx.active_object
		objops = bpy.ops.object
		mode = ctx.mode
		if activeobj != None:
			v,e,f = ctx.tool_settings.mesh_select_mode
			if activeobj.type == 'MESH':
				if self.level == 1: # Vertex mode
					if mode == "EDIT_MESH" and v:
						set('OBJECT')
					else: 
						set('EDIT')
						mesh(ctx,True,False,False)
				elif self.level == 2: # Edge mode
					if mode == "EDIT_MESH" and e:
						set('OBJECT')
					else: 
						set('EDIT')
						mesh(ctx,False,True,False)
				#elif self.level == 3: # Reserved for Border mode
				#    # this is reserved for border mode for now just act as edge mode
				#    if mode == "EDIT_MESH" and e:
				#        set('OBJECT')
				#    else:
				#        set('EDIT')
				#        mesh(ctx,False,True,False)
				elif self.level == 3: # Mesh mode
					if mode == "EDIT_MESH" and f:
						set('OBJECT')
					else:
						set('EDIT')
						mesh(ctx,False,False,True)
				#elif self.level == 5: # Reserved for Element mode
				#    # this is reserved for Element mode for now act as Face mode
				#    if mode == "EDIT_MESH" and f:
				#        set('OBJECT')
				#    else:
				#        set('EDIT')
				#        mesh(ctx,False,False,True)
				elif self.level == 6:
					set('OBJECT')
				# this do not have similar in 3D Max
				elif self.level == 7:
					if mode == "SCULPT": 
						set('OBJECT')
					else: 
						set('SCULPT')
				elif self.level == 8:
					if mode == "PAINT_VERTEX":
						set('OBJECT')
					else:
						set('VERTEX_PAINT')
				elif self.level == 9:
					if mode == "PAINT_WEIGHT":
						set('OBJECT')
					else: 
						set('WEIGHT_PAINT')
				elif self.level == 0:
					if mode == "PAINT_TEXTURE": 
						set('OBJECT')
					else: 
						set('TEXTURE_PAINT')
			elif activeobj.type == 'SURFACE':
				if self.level == 1:
					if mode == "EDIT_SURFACE": 
						set('OBJECT')
					else: 
						set('EDIT')
				elif self.level == 0 or self.level >= 2: 
					set('OBJECT')

			elif activeobj.type == 'CURVE':
				if self.level == 1:
					if mode == "EDIT_CURVE": 
						set('OBJECT')
					else: 
						set('EDIT')
				elif self.level == 0 or self.level >= 2: 
					set('OBJECT')

			elif activeobj.type == 'META':
				if self.level == 1:
					if mode == "EDIT_METABALL": 
						set('OBJECT')
					else: 
						set('EDIT')
				elif self.level == 0 or self.level >= 2: 
					set('OBJECT')

			elif activeobj.type == 'LATTICE':
				if self.level == 1:
					if mode == "EDIT_LATTICE": 
						set('OBJECT')
					else: 
						set('EDIT')
				elif self.level == 0 or self.level >= 2: 
					set('OBJECT')

			elif activeobj.type == 'ARMATURE':
				if self.level == 1:
					if mode == "EDIT_ARMATURE":
						set('OBJECT')
					else:
						set('EDIT')
				elif self.level == 2:
					if mode == "POSE":
						set('OBJECT')
					else:
						set('POSE')
				elif self.level == 0 or self.level >= 3:
					set('OBJECT')

			elif activeobj.type == 'GPENCIL':
				if self.level == 1:
					if mode == 'GPENCIL_EDIT':
						set('OBJECT')
					else:
						set('GPENCIL_EDIT')
				elif self.level == 2:
					if mode == 'GPENCIL_SCULPT':
						set('OBJECT')
					else:
						set('GPENCIL_SCULPT')
				elif self.level == 3:
					if mode == 'GPENCIL_PAINT':
						set('OBJECT')
					else:
						set('GPENCIL_PAINT')
				elif self.level == 4:
					if mode == 'GPENCIL_WEIGHT':
						set('OBJECT')
					else:
						set('GPENCIL_WEIGHT')
				elif self.level > 4:
					set('OBJECT')
		return{"FINISHED"}

def subobjectlevel_cls(register):
	classes = [BsMax_OT_SubobjectLevel]
	if register:
		[bpy.utils.register_class(c) for c in classes]
	else:
		[bpy.utils.unregister_class(c) for c in classes]

if __name__ == '__main__':
	subobjectlevel_cls(True)

__all__ = ["subobjectlevel_cls"]