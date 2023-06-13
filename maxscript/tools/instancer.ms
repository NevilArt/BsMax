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



rollout instancerro "Instancer" width:235
(
    local target = #()

    pickbutton maternodepb "Pick Master" autodisplay:true width:150 pos:[8,8]
    multilistbox targetnodelb "" width:150 height:10 pos:[8,32]
    button addbt "+" width:70 pos:[8,170]
    button removbt "-" width:70 pos:[88,170]
    button findsimillarbt "Find simmilars" width:150 pos:[8,195]
    button makeinstancebt "Make it instance" width:150 pos:[8,220]
    checkbox fcheckcb "Advance" pos:[165,199] tooltip:"Advance check"
    checkbox mattcb "Material" pos:[165,223] tooltip:"apply materials too"

    on maternodepb rightclick do if selection.count == 1 do
    (
        maternodepb.object = selection[1]
        maternodepb.caption = selection[1].name
    )

    on addbt pressed do
    (
        local names = #()
        for i in selection do (
            if i != maternodepb.object do (
                appendifunique target i
            )
        )
        
        for i in target do (
            append names i.name
        )
        
        targetnodelb.items = names
    )
    
    on removbt pressed do
    (
        target = #()
        targetnodelb.items = #()
    )
    
    on findsimillarbt pressed do
    (
        if maternodepb.object != undefined do (
            local names = #()
            target = #()

            if superclassof maternodepb.object == GeometryClass then (
                for i in objects do (
                    if classof i != LinkComposite then (
                        if superclassof i.baseobject == GeometryClass do (
                            if not i.isHidden do (
                                Pface = #{1}
                                Cface = #{1}
                                try (
                                    --## check if poly count > 0 do
                                    if meshop.getNumFaces i.baseobject.mesh == meshop.getNumFaces maternodepb.object.baseobject.mesh do (
                                        if fcheckcb.checked do (
                                            Pface = execute ("#{1.."+ (meshop.getNumFaces maternodepb.object.baseobject.mesh) as string + "}")
                                            Cface = execute ("#{1.."+ (meshop.getNumFaces i.baseobject.mesh) as string + "}")
                                        )
                                    )
                                )
                                catch (
                                    print (">>: " + i.name)
                                ) 

                                try (
                                    if meshop.getFaceArea i.baseobject.mesh Cface == meshop.getFaceArea maternodepb.object.baseobject.mesh Pface do (
                                        if i != maternodepb.object do (
                                            append target i
                                        )
                                    )
                                )
                                catch (
                                    print (">>: " + i.name)
                                )
                            )
                        )
                    )
                )
            )
            else (
                for i in objects do (
                    if classof i == classof maternodepb.object and i != maternodepb.object do (
                        append target i
                    )
                )
            )
            /*else if superclassof maternodepb.object == shape then for i in objects do if classof i == classof maternodepb.object and i != maternodepb.object do append target i
            else if superclassof maternodepb.object == light then ()
            else if superclassof maternodepb.object == camera then ()
            else if superclassof maternodepb.object == helper then ()
            else if superclassof maternodepb.object == SpacewarpObject then ()*/
            for i in target do (
                append names i.name
            )
            targetnodelb.items = names
            select target
        )
    )
    
    on makeinstancebt pressed do (
        if maternodepb.object != undefined do (
            for i in target do (
                i.baseobject = maternodepb.object.baseobject
            )

            if mattcb.checked do (
                for i in target do (
                    i.material = maternodepb.object.material
                )
            )
        )
    )
)


function open_instancer_dialog =
(
	try(destroydialog instancerro)catch()
    createdialog instancerro
)