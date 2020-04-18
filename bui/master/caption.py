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
import blf
from .classes import Vector2,Colors,Align

class Caption:
	def __init__(self,owner,text="",font="",font_size=12):
		self.owner = owner
		self.text = text
		self._text = ""
		self._size = Vector2(0,0)
		self.font = font
		self.font_size = font_size
		self._font_size = 0
		self.pos = Vector2(0,0)
		self.offset = Vector2(0,0)
		self.color = Colors()
		self.align = Align(False,False,False,False,True)
		self.hide = False
	def __iadd__(self, targ):
		self.text = targ.text
		self.font = targ.font
		self.font_size = targ.font_size
		self.pos = targ.pos.copy()
		return self
	
	@property
	def size(self):
		""" get size from font size and text lenght """
		""" recalculate when text or font_size changes """
		if self.text != self._text or self.font_size != self._font_size:
			w,h = blf.dimensions(0,self.text)
			self._size.set(w,h)
			self._text = self.text
			self._font_size = self.font_size
		return self._size

	def location(self):
		""" get location from parent location and alignment """
		if self.owner != None:
			return self.owner.location+self.align.location(self.owner.size,self.size)+self.offset
		else:
			return self.pos