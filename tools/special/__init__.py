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

from .blender import register_blender,unregister_blender
from .max import register_max,unregister_max
from .maya import register_maya,unregister_maya

class RegisterData:
	def __init__(self):
		self.pack = ''
reg = RegisterData()

def register_special(preferences):
	Unregister_special()

	toolpack = preferences.toolpack
	if toolpack == 'Blender':
		register_blender()
	elif toolpack == '3DsMax':
		register_max()
	elif toolpack == 'Maya':
		register_maya()

	reg.pack = toolpack

def Unregister_special():
	if reg.pack == 'Blender':
		unregister_blender()
	elif reg.pack == '3DsMax':
		unregister_max()
	elif reg.pack == 'Maya':
		unregister_maya()
	reg.pack = ''