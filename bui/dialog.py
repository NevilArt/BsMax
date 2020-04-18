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

import bpy, gpu, bgl, blf
from gpu_extras.batch import batch_for_shader
from bpy.types import Operator
from .master.bui import BUI
from .master.classes import Vector2
from .master.graphic import Rectangle
from .button import Button
from .box import Box
from .titlebar import TitleBar

class DlgBox(BUI):
	def __init__(self,owner):
		super().__init__()
		self.owner = owner
		self.pos.auto = True
		self.size.auto = True
		self.table.gap.set(2,2)
		owner._append(self)

class Dialog(Operator,BUI):
	def __init__(self):
		super().__init__(background=True)
		self.handler = None
		self.active_space = None
		self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
		self.escape = False
		self.size.auto = True

		self.focus = self
		self.escape = True
		self.caption.hide = True
		self.table.gap.set(4,4)

		self.box = DlgBox(self)
		self.titlebar = TitleBar(self)
		self.table.create()

		self.background.color.set((0.13,0.13,0.13,1),(0.13,0.13,0.13,1),(0.13,0.13,0.13,1))
		self.background.fillet.set(9,9,9,9)

	def redraw(self):
		self.table.update()
		self.titlebar.size.x = self.box.size.x
		self.background.width = self.size.x
		self.background.height = self.size.y
		self.titlebar.caption += self.caption
		self.update()

		for graphic in self.get_graphics():
			self.shader.bind()
			vertices, indices, color = graphic.get_shape()
			batch = batch_for_shader(self.shader,'TRIS',{"pos":vertices},indices=indices)
			self.shader.uniform_float("color", color)
			batch.draw(self.shader)

		for caption in self.get_captions():
			if not caption.hide:
				blf.size(0,caption.font_size,72)
				location = caption.location()
				blf.position(0,location.x,location.y,0)
				blf.color(0,1,1,1,1)
				blf.draw(0,caption.text)

	def modal(self, ctx, event):
		if ctx.area:
			ctx.area.tag_redraw()

		if self.destroy or (event.type in {'ESC'} and self.escape):
			self.unregister()
			return {'CANCELLED'}

		if event.type == 'MOUSEMOVE':
			self.hover = True if self.grab else self.mouse.is_hover(self,event)

		self.mouse.get_action(self,event)

		if not self.hover and not self.grab:
			self.reset()
			return {'PASS_THROUGH'}

		self.focus.kb.get_action(self,event)
		return {'RUNNING_MODAL'}

	def unregister(self):
		if self.handler != None:
			self.active_space.draw_handler_remove(self.handler,"WINDOW")

	def append(self,controller):
		self.box.append(controller)

	def open(self):
		pass
	def close(self):
		pass

	def convert_setting(self):
		if self.caption.text == "":
			self.caption.text = self.bl_label
	
		if self.pos == Vector2(0,0):
			#TODO get center of the screen
			self.pos.set(250,250)

		self.size.auto = True if self.size == Vector2(0,0) else False
		self.table.update()

	def invoke(self, ctx, event):
		ctx.window_manager.modal_handler_add(self)
		self.active_space = ctx.area.spaces.active
		self.handler = self.active_space.draw_handler_add(self.redraw,(),'WINDOW','POST_PIXEL')
		self.setup() # read user data
		self.convert_setting()
		self.open() # reserved function
		return {'RUNNING_MODAL'}

__all__ = ["Dialog"]