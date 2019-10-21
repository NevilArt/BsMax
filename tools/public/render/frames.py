import bpy
from bpy.types import Operator, Panel
from bpy.props import StringProperty

# TODO need to make a better method that works with net render

def fix_string_intarray(string):
	newstring = ""
	for l in string:
		if l in {'0','1','2','3','4','5','6','7','8','9',',','-'}:
			newstring += l
	return newstring

def get_str_from_int(num, count):
	string = str(num)
	for i in range(len(string), count):
		string = "0" + string
	return string

def get_int_array_from_string(string):
	string = string.strip()
	ranges = string.split(",")
	numstr = [r.split("-") for r in ranges]
	numint = []
	for n in numstr:
		if len(n) == 1:
			if n[0] != '':
				numint.append(int(n[0]))
		elif len(n) == 2:
			n1 = int(n[0])
			n2 = int(n[1])
			if n2 > n1:
				for i in range(n1, n2+1):
					numint.append(i)
	return numint

class BsMax_OT_RenderFrames(Operator):
	bl_idname = "render.renderframes"
	bl_label = "Render Frames"

	frames = []
	filepath = ""
	index = 0

	def modal(self, ctx, event):
		if event.type == 'ESC' or self.index >= len(self.frames):
			ctx.scene.render.filepath = self.filepath
			return {'CANCELLED'}
		if ctx.scene.camera != None:
			frame = self.frames[self.index]
			ctx.scene.frame_set(frame)
			bpy.ops.wm.redraw_timer(type='DRAW', iterations=1, time_limit=0)
			ctx.scene.render.filepath = self.filepath + get_str_from_int(frame, 4)
			bpy.ops.render.render(write_still=True)
			self.index += 1
		return {'RUNNING_MODAL'}

	def invoke(self, ctx, event):
		scene = ctx.scene
		self.filepath = scene.render.filepath
		scene.frames = fix_string_intarray(scene.frames)
		self.frames = get_int_array_from_string(scene.frames)
		ctx.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class RENDER_PT_frames(Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "output"
	bl_label = "Frames"
	bl_parent_id = "RENDER_PT_dimensions"
	COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

	def draw(self, ctx):
		layout = self.layout
		col = layout.column(align=True)
		col.prop(ctx.scene, "frames", text="")
		col.operator("render.renderframes")

def frames_cls(register):
	bpy.types.Scene.frames = StringProperty()
	classes = [BsMax_OT_RenderFrames, RENDER_PT_frames]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	frames_cls(True)

__all__ = ["frames_cls"]