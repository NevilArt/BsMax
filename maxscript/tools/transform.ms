/*##########################################################################
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
##########################################################################*/

struct Vector3(public x=0, public y=0, public z=0)



struct TransfromMatrix 
(
    public location = Vector3 x:0 y:0 z:0,
    public euler_rotation = Vector3 x:0 y:0 z:0,
    public scale_Vector = Vector3 x:1 y:1 z:1,

    function from_transform matrix =
    (
        pos = matrix.position
        this.location.x = pos.x
        this.location.y = pos.y
        this.location.z = pos.z

        rot = matrix.rotation as eulerAngles
        this.euler_rotation.x = rot.x
        this.euler_rotation.y = rot.y
        this.euler_rotation.z = rot.z

        scl = matrix.scale
        this.scale_Vector.x = scl.x
        this.scale_Vector.y = scl.y
        this.scale_Vector.z = scl.z
    ),

    public function as_unreal =
    (
        retMatrix = TransfromMatrix()
        retMatrix.location.x = this.location.x
        retMatrix.location.y = -this.location.y
        retMatrix.location.z = this.location.z

        retMatrix.euler_rotation.x = this.euler_rotation.y
        retMatrix.euler_rotation.y = this.euler_rotation.x - 90
        retMatrix.euler_rotation.z = -this.euler_rotation.z - 90

        retMatrix.scale_Vector.x = this.scale_Vector.x
        retMatrix.scale_Vector.y = this.scale_Vector.y
        retMatrix.scale_Vector.z = this.scale_Vector.z
        return retMatrix
    ),

    public function as_blender =
    (
        retMatrix = TransfromMatrix()
        retMatrix.location.x = this.location.x / 100.0
        retMatrix.location.y = this.location.y / 100.0
        retMatrix.location.z = this.location.z / 100.0

        retMatrix.euler_rotation.x = DegToRad this.euler_rotation.x
        retMatrix.euler_rotation.y = DegToRad this.euler_rotation.y
        retMatrix.euler_rotation.z = DegToRad this.euler_rotation.z

        retMatrix.scale_Vector.x = this.scale_Vector.x
        retMatrix.scale_Vector.y = this.scale_Vector.y
        retMatrix.scale_Vector.z = this.scale_Vector.z
        return retMatrix
    )
)



function matrix_to_blender_clipboard matrix =
(
    script = "BSMAXTRANSFORMCLIPBOARDV2\n"
    script += matrix.location.x as string + ","
    script += matrix.location.y as string + ","
    script += matrix.location.z as string + ","
    
    script += matrix.euler_rotation.x as string + ","
    script += matrix.euler_rotation.y as string + ","
    script += matrix.euler_rotation.z as string + ","
    
    script += matrix.scale_Vector.x as string + ","
    script += matrix.scale_Vector.y as string + ","
    script += matrix.scale_Vector.z as string 
    
    setclipboardText script
)



function copy_selected_transform_to_clipboard =
(
    if selection.count == 1 do (
        trmMatrix = TransfromMatrix()
        trmMatrix.from_transform $.transform
        matrix_to_blender_clipboard (trmMatrix.as_blender())
    )
)