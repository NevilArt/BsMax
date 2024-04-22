############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################
# 2024/04/08

import bpy

from primitive.primitive import Primitive_Geometry_Class


def get_box_mesh(width, length, height, wsegs, lsegs, hsegs):
	verts, edges, faces = [], [], []
	# Control the input values
	if wsegs < 1: wsegs = 1
	if lsegs < 1: lsegs = 1
	if hsegs < 1: hsegs = 1

	w = width / wsegs
	l = length / lsegs
	h = height / hsegs
	hw = width / 2
	hl = length / 2

	# Create vertexes
	for he in (0.0, height):
		for i in range(wsegs + 1):
			for j in range(lsegs + 1):
				x = w * i - hw
				y = l * j - hl
				z = he
				verts.append((x, y, z))

	for i in range(1,hsegs):
		for j in range(lsegs + 1):
			x = -hw
			y = l * j - hl
			z = h * i
			verts.append((x, y, z))

		for j in range(1, wsegs + 1):
			x = w * j - hw
			y = length - hl
			z = h * i
			verts.append((x, y, z))

		for j in range(lsegs - 1, -1, -1):
			x = width - hw
			y = l * j - hl
			z = h * i
			verts.append((x , y, z))

		for j in range(wsegs - 1, 0, -1):
			x = w * j - hw
			y = -hl 
			z = h * i
			verts.append((x, y, z))

	# Create faces
	# fill plates
	for k in range(2):
		f = k * (wsegs + 1) * (lsegs + 1)
		for i in range(wsegs):
			for j in range(lsegs):
				a = j + (lsegs + 1) * i + f
				b = a + 1
				c = b + lsegs + 1
				d = c - 1
				if k == 0:
					faces.append((a, b, c, d))
				else:
					faces.append((d, c, b, a))

	# fill center
	f = ((lsegs + 1) * 2) * (wsegs + 1)
	l = (wsegs + lsegs) * 2
	for i in range(hsegs - 2):
		for j in range(l):
			a = f + i * l + j   
			if j < l - 1:
				b = a + 1
				c = b + l
				d = c - 1
			else:
				b = f + i * l
				c = f + (i + 1) * l
				d = a + l
			faces.append((d, c, b, a))

	f2 = f + l * (hsegs - 2) # last line first vertext
	if hsegs > 1:
		# silde lowr line 1
		for i in range(lsegs):
			a = i
			b = a + 1
			c = f + i + 1
			d = f + i
			faces.append((d, c, b, a))

		# silde lowr line 2
		fl, fu = lsegs, f + lsegs
		for i in range(wsegs):
			a = fl + i * (lsegs + 1)
			b = a + lsegs + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))

		# silde lowr line 3
		fl = (wsegs + 1) * (lsegs + 1) - 1
		fu = f + wsegs + lsegs
		for i in range(lsegs):
			a = fl - i
			b = a - 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))

		# silde lowr line  4
		fl = (lsegs + 1) * wsegs
		fu = (wsegs + 1) * (lsegs + 1) * 2 + (lsegs + 1) * 2 + (wsegs - 2)
		for i in range(wsegs):
			a = fl - i * (lsegs + 1)
			b = a - (lsegs + 1)
			if i < wsegs - 1:
				c = fu + i + 1
			else:
				c = f
			d = fu + i
			faces.append((d, c, b, a))

		# silde Uper line 1
		fl = (wsegs + 1) * ((hsegs + lsegs - 1) * 2) + (lsegs - 1) * ((hsegs - 2) * 2)
		fu = (wsegs + 1) * (lsegs + 1)
		for i in range(lsegs):
			a = fl + i
			b = a + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))

		# silde Uper line 2
		fl += lsegs
		fu += lsegs
		for i in range(wsegs):
			a = fl + i
			b = a + 1
			c = fu + (i + 1) * (lsegs + 1)
			d = fu + i * (lsegs + 1)
			faces.append((d, c, b, a))

		# silde Upper line 3
		fl += wsegs
		fu = ((wsegs + 1) * (lsegs + 1) * 2) - 1
		for i in range(lsegs):
			a = fl + i
			b = a + 1
			c = fu - (i + 1)
			d = fu - i
			faces.append((d, c, b, a))

		# silde lowr line  4
		fl += lsegs
		fu -= lsegs
		for i in range(wsegs):
			a = fl + i
			if i < wsegs - 1:
				b = a + 1
				c = fu - (i + 1) * (lsegs + 1)
			else:
				b = (wsegs + 1) * ((hsegs + lsegs - 1) * 2) + (lsegs - 1) * ((hsegs - 2) * 2)
				c = (wsegs + 1) * (lsegs + 1)
			d = fu - i * (lsegs + 1)
			faces.append((d, c, b, a))
	else:
		# silde lowr line 1
		fu = (wsegs + 1) * (lsegs + 1)
		for i in range(lsegs):
			a = i
			b = a + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))

		# silde lowr line 2
		fl = lsegs
		fu += lsegs
		for i in range(wsegs):
			a = fl + i * (lsegs + 1)
			b = a + lsegs + 1
			c = fu + (i + 1) * (lsegs + 1)
			d = fu + i * (lsegs + 1)
			faces.append((d, c, b, a))

		# silde lowr line 3
		fl = (wsegs + 1) * (lsegs + 1) - 1
		fu = ((wsegs + 1) * (lsegs + 1) * 2) - 1
		for i in range(lsegs):
			a = fl - i
			b = a - 1
			c = fu - (i + 1)
			d = fu - i
			faces.append((d, c, b, a))

		# silde lowr line  4
		fl = (lsegs + 1) * wsegs
		fu -= lsegs
		for i in range(wsegs):
			a = fl - i * (lsegs + 1)
			b = a - (lsegs + 1)
			if i < wsegs - 1:
				c = fu - (i + 1) * (lsegs + 1)
			else:
				c = (wsegs + 1) * (lsegs + 1)
			d = fu - i * (lsegs + 1)
			faces.append((d, c, b, a))

	return verts, edges, faces


import numpy as np

def create_cuboid(
		width, length, height, width_segments, length_segments, height_segments
	):
    
	# Define the number of segments along each dimension
    w_segments = max(int(width_segments), 1)
    l_segments = max(int(length_segments), 1)
    h_segments = max(int(height_segments), 1)

    # Generate the vertices of the cuboid
    x = np.linspace(0, width, w_segments + 1)
    y = np.linspace(0, length, l_segments + 1)
    z = np.linspace(0, height, h_segments + 1)

    # Generate the grid of vertices for each face
    xv, yv = np.meshgrid(x, y)
    top_z = np.ones_like(xv) * height
    bottom_z = np.zeros_like(xv)

    yz_verts = np.stack([yv, xv, top_z], axis=-1)
    yz_verts = np.concatenate([yz_verts, np.stack([yv, xv, bottom_z], axis=-1)], axis=0)

    xz_verts = np.stack([xv, np.ones_like(yv) * length, yv], axis=-1)
    xz_verts = np.concatenate([xz_verts, np.stack([xv, np.zeros_like(yv), yv], axis=-1)], axis=0)

    xy_verts = np.stack([np.ones_like(xv) * width, xv, yv], axis=-1)
    xy_verts = np.concatenate([xy_verts, np.stack([np.zeros_like(xv), xv, yv], axis=-1)], axis=0)

    # Stack the vertices of all faces
    vertices = np.concatenate([yz_verts, xz_verts, xy_verts], axis=0)

    # Define the faces for each face
    yz_faces = np.reshape(np.arange(w_segments * l_segments * 2), (l_segments * 2, w_segments)) + len(yz_verts) // 2
    xz_faces = np.reshape(np.arange(w_segments * h_segments * 2), (h_segments * 2, w_segments)) + len(yz_verts) + len(xz_verts) // 2
    xy_faces = np.reshape(np.arange(l_segments * h_segments * 2), (h_segments * 2, l_segments)) + len(yz_verts) + len(xz_verts) + len(xy_verts) // 2

    # Stack the faces of all faces
    faces = np.concatenate([yz_faces, xz_faces, xy_faces], axis=0)
    print(faces)

    return vertices, [], faces

class Mesh(Primitive_Geometry_Class):
	def init(self):
		self.classname = "NewMesh"

	def create(self, ctx):
		# mesh = get_box_mesh(2, 3, 4, 20, 30, 40)
		mesh = create_cuboid(2, 3, 4, 2, 2, 2)
		# self.create_mesh(ctx, mesh, self.classname)
		# self.update_mesh(mesh)

	def update(self):
		pass

if __name__ == "__main__":
	newMesh = Mesh()
	newMesh.create(bpy.context)