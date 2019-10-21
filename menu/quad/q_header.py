import bpy
from .q_refrence import QuadMenuRef
from .q_graphic import get_rectangle
from .q_items import ItemShape, ItemText

class QuadHeader:
	def __init__(self, x, y, width, text, mirror):
		self.x = x
		self.y = y
		self.width = width
		self.height = QuadMenuRef.size
		self.text = text
		self.mirror = mirror
		self.controllers = []
		self.create()

	def update(self):
		for c in self.controllers:
			c.update()

	def update_lbl(self):
		for c in self.controllers:
			c.update_lbl()

	def create(self):
		btn_width = self.height
		btn_height = -self.height
		btn_color = QuadMenuRef.hover_color

		btn_x = self.x
		if self.mirror[0]:
			btn_x = self.x - self.height

		btn_y = self.y
		if self.mirror[1]:
			btn_y = self.y + self.height

		btn_v, btn_i = get_rectangle(btn_width, btn_height, btn_x, btn_y)
		button = ItemShape(btn_v, btn_i, btn_color)
		self.controllers.append(button)

		lbl_width = self.width - btn_width
		lbl_height = btn_height
		lbl_color = QuadMenuRef.header_color

		lbl_x = btn_x + btn_width
		if self.mirror[0]:
			lbl_x = btn_x - lbl_width
		lbl_y = btn_y

		lbl_v, lbl_i = get_rectangle(lbl_width, lbl_height, lbl_x, lbl_y)
		label = ItemShape(lbl_v, lbl_i, lbl_color)
		self.controllers.append(label)

		txt_x = lbl_x - 3
		txt_y = lbl_y - QuadMenuRef.size + 3
		txt_color = QuadMenuRef.text_color
		txt = ItemText(txt_x, txt_y, self.text, self.width, txt_color, self.mirror[0])
		self.controllers.append(txt)

	def apply(self):
		# TODO execute header action
		# seprate blue part and gray part action
		# blue call blender menu
		# gray call last action
		#print("header action " + self.text)
		# for now just call blender default
		bpy.ops.bsmax.blenderdefaultmenucall('INVOKE_DEFAULT')

	def mousehover(self, x, y, clicked):
		sxs = self.x
		sxe = self.x + self.width
		if self.mirror[0]:
			sxs = self.x - self.width
			sxe = self.x

		sys = self.y
		sye = self.y + QuadMenuRef.size
		if self.mirror[1]:
			sys = self.y - QuadMenuRef.size
			sye = self.y 
			
		if ((sxs <= x <= sxe) and (sys <= y <= sye)):
			if clicked:
				self.apply()
			return True
		return False

__all__ = ["QuadHeader"]