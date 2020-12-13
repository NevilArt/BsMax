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
from bpy.props import IntProperty

class Object_OT_SubobjectLevel(bpy.types.Operator):
	bl_idname = "object.subobject_level"
	bl_label = "Subobject Level"
	level: IntProperty(name="SubobjectLevel")

	@classmethod
	def poll(self, ctx):
		return ctx.active_object != None
	
	def set(self, mode):
		bpy.ops.object.mode_set(mode=mode)
	
	def mesh(self, ctx,v,e,f):
		ctx.tool_settings.mesh_select_mode = v,e,f

	def execute(self, ctx):  
		activeobj = ctx.active_object
		mode = ctx.mode
		if activeobj != None:
			v,e,f = ctx.tool_settings.mesh_select_mode
			if activeobj.type == 'MESH':
				if self.level == 1: # Vertex mode
					if mode == "EDIT_MESH" and v:
						self.set('OBJECT')
					else: 
						self.set('EDIT')
						self.mesh(ctx,True,False,False)
				elif self.level == 2: # Edge mode
					if mode == "EDIT_MESH" and e:
						self.set('OBJECT')
					else: 
						self.set('EDIT')
						self.mesh(ctx,False,True,False)
				#elif self.level == 3: # Reserved for Border mode
				#    # this is reserved for border mode for now just act as edge mode
				#    if mode == "EDIT_MESH" and e:
				#        self.set('OBJECT')
				#    else:
				#        self.set('EDIT')
				#        self.mesh(ctx,False,True,False)
				elif self.level == 3: # Mesh mode
					if mode == "EDIT_MESH" and f:
						self.set('OBJECT')
					else:
						self.set('EDIT')
						self.mesh(ctx,False,False,True)
				#elif self.level == 5: # Reserved for Element mode
				#    # this is reserved for Element mode for now act as Face mode
				#    if mode == "EDIT_MESH" and f:
				#        self.set('OBJECT')
				#    else:
				#        self.set('EDIT')
				#        self.mesh(ctx,False,False,True)
				elif self.level == 6:
					self.set('OBJECT')
				# this do not have similar in 3D Max
				elif self.level == 7:
					if mode == "SCULPT": 
						self.set('OBJECT')
					else: 
						self.set('SCULPT')
				elif self.level == 8:
					if mode == "PAINT_VERTEX":
						self.set('OBJECT')
					else:
						self.set('VERTEX_PAINT')
				elif self.level == 9:
					if mode == "PAINT_WEIGHT":
						self.set('OBJECT')
					else: 
						self.set('WEIGHT_PAINT')
				elif self.level == 0:
					if mode == "PAINT_TEXTURE": 
						self.set('OBJECT')
					else: 
						self.set('TEXTURE_PAINT')
			elif activeobj.type == 'SURFACE':
				if self.level == 1:
					if mode == "EDIT_SURFACE": 
						self.set('OBJECT')
					else: 
						self.set('EDIT')
				elif self.level == 0 or self.level >= 2: 
					self.set('OBJECT')

			elif activeobj.type == 'CURVE':
				if self.level == 1:
					if mode == "EDIT_CURVE": 
						self.set('OBJECT')
					else: 
						self.set('EDIT')
				elif self.level == 0 or self.level >= 2: 
					self.set('OBJECT')

			elif activeobj.type == 'META':
				if self.level == 1:
					if mode == "EDIT_METABALL": 
						self.set('OBJECT')
					else: 
						self.set('EDIT')
				elif self.level == 0 or self.level >= 2: 
					self.set('OBJECT')

			elif activeobj.type == 'LATTICE':
				if self.level == 1:
					if mode == "EDIT_LATTICE": 
						self.set('OBJECT')
					else: 
						self.set('EDIT')
				elif self.level == 0 or self.level >= 2: 
					self.set('OBJECT')

			elif activeobj.type == 'ARMATURE':
				if self.level == 1:
					if mode == "EDIT_ARMATURE":
						self.set('OBJECT')
					else:
						self.set('EDIT')
				elif self.level == 2:
					if mode == "POSE":
						self.set('OBJECT')
					else:
						self.set('POSE')
				elif self.level == 0 or self.level >= 3:
					self.set('OBJECT')

			elif activeobj.type == 'GPENCIL':
				if self.level == 1:
					if mode == 'GPENCIL_EDIT':
						self.set('OBJECT')
					else:
						self.set('GPENCIL_EDIT')
				elif self.level == 2:
					if mode == 'GPENCIL_SCULPT':
						self.set('OBJECT')
					else:
						self.set('GPENCIL_SCULPT')
				elif self.level == 3:
					if mode == 'GPENCIL_PAINT':
						self.set('OBJECT')
					else:
						self.set('GPENCIL_PAINT')
				elif self.level == 4:
					if mode == 'GPENCIL_WEIGHT':
						self.set('OBJECT')
					else:
						self.set('GPENCIL_WEIGHT')
				elif self.level > 4:
					self.set('OBJECT')
		return{"FINISHED"}

def register_subobjectlevel():
	bpy.utils.register_class(Object_OT_SubobjectLevel)

def unregister_subobjectlevel():
	bpy.utils.unregister_class(Object_OT_SubobjectLevel)