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
from mathutils import Vector
from bsmax.graphic import register_line,unregister_line,get_screen_pos

def get_center(objs):
	location = Vector((0,0,0))
	for obj in objs:
		location += obj.matrix_world.translation
	return location / len(objs)

class Object_OT_Link_to(bpy.types.Operator):
	""" this class mimics the 3DsMax link to operator """
	bl_idname = "object.link_to"
	bl_label = "Link to"
	bl_options = {'REGISTER', 'UNDO'}

	handle = None
	start, center, end = None, Vector((0,0,0)), None
	children, parent = [], None

	def modal(self, ctx, event):
		ctx.area.tag_redraw()
		if not event.type in {'LEFTMOUSE','RIGHTMOUSE', 'MOUSEMOVE', 'ESC'}:
			return {'PASS_THROUGH'}
		
		elif event.type == 'MOUSEMOVE':
			""" update the line coordinate """
			""" self.center is a 3D coordinate """
			self.start = get_screen_pos(ctx,self.center) 
			self.end = event.mouse_region_x, event.mouse_region_y

		elif event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				""" clear all selection """
				bpy.ops.object.select_all(action='DESELECT')
				ctx.view_layer.objects.active = None
				
				""" Pick new object as target """
				coord = event.mouse_region_x, event.mouse_region_y
				bpy.ops.view3d.select(extend=False,location=coord)

				""" Ignore selected obects as target """
				if ctx.active_object in self.children:
					ctx.view_layer.objects.active = None

			if event.value =='RELEASE':
				""" if target selected do parenting """
				if ctx.view_layer.objects.active != None:
					self.finish(ctx, event)

			return {'RUNNING_MODAL'}

		elif event.type in {'RIGHTMOUSE','ESC'}:
			unregister_line(self.handle)
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}
	
	def setup(self, ctx, event):
		self.children = ctx.selected_objects.copy()
		self.center = get_center(self.children)
		self.start = self.end = event.mouse_region_x, event.mouse_region_y
		bpy.ops.object.select_all(action='DESELECT')
		ctx.view_layer.objects.active = None
	
	def finish(self, ctx, event):
		parent_object = ctx.view_layer.objects.active
		bpy.ops.object.select_all(action='DESELECT')
		
		for obj in self.children:
			if parent_object.parent == obj:
				location = parent_object.matrix_world.translation.copy()
				parent_object.parent = None
				parent_object.location = location
		
			obj.parent = parent_object
			obj.matrix_parent_inverse = parent_object.matrix_world.inverted()
		
		parent_object.select_set(state=True)
		self.children.clear()
		self.children.append(parent_object)
		self.setup(ctx, event)

	def invoke(self, ctx, event):
		self.setup(ctx, event)
		self.handle = register_line(ctx, self, '2d', (1, 0.5, 0.5, 1))
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

# hasattr(bpy.types, bpy.ops.object.link_to.idname())

def linkto_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.link_to",icon="LINKED")

def register_linkto():
	bpy.utils.register_class(Object_OT_Link_to)
	bpy.types.VIEW3D_MT_object_parent.append(linkto_menu)

def unregister_linkto():
	bpy.types.VIEW3D_MT_object_parent.remove(linkto_menu)
	bpy.utils.unregister_class(Object_OT_Link_to)

if __name__ == "__main__":
	register_linkto()