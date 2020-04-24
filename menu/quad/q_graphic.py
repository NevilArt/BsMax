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

def get_rectangle(width, height, x, y):
	verts = ((x,y),(x+width,y),(x+width,y+height),(x,y+height))
	faces = ((0,1,2),(2,3,0))
	return verts, faces

def get_frame(width, height, x, y, thicknes):
	w,h,t = width, height, thicknes
	m,n = w-t, h-t
	verts = [(x,y),(w+x,y),(t+x,t+y),(m+x,t+y),(t+x,n+y),(m+x,n+y),(x,h+y),(w+x,h+y)]
	faces = [(0,1,3),(3,2,0),(0,2,4),(4,6,0),(1,7,3),(7,5,3),(6,4,5),(4,5,7)]
	return verts, faces

def get_setting_button(size, x, y):
	shape = ((0,0),(1,0),(0.05,0.05),(0.95,0.05),(0.05,0.75),(0.95,0.75),(0,1),(1,1))
	verts = [(s[0]*size+x,s[1]*size+y) for s in shape]
	faces =((0,1,2),(2,1,3),(1,7,3),(3,7,5),(1,3,7),(0,2,4),(4,6,0),(4,5,6),(5,7,6))
	return verts, faces

def get_checkmark(size, x, y):
	shape = ((0,0.4),(0.25,0.75),(0.5,0.5),(0.8,0.9),(1,0.8),(0.4,0.2))
	verts = [(s[0]*size+x,s[1]*size+y) for s in shape]
	faces =((0,1,2),(0,2,5),(2,3,5),(5,3,4))
	return verts, faces

def get_arrow(size, x, y, riverce):
	shape =((0,0),(1,0.5),(0,1))
	if riverce:
		shape =((1,0),(0,0.5),(1,1))
	verts = [(s[0]*size+x,s[1]*size+y) for s in shape]
	faces =[(0,1,2)]
	return verts, faces