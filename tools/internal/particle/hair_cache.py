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
from keymaps.cinema4d import text
import bpy, os, shutil
from pathlib import Path
from bpy.types import Operator

# swich between hair caches not working as aspected                  #
# this is a temprary solution till problem solvein blender itself    #
# all cache files rename as index 0 and same name in Combined folder #
# this helps to load all of files only by frame nombrt automaticaly  #

class Particle_OT_Hair_Cache_Combine(Operator):
	""" Combine all of multi caches to single cache sequence """
	bl_idname = 'particle.hair_cache_combine'
	bl_label = 'Combine Hair Caches'
	bl_options = {'REGISTER', 'INTERNAL'}

	def get_full_cache_path(self, cache_path):
		""" Check for path is absolut or relative """
		if cache_path[0] == '/':
			file_path = Path(bpy.data.filepath)
			parent_dir = str(file_path.parent)
			ret_path = parent_dir + '\\' + cache_path[2: len(cache_path)]
		else:
			ret_path = cache_path

		""" Check is Combined or parent directory """
		folder_name = os.path.dirname(ret_path).split('\\')[-1]
		if folder_name == 'Combined':
			""" Return Parent directory if path set in Combined folder """
			ret_path = str(Path(ret_path).parent) + '\\'
		
		return ret_path
	
	def clear_directory(self, path):
		for file in os.listdir(path):
			os.remove(path + file)

	def execute(self, ctx):
		point_cache = ctx.object.particle_systems.active.point_cache
		""" Ignore if path not selected """
		if point_cache.filepath == '':
			return{"FINISHED"}
		
		""" Create pathes """
		cache_name = point_cache.name
		cache_path = self.get_full_cache_path(point_cache.filepath)
		combined_path = cache_path + 'Combined\\'

		if not os.path.exists(combined_path):
			os.mkdir(combined_path)
		self.clear_directory(combined_path)
		
		for full_name in os.listdir(cache_path):
			file_name, file_extension = os.path.splitext(full_name)
			
			if file_extension != '.bphys':
				continue
			
			""" Source file name """
			source = cache_path + file_name + file_extension

			frame = file_name[len(file_name)-9: len(file_name)-3]
			
			""" Create new file name with Index 00 """
			file_name_00 = cache_name + '_' + frame + '_00'
			
			target = combined_path + file_name_00 + file_extension
			shutil.copy(source, target)
		
		""" Set cache path as new created files path """
		point_cache.filepath = combined_path
		
		return{"FINISHED"}




def hair_cache_panle(self, ctx):
	if ctx.object.particle_systems.active.point_cache.use_external:
		layout = self.layout
		row = layout.row()
		row.label(text='')
		row.operator('particle.hair_cache_combine',
			text = 'Combine Caches',
			icon='GP_MULTIFRAME_EDITING')



classes = [Particle_OT_Hair_Cache_Combine]

def register_hair_cache():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.PARTICLE_PT_cache.append(hair_cache_panle)

def unregister_hair_cache():
	bpy.types.PARTICLE_PT_cache.remove(hair_cache_panle)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_hair_cache()