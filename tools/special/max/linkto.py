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
		location += obj.location
	return location / len(objs)

class Object_OT_Link_to(bpy.types.Operator):
	bl_idname = "object.link_to"
	bl_label = "Link to"
	bl_options = {'REGISTER', 'UNDO'}

	center = None
	start, end, handle = None, None, None
	selected_objects = []

	@classmethod
	def poll(self, ctx):
		return len(ctx.selected_objects) > 0

	def modal(self, ctx, event):
		ctx.area.tag_redraw()
		if not event.type in {'LEFTMOUSE','RIGHTMOUSE', 'MOUSEMOVE','ESC'}:
			return {'PASS_THROUGH'}
		
		elif event.type == 'MOUSEMOVE':
			self.start = get_screen_pos(ctx,self.center)
			self.end = event.mouse_region_x, event.mouse_region_y

		elif event.type == 'LEFTMOUSE':
			if event.value == 'PRESS':
				""" remove all selected and active object """
				bpy.ops.object.select_all(action='DESELECT')
				ctx.view_layer.objects.active = None
				
				""" Pick new object as target """
				coord = event.mouse_region_x, event.mouse_region_y
				bpy.ops.view3d.select(extend=False,location=coord)

				""" Ignore selected obects as target """
				if ctx.active_object in self.selected_objects:
					ctx.view_layer.objects.active = None

			if event.value =='RELEASE':

				""" Restore selection """
				for obj in self.selected_objects:
					if obj != ctx.active_object:
						obj.select_set(True)
				
				""" if target selected call the operator """
				if ctx.view_layer.objects.active != None:
					""" TODO replace with clear code """
					""" check dependency first then link do parenting """
					bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
					return {'CANCELLED'}

			return {'RUNNING_MODAL'}

		elif event.type in {'RIGHTMOUSE','ESC'}:
			unregister_line(self.handle)
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		""" Store selected objects """
		self.selected_objects = ctx.selected_objects.copy()
		self.center = get_center(self.selected_objects)
		self.start = self.end = event.mouse_region_x, event.mouse_region_y
		self.handle = register_line(ctx, self, '2d', (1, 0.5, 0.5, 1))
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

# hasattr(bpy.types, bpy.ops.object.link_to.idname())

def register_linkto():
	bpy.utils.register_class(Object_OT_Link_to)

def unregister_linkto():
	bpy.utils.unregister_class(Object_OT_Link_to)

if __name__ == "__main__":
	register_linkto()