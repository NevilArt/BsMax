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


rollout GroundPicker "Ground Picker"
(
    local Orig = #()
    
    pickbutton Groundpbtn "Pick Ground" width:150 autodisplay:true
    radiobuttons Posrbtn "Position" labels:#("Pivot", "Min", "Center") align:#left
    radiobuttons Rotrbtn "Rotation" labels:#("Non ", "Normal") align:#left
    checkbox RandRotcb "Random  Rotation"
    spinner Zoffset "Z Offset" type:#worldUnits range:[-99999,99999,0]
    button Applybtn "Apply On selections" width:150
    button Resetbtn "Reset" width:150
    
    function Shot Obj =
    (
        -- Calculate Z offset --
        local ZAdd = 0, OScale = Obj.scale
        case Posrbtn.state of (
            1: ZAdd = 0 + Zoffset.value
            2: ZAdd = Obj.pos.z - Obj.min.z + Zoffset.value
            3: ZAdd = Obj.pos.z - Obj.center.z + Zoffset.value
        )
        -- Calculate Transform
        Hit = intersectray Groundpbtn.object (ray [Obj.pos.x, Obj.pos.y, Groundpbtn.object.max.z] [0,0,-1])
        if Hit != undefined do (
            Zv = Hit.dir
            Yv = [0,0,1]
            Xv = normalize (cross Yv Zv)
            Yv = Normalize (cross Zv Xv)
            T = matrix3 Xv Yv Zv hit.pos
            --TODO Retrive Scale
            -- Apply position --
            case Rotrbtn.state of (
                1: (
                    Obj.pos = T.pos + [0,0,ZAdd]
                )
                
                2: (
                    Obj.transform = T
                    in coordsys local obj.pos.z += ZAdd
                    obj.scale = OScale
                )
            )
            
            if RandRotcb.checked do (
                in coordsys local obj.rotation.z  = (random 0.0 2.5)
            )
        )
    )

    function updatefn =
    (
        disableSceneRedraw() 
        seed 1
        for O in Orig do (
            O[1].transform = O[2]
            Shot O[1]
        )
        enableSceneRedraw()
        Redrawviews()
    )

    on Applybtn pressed do 
    (
        if Groundpbtn.object != undefined and selection.count > 0 do (
            Orig = #()
            for O in selection do (
                if O != Groundpbtn.object do (
                    append Orig #(O, O.transform)
                )
            )
            updatefn()
        )
    )

    on Zoffset changed val do updatefn()
    on Posrbtn changed state do updatefn()
    on Rotrbtn changed state do updatefn()
    on RandRotcb changed state do updatefn()
    on Resetbtn pressed do
    (
        for O in Orig do (
            O[1].transform = O[2] -- reset to original position
        )
    )
)

function open_ground_picker_dialog =
(	
	createdialog GroundPicker width:180
)