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
from .classes import Vector2

class MouseButton:
	def __init__(self):
		self.pressed = False
		self.grab = False
		self.pos = Vector2(0,0)
	def delta(self,x,y):
		return x-self.pos.x, y-self.pos.y

class Mouse:
	def __init__(self):
		self.rmb = MouseButton()
		self.mmb = MouseButton()
		self.lmb = MouseButton()
		self.pos = Vector2(0,0)
	
	def delta(self,x,y):
		return x-self.pos.x,y-self.pos.y
	
	def is_hover(cls,self,event,deep=True):
		if self.enabled and self.touchable:
			mx,my = event.mouse_region_x, event.mouse_region_y
			x,y = self.location.x, self.location.y
			w,h = self.size.x, self.size.y
			hover = (x < mx < x+w and y < my < y+h)
			if hover:
				if deep:
					self.active = self
					for c in self.controllers:
						if c.mouse.is_hover(c,event):
							self.active = c if c.active == c else c.active
							break
				if self.scale.enabled:
					s, scale = self.scale.sensitive, self.scale
					if scale.top:
						scale.touched.top = y+h-s < my < y+h
					if scale.bottom:
						scale.touched.bottom = y < my < y+s
					if scale.left:
						scale.touched.left = x < mx < x+s
					if scale.right:
						scale.touched.right = x+w-s < mx < x+w
			return hover
		return False

	def get_action(cls,self,event):
		if self.enabled:
			""" read mouse """
			x,y = event.mouse_region_x, event.mouse_region_y

			if event.type == 'LEFTMOUSE' and self.hover:
				if event.value == 'PRESS':
					self.grab = True
					self.mouse.lmb.pressed = True
					self.mouse.lmb.pos = Vector2(x,y)
					self.active.push()
					self.active.mouse.lmb.grab = True
				if event.value =='RELEASE':
					self.grab = False
					self.mouse.lmb.pressed = False
					self.active.mouse.lmb.grab = False
					self.active.release()
					if self.active.mouse.is_hover(self,event,deep=False):
						self.active.click()

			if event.type == 'MIDDLEMOUSE':
				if event.value == 'PRESS':
					self.mouse.mmb.pressed = True
					self.mouse.mmb.pos = Vector2(x,y)
					self.active.middlepush()
				if event.value =='RELEASE':
					self.mouse.mmb.pressed = False
					self.active.middlerelease()
					if self.active.mouse.is_hover(self,event,deep=False):
						self.active.middleclick()

			if event.type == 'RIGHTMOUSE':
				if event.value == 'PRESS':
					self.mouse.rmb.pressed = True
					self.mouse.rmb.pos = Vector2(x,y)
					self.active.rightpush()
				if event.value =='RELEASE':
					self.mouse.rmb.pressed = False
					self.active.rightrelease()
					if self.active.mouse.is_hover(self,event,deep=False):
						self.active.rightclick()

			if event.type == 'MOUSEMOVE':
				dx,dy = self.mouse.delta(x,y)
				if dx != 0 or dy != 0:
					if self.mouse.lmb.pressed:
						if self.active.scale.enabled and self.active.scale.touched.any():
							self.active.resize(self.active.scale.touched,Vector2(dx,dy))
						else:
							self.active.drag(dx,dy)
					elif self.hover:
						self.active.move(dx,dy)
				self.mouse.pos = Vector2(x,y)

			if self.active != None:
				self.active.state = 2 if self.mouse.lmb.pressed else 1 if self.hover else 0


class Keyboard:
	def __init__(self):
		self.ctrl = False
		self.shift = False
		self.alt = False
		self.str = ""

	def get_action(cls,self,event):
		if self.enabled:
			""" get keys state """
			if event.type in {'LEFT_SHIFT','RIGHT_SHIFT'}:
				if event.value == 'PRESS':
					cls.shift = True
				if event.value == 'RELEASE':
					cls.shift = False

			if event.type in {'LEFT_CTRL','RIGHT_CTRL'}:
				if event.value == 'PRESS':
					cls.ctrl = True
				if event.value == 'RELEASE':
					cls.ctrl = False

			if event.type in {'LEFT_ALT','RIGHT_ALT'}:
				if event.value == 'PRESS':
					cls.alt = True
				if event.value == 'RELEASE':
					cls.alt = False
			
			nums = ['ZERO','ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE']
			letters = ['A','B','C','D','E','F','G','H','I','J','K','L',
					'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

			if event.type in letters and event.value == 'PRESS':
				cls.str += event.type if cls.shift else event.type.lower()
			if event.type in nums and event.value == 'PRESS':
				for i in range(len(nums)):
					if event.type == nums[i]:
						cls.str += str(i)
			if event.type == 'DEL' and event.value == 'PRESS':
				cls.str = ""


__all__ = ["Keyboard", "Mouse"]