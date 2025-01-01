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
# 2024/12/27

import bpy
import os
import subprocess
import platform
import json


def get_datafiles_path():
	""" return datafile path and create if not exist """
	datafiles_path = bpy.utils.user_resource("SCRIPTS", path="addons")

	datafiles_path += os.sep + 'BsMax-datafiles'

	if not os.path.isdir(datafiles_path):
		os.mkdir(datafiles_path)

	return datafiles_path


def open_folder_in_explorer(path):
	if not os.path.isdir(path):
		return

	if platform.system() == "Windows":
		os.startfile(path)
	
	elif platform.system() == "Darwin":
		subprocess.call(["open", path])
	
	elif platform.system() == "Linux":
		subprocess.call(["xdg-open", path])


def write_dictionary_to_json_file(data, file_path):
	try:
		with open(file_path, 'w', encoding='utf-8') as json_file:
			json.dump(data, json_file, ensure_ascii=False, indent=4)
		return True
	except:
		return False


def read_json_file_to_dictionary(file_path):
	try:
		with open(file_path, 'r', encoding='utf-8') as json_file:
			data = json.load(json_file)
		return data
	except:
		return {}