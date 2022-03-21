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

bl_info = {
	"name" : "MaxivzsTools",
	"author" : "Maxi Vazquez",
	"description" : "Collection of context sensitive and time saving tools",
	"blender" : (2, 80, 0),
	"location" : "View3D",
	"warning" : "",
	"category" : "Generic"
}

import bpy

from . pannels import MaxivzTools_PT_Panel
from . mvztools import (MESH_OT_SuperSmartCreate,
	MESH_OT_CSBevel,
	MESH_OT_SmartDelete,
	MESH_OT_SmartSelectLoop,
	MESH_OT_SetCylindricalObjSides,
	MESH_OT_QuickSelectionVert,
	MESH_OT_QuickSelectionEdge,
	MESH_OT_QuickSelectionFace,
	MESH_OT_ContextSensitiveSlide,
	MESH_OT_SmartSelectRing,
	MESH_OT_QuickPivot,
	MESH_OT_SimpleEditPivot,
	MESH_OT_QuickModifierToggle,
	MESH_OT_QuickWireToggle,
	MESH_OT_WireShadedToggle,
	MESH_OT_TargetWeldToggle,
	MESH_OT_SmartExtrude,
	MESH_OT_QuickRadialSymmetry,
	MESH_OT_QuickFFD,
	MESH_OT_SmartTranslate,
	UV_OT_QuickRotateUv90Pos,
	UV_OT_QuickRotateUv90Neg)

classes = (MESH_OT_SuperSmartCreate,
	MESH_OT_CSBevel,
	MESH_OT_SmartDelete,
	MESH_OT_SmartSelectLoop,
	MESH_OT_SetCylindricalObjSides,
	MESH_OT_QuickSelectionVert,
	MESH_OT_QuickSelectionEdge,
	MESH_OT_QuickSelectionFace,
	MESH_OT_ContextSensitiveSlide,
	MESH_OT_SmartSelectRing,
	MESH_OT_QuickPivot,
	MESH_OT_SimpleEditPivot,
	MESH_OT_QuickModifierToggle,
	MESH_OT_QuickWireToggle,
	MESH_OT_WireShadedToggle,
	MESH_OT_TargetWeldToggle,
	MESH_OT_SmartExtrude,
	MESH_OT_QuickRadialSymmetry,
	MESH_OT_QuickFFD,
	MESH_OT_SmartTranslate,
	UV_OT_QuickRotateUv90Pos,
	UV_OT_QuickRotateUv90Neg,
	MaxivzTools_PT_Panel)

register,unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
	register()