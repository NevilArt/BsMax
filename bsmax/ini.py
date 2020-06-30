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
import bpy
from os import path

class INI:
	def __init__(self):
		self.data = []
		self.filename = bpy.utils.user_resource('SCRIPTS', "addons") + "/BsMax.ini"
	
	def save(self):
		pass
	
	def load(self):
		if path.exists(self.filename):
			return open(self.filename).read()
