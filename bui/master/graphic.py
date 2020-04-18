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

from math import sin,cos,pi
from .classes import Colors,Vector2,Corner,Edge,Align

class Graphic:
	def __init__(self,owner):
		self.color = Colors()
		self.vertices = []
		self.indices = []
		self.hide = False
		self.owner = owner
		self.offset = Vector2(0,0)
		self.align = Align(False,False,False,False,True)
		owner.graphics.append(self)
	def is_updated(self):
		return True
	def create_shape(self):
		x = self.owner.location.x+self.offset.x
		y = self.owner.location.y+self.offset.y
		w = self.owner.size.x
		h = self.owner.size.y
		self.vertices = ((x,y),(x+w,y),(x+w,y+h),(x,y+h))
		self.indices = ((0,1,2),(2,3,0))
	def get_shape(self):
		if self.hide:
			return [],[],(0,0,0,0)
		if self.is_updated():
			self.create_shape()
		return self.vertices, self.indices, self.color.get(self.owner.state)
		
class Rectangle(Graphic):
	def __init__(self,owner,width=0,height=0,fillet=[0,0,0,0]):
		super().__init__(owner)
		self.width = width
		self._width = width
		self.height = height
		self._height = height
		ul,ur,dl,dr = fillet
		self.fillet = Corner(ul,ur,dl,dr)
		self._fillet = Corner(ul,ur,dl,dr)
		self.create_shape()

	def is_updated(self):
		return self.width == self._width and\
			self.height == self._height and\
			self.fillet == self._fillet
	def updated(self):
		self._width = self.width
		self._height = self.height
		self._fillet = self.fillet.copy()

	def get_start_angle(self,dirx,diry):
		if dirx == 1 and diry == -1:
			return pi/2
		elif dirx == -1 and diry == -1:
			return pi
		elif dirx == -1 and diry == 1:
			return pi*1.5
		else:
			return 0

	def get_corner(self, orig, width, height, radius, dirx, diry):
		verts = []
		x1 = (width-radius)*dirx
		x2 = width*dirx
		y1 = (height-radius)*diry
		y2 = height*diry
		if radius > 0:
			s = self.get_start_angle(dirx,diry)
			div = 1 if radius < 10 else 3
			eges = radius/div
			steep = (pi/2)/eges
			for i in range(int(eges)):
				d = s+i*steep if i < int(eges)-1 else s+pi/2
				x = x1+sin(d)*radius
				y = y1+cos(d)*radius
				verts.append([x,y])
		else:
			verts.append([x2,y2])
		for i in range(len(verts)):
			verts[i][0] += orig.x
			verts[i][1] += orig.y
		return verts

	def create_shape(self):
		width,height = self.width,self.height
		size = Vector2(width,height)
		pos = self.owner.location + self.offset + self.align.location(self.owner.size,size)
		
		verts,inds = [],[]
		center = Vector2(pos.x+width/2,pos.y+height/2)
		verts.append((center.x,center.y))
		
		verts += self.get_corner(center,width/2,height/2,self.fillet.top_right,1,1)
		verts += self.get_corner(center,width/2,height/2,self.fillet.bottom_right,1,-1)
		verts += self.get_corner(center,width/2,height/2,self.fillet.bottom_left,-1,-1)
		verts += self.get_corner(center,width/2,height/2,self.fillet.top_left,-1,1)

		count = len(verts)
		for i in range(1,count):
			if i < count-1:
				inds.append((0,i,i+1))
			else:
				inds.append((0,i,1))
		self.vertices = verts
		self.indices = inds
		self.updated()

class Circle:
	def __init__(self,radius=0):
		def __init__(self,owner):
			super().__init__(owner)
			self.radius = radius
			self._radius = radius
	def is_updated(self):
		return self.radius == self._radius
	def create_shape(self):
		x,y = self.owner.location.x, self.owner.location.y
		w,h = self.owner.size.x, self.owner.size.y
		self.vertices = ((x,y),(x+w,y),(x+w,y+h),(x,y+h))
		self.indices = ((0,1,2),(2,3,0))

class Gride:
	def __init__(self):
		def __init__(self,owner):
			super().__init__(owner)
			self.count = Vector2(1,1)
	def is_updated(self):
		return True
	def create_shape(self,pos,size,state):
		self.state = state
		x,y = pos.x+self.offset.x, pos.y+self.offset.y
		w,h = self.size.x, self.size.y
		self.vertices = ((x,y),(x+w,y),(x+w,y+h),(x,y+h))
		self.indices = ((0,1,2),(2,3,0))

__all__ = ["Rectangle", "Gride"]