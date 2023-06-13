/*##########################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
##########################################################################*/


rollout materialcreatorro "MC"
(
    spinner countsp "ID Count" type:#integer range:[1,1000,2]
    checkbox randomcolorcb "Random Color" checked:true
    dropdownlist typeddl "" items:#("Standard","Arch")
    button createbt "Create" width:70 across:2
    button autobt "Auto" width:70 enabled:false

    function creatematt count =
    (
        objmatt = Multimaterial()

        if selection.count == 1 do (
            objmatt.name = selection[1].name
        )

        objmatt.numsubs  = count

        for i = 1 to count do (
            newmatt = standardmaterial()
            R = random 0 256
            G = random 0 256
            B = random 0 256
            newmatt.Diffuse = color R G B
            objmatt[i] = newmatt
        )

        $.material = objmatt

        if randomcolorcb.state do (
            --### this part do not work correctly --
            local newmod = selection[1].modifiers[#MaterialByElement]
            
            if newmod == undefined do (
                newmod = MaterialByElement()
            )
            
            newmod.method = 0
            newmod.Material_ID_Count = count
            addModifier $ newmod
        )
    )

    on createbt pressed do
    (
        creatematt countsp.value
    )

    on autobt pressed do
    (
        local count = 3
        -- get count
        creatematt 3
    )
)


function open_new_multi_material_creator_dialog =
(
	try(destroydialog materialcreatorro)catch()
	createdialog materialcreatorro pos:mouse.screenpos
)



function set_gray_material =
(
    -- need to update to new methd --
    $.wirecolor = color 0 0 0
    if classof $ == editable_poly do (
        $.cageColor = color 128 128 128
    )
    $.material = meditMaterials[24]
    meditMaterials[24].name = "Gray"
)



function remove_material =
(
    -- TODO change wire color only if it  is gray
	$.wirecolor = random (color 50 50 50) (color 220 220 220)
	$.material = undefined
)