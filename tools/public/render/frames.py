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
from bpy.app.handlers import persistent

class RENDER_PT_frames(bpy.types.Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "output"
	bl_label = "Frames"
	bl_parent_id = "RENDER_PT_dimensions"
	COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

	def draw(self, ctx):
		layout = self.layout
		col = layout.column(align=True)
		col.label(text="Render only this frames")
		row = col.row(align=True)
		row.prop(ctx.scene, "frames", text="")
		row.prop(ctx.scene, "use_frames", text="")

class BitArray:
	def __init__(self):
		self.string = ""
		self.ints = []
	
	def get_string(self, frames):
		""" check the string first """
		self.string = ""
		for l in frames:
			if l in '0123456789,-':
				self.string += l

		""" convert strings to integers """
		self.string = self.string.strip()
		ranges = self.string.split(",")
		numstr = [r.split("-") for r in ranges]
		self.ints.clear()
		for n in numstr:
			if len(n) == 1:
				if n[0] != '':
					self.ints.append(int(n[0]))
			elif len(n) == 2:
				n1,n2 = int(n[0]),int(n[1])
				if n2 > n1:
					for i in range(n1,n2+1):
						self.ints.append(i)
		self.ints.sort()

class Scene_Data:
	def __init__(self):
		self.frame_start = 0
		self.frame_end = 0
	def store(self,scene):
		self.frame_start = int(scene.frame_start)
		self.frame_end = int(scene.frame_end)
	def restore(self,scene):
		scene.frame_start = self.frame_start
		scene.frame_end = self.frame_end

sd = Scene_Data()
ba = BitArray()
	
@persistent
def frames_render_init(scene):
	if scene.use_frames:
		sd.store(scene)
		ba.get_string(scene.frames)
		scene.frame_current = scene.frame_start = min(ba.ints)
		scene.frame_start = min(ba.ints)
		scene.frame_end = max(ba.ints)*10

@persistent
def frames_render_complete(scene):
	if scene.use_frames:
		sd.restore(scene)

@persistent
def check_render_frame(scene):
	if scene.use_frames:
		if len(ba.ints) > 0:
			scene.frame_current = ba.ints[0]
			ba.ints.pop(0)
		
def register_frames():
	bpy.types.Scene.frames = bpy.props.StringProperty()
	bpy.types.Scene.use_frames = bpy.props.BoolProperty()
	bpy.utils.register_class(RENDER_PT_frames)
	bpy.app.handlers.render_init.append(frames_render_init)
	bpy.app.handlers.render_complete.append(frames_render_complete)
	bpy.app.handlers.render_pre.append(check_render_frame)

def unregister_frames():
	bpy.app.handlers.render_pre.remove(check_render_frame)
	bpy.app.handlers.render_init.remove(frames_render_init)
	bpy.app.handlers.render_complete.remove(frames_render_complete)
	bpy.utils.unregister_class(RENDER_PT_frames)

if __name__ == "__main__":
	try:
		unregister_frames()
	except:
		pass
	register_frames()