############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

from .master.bui import BUI
from .master.classes import Vector2,Range
from .master.graphic import Rectangle
from .button import Button

class Slider(BUI):
	def __init__(self,owner,pos=[0,0],size=[80,30],text="",column=0,row=0,
				onmove=None,ondrag=None,
				onpush=None,onrelease=None,
				onclick=None,ondoubleclick=None,
				onrightpush=None,onrightrelease=None,
				onrightclick=None,onmiddleclick=None,
				onmiddlepush=None,onmiddlerelease=None):
		super().__init__(owner=owner,pos=pos,size=size,text=text,column=column,row=row,
				onmove=onmove,ondrag=ondrag,
				onpush=onpush,onrelease=onrelease,
				onclick=onclick,ondoubleclick=ondoubleclick,
				onrightpush=onrightpush,onrightrelease=onrightrelease,
				onrightclick=onrightclick,onmiddleclick=onmiddleclick,
				onmiddlepush=onmiddlepush,onmiddlerelease=onmiddlerelease)

		self.body = Rectangle(self)
		self.body.color.set((0.219,0.219,0.219,1),(0.219,0.219,0.219,1),(0.219,0.219,0.219,1))

		self.x = Range(0,100,20)
		self.y = Range(0,100,20)
		self.setup()
		owner.append(self)

	def setup(self):
		self.handel = Button(self,size=[30,30])
		self.handel.table.ignore = True
		self.handel.body.fillet.set(15,15,15,15)
		self.handel.moveable = True
		self.handel.ondrag = self.handel_draged
		self.handel.onrightclick = self.joy_rightclick
		self.body.fillet.set(15,15,15,15)

	def handel_draged(self):
		start = Vector2(self.location.x,self.location.y)
		current = Vector2(self.handel.location.x, self.handel.location.y)
		end = Vector2(self.location.x+self.size.x-self.handel.size.x,
			self.location.y+self.size.y-self.handel.size.y)

		length = Vector2(self.x.get_lenght(), self.y.get_lenght())

		if end.x-start.x != 0:
			self.x.value = self.x.min+length.x*((current.x-start.x)/(end.x-start.x))
		else:
			self.x.value = 0

		if end.y-start.y != 0:
			self.y.value = self.y.min+length.y*((current.y-start.y)/(end.y-start.y))
		else:
			self.y.value = 0

		if self.ondrag != None:
			self.ondrag()

	def reset(self):
		self.x.reset()
		self.y.reset()

	def joy_rightclick(self):
		if self.onrightclick != None:
			self.onrightclicked()
		else:
			self.reset()

	def update(self):
		if self.owner != None:
			self.body.size = self.size
		if not self.handel.mouse.lmb.grab:
			length = Vector2(self.size.x-self.handel.size.x,self.size.y-self.handel.size.y)
			percent = Vector2(self.x.get_position_percet(),self.y.get_position_percet())
			self.handel.pos.set(length.x*percent.x, length.y*percent.y)
		self._update()

__all__ = ["Slider"]