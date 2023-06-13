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


function arrange_by_distance =
(
    if selection.count < 2 do (
        return undefined
    )

    Obj = Selection
	Local A, B, MD = 0
    A = Obj[1]
    B = Obj[2]

    for i = 1 to Obj.count do (
        for j = i to Obj.count do (
            if Distance Obj[i] Obj[j] > MD do (
                MD = Distance Obj[i] Obj[j]
                A = Obj[i]
                B = Obj[j]
            )
        )
    )

    Local Dis = #(), Sobj = #()

    for i in Obj do (
        append Dis (Distance A i)
    )

    sort Dis

    for i = 1 to Dis.count do (
        for j = 1 to obj.count do (
            if Distance A Obj[j] == Dis[i] do (
                append Sobj Obj[j]
            )
        )
    )

    for i = 2 to (Sobj.count - 1) do (
        Sobj[i].pos = A.pos + (((B.pos - A.pos) / (Sobj.count - 1)) * (i-1))
    )
    
    for i = 2 to (Sobj.count - 1) do (
        Sobj[i].Scale = A.Scale + (((B.Scale - A.Scale) / (Sobj.count - 1)) * (i-1))
    )
    
    local XA,YA,ZA,XB,YB,ZB

    try(XA = A.rotation.controller.X_Rotation)catch(XA = undefined)
    try(YA = A.rotation.controller.Y_Rotation)catch(YA = undefined)
    try(ZA = A.rotation.controller.Z_Rotation)catch(ZA = undefined)
    try(XB = B.rotation.controller.X_Rotation)catch(XB = undefined)
    try(YB = B.rotation.controller.Y_Rotation)catch(YB = undefined)
    try(ZB = B.rotation.controller.Z_Rotation)catch(ZB = undefined)

    if classof XA != UndefinedClass and classof XB != undefined do (
        for i = 2 to (Sobj.count - 1) do (
            Sobj[i].rotation.controller.X_Rotation = XA + ((XB - XA) / (Sobj.count - 1)) * (i - 1)
        )
    )

    if classof YA != UndefinedClass and classof YB != undefined do (
         for i = 2 to (Sobj.count - 1) do (
            Sobj[i].rotation.controller.Y_Rotation = YA + ((YB - YA) / (Sobj.count - 1)) * (i - 1)
         )
    )

    if classof ZA != UndefinedClass and classof ZB != undefined do (
        for i = 2 to (Sobj.count - 1) do (
            Sobj[i].rotation.controller.Z_Rotation = ZA + ((ZB - ZA) / (Sobj.count - 1)) * (i - 1)
        )
    )
)



function arrange_on_shape =
(
	Local S = Selection
	function shapeFilt o = (superClassOf o == Shape)
	
    if S.count > 0 do (
        obj = pickObject message:"Now Get a Shap Object" filter:shapeFilt
    )
	
    if obj != undefined do (
        undo on (
            --## create 2 metjhod for open and close splines ---
            Local pos = point pos:[0,0,0] 
            Pos.pos.controller = Path_Constraint()
            Pos.pos.controller.follow = on
            Pos.pos.controller.path = obj
            for i = 1 to S.count do (	
                Pos.pos.controller.percent = (100.0 / (S.count - 1)) * (i - 1)
                --S[i].pos = Pos.pos
                S[i].transform = Pos.transform
            )
            Delete Pos
        )
    )
)