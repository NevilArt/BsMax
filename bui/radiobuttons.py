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
from .master.bui import BUI
from .master.graphic import Rectangle
from .master.caption import Caption
from .checkbox import CheckBox
from .box import Box
from .check import Check
from .label import Label


class RadioButtons(BUI):
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

		self.pos.auto = True
		self.size.auto = True
		""" special variables """
		self._selected = 0
		self.default = 0
		self.setup()
		owner.append(self)

	def add(self,text="",row=0,column=0):
		""" get radio size """
		caption = Caption(None,text=text,font_size=self.caption.font_size)
		w,h = max(80,caption.size.x), max(20,caption.size.y)

		frame = Box(self,size=[w+h+10,h+10],column=column,row=row,onclick=self.picked)

		w,h = frame.size.x,frame.size.y
		frame.check = Check(frame,size=[h,h],column=1,row=1,mode='radio')
		frame.check.checked = len(self.controllers)-1 == self.default
		frame.label = Label(frame,size=[w-h,h],column=2,row=1,text=text)

		return frame
		
	def setup(self):
		pass

	def picked(self):
		for index,rb in enumerate(self.controllers):
			rb.check.checked = (rb == self.active)
			if rb.check.checked:
				self._selected = index

	def click(self):
		self.owner.focus_on(self)
		if self.onclick != None:
			self.onclick()

	@property
	def selected(self):
		return self._selected
	@selected.setter
	def selected(self, selected):
		if selected != self._selected:
			if 0 < selected < len(self.controllers):
				for rb in self.controllers:
					rb.check.checked = False
				self.controllers[selected].check.checked = True
				self._selected = selected

__all__ = ["RadioButtons"]