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
from .check import Check
from .label import Label

class CheckBox(BUI):
	def __init__(self,owner,pos=[0,0],size=[80,30],text="",column=0,row=0,
				onmove=None,ondrag=None,
				onpush=None,onrelease=None,
				onclick=None,ondoubleclick=None,
				onrightpush=None,onrightrelease=None,
				onrightclick=None,onmiddleclick=None,
				onmiddlepush=None,onmiddlerelease=None):
		super().__init__(owner=owner,pos=pos,size=size,column=column,row=row,
				onmove=onmove,ondrag=ondrag,
				onpush=onpush,onrelease=onrelease,
				onclick=onclick,ondoubleclick=ondoubleclick,
				onrightpush=onrightpush,onrightrelease=onrightrelease,
				onrightclick=onrightclick,onmiddleclick=onmiddleclick,
				onmiddlepush=onmiddlepush,onmiddlerelease=onmiddlerelease)

		self.caption.hide = True
		self._text = text
		self.pos.auto = True
		self._checked = False
		self.setup()
		owner.append(self)

	def setup(self):		
		w,h = self.size.x,self.size.y
		self.check = Check(self,size=[h,h],column=1,row=1,mode='check')
		self.label = Label(self,size=[w-h,h],column=2,row=1,text=self._text)

	def click(self):
		self.check.checked = self._checked = not self._checked
		self.owner.focus_on(self)
		if self.onclick != None:
			self.onclick()

	@property
	def checked(self):
		return self._checked
	@checked.setter
	def checked(self, checked):
		self.check.checked = self._checked = checked

__all__ = ["CheckBox"]