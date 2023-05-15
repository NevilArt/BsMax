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

function select_flat_surface =
(
    macroScript FlatSelect tooltip:"Select Flat" category:"Modeling Tools"
    (	
        on isVisible do (
            classof $ == Editable_Poly
        )

        on isChecked do (
            $.SelectByAngle == on and $.ignoreBackfacing == on
        )

        on execute do (
            if  $.SelectByAngle == on then (
                $.SelectByAngle = off
                $.ignoreBackfacing = off
            )
            else (
                $.SelectByAngle = on
                $.ignoreBackfacing = on
            )
             $.selectAngle = 45
        )
    )
)



function poly_nurms_toggle iterations =
(
    if classof $ == Editable_Poly do (
        if $.surfSubdivide == true then (
            if $.iterations != iterations then (
                $.iterations = iterations
            )
            else (
                 $.surfSubdivide = off
            )
        )
        else (
            $.surfSubdivide = on
            $.iterations = iterations
        )
    )
)



function create_image_plane =
(
	--Quick Image plane creator V1.1.0 Created by nevil 2012/11/12 firfira animation studio --
	myfile = getOpenFileName "Get one of textures:" types:"Image file(*.*)"

    if myfile == undefined do (
        return undefined
    )

    mytype = getFilenameType myfile
    if mytype == ".jpg" or mytype == ".png" do (
        tmap = openBitMap myfile
        BW = tmap.width / 10.0
        BH = tmap.height / 10.0
        myplan = Plane lengthsegs:1 widthsegs:1 length:BH width:BW pos:[0,0,0] isSelected:off name:"Image Plan"
        addModifier myplan (Edit_Poly())
        addModifier myplan (Uvwmap())
        mystring = getFilenameFile myfile
        myplan.transform = (matrix3 [1,0,0] [0,0,1] [0,-1,0] [0,0,0])
        mymatt = standard ()
        mymatt.selfIllumAmount = 100
        mymatt.showInViewport = true
        mymatt.name = "Image Plane"
        mybitmap = bitmaptexture ()
        mybitmap.filename = myfile
        mymatt.diffuseMap = mybitmap

        if mytype == ".png" do (
            mybitmap.monoOutput = 1
            mymatt.opacityMap = mybitmap
        )
        myplan.material = mymatt	
    )
)



rollout pivottoolsro ""
(
    --checkbutton apobt "Affect Pivot Only" width:150
    button topcenterbt "Top Center" width:150
    button centerbt "Center" width:150
    button butcenterbt "Button Center" width:150
    button cancelbt "Exit" width:150
    
    on topcenterbt pressed do 
    (
        for i in selection do (
            i.pivot.x = i.center.x
            i.pivot.y = i.center.y
            i.pivot.z = i.max.z
        )
    )
    
    on centerbt pressed do (
        for i in selection do (
            i.pivot = i.center
        )
    )
        
    on butcenterbt pressed do 
    (
        for i in selection do (
            i.pivot.x = i.center.x
            i.pivot.y = i.center.y
            i.pivot.z = i.min.z
        )
    )
    
    on cancelbt pressed do (
        destroydialog pivottoolsro
    )
)



function open_pivot_tools_dialog =
(
	try(destroydialog pivottoolsro)catch()
	createdialog pivottoolsro style:#() pos:mouse.screenpos
)



function corner_edge_select =
(
	--Hid un hid in meno have to add---
	--################################
	-- has to be fix
	--################################
	if selection.count == 1 do (
		obj = Selection[1]
		if classof obj == Editable_Poly and subobjectLevel == 2 do (
			VC = Polyop.getNumVerts obj
			SelectArray = #()
			
            for i = 1 to VC do (
				V = (polyop.getEdgesUsingVert obj i) as array
				if V.count == 3 do append SelectArray i
			)
			
            polyop.setVertSelection obj SelectArray
			obj.EditablePoly.ConvertSelection #Vertex #Edge
			obj.EditablePoly.SelectEdgeLoop()
		)
	)
)