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

-- Cat Pelvis --
-- Free screepted tool --
-- Developed by Nevil (Naser Merati) --
-- More on Nevilart.blogspot.com --
-- Any problem or question NevilArt@Gmail.Com --
------------------------------------------------
Rollout CatPelvisLegLinkerro "C.P.P"
(
	Global Pelvis, IKS
	button Createbtn "Cat Quick Link" width:100 height:100
	---------------------------------------------------------------------------------------------------------------------------
	function GetCatParent Obj =
	(
		local RetParent = undefined
		if classof Obj == CATParent then (
			RetParent = Obj
		)
		else (
			for Cat in Helpers do (
				if classof Cat == CATParent do (
					
					for N in Cat.CATRigNodes do (
						if N == Obj do (
							RetParent = Cat
							exit
						)
					)
					
					if RetParent != undefined do (
						exit
					)
				)
			)
		)
		return RetParent
	)

	function GetCatPelvis Cat =
	(
		local Pelvis = undefined
		if classof Cat == CATParent do (
			for C in Cat.CATRigNodes do (
				if classof C == HubObject do (
					if C.parent == undefined do (
						Pelvis = C
						exit
					)
				)
			)
		)
		return Pelvis
	)

	function GetCatIKTargs Cat =
	(
		local IKS = #()
		if classof Cat == catparent do (
			for C in Cat.CATRigNodes do (
				if classof C == IKTarget do (
					append IKS C
				)
			)
		)
		return IKS
	)

	on Createbtn pressed do (
		if selection.count == 1 do (
			CParent =  GetCatParent Selection[1]
			Pelvis = GetCatPelvis CParent
			IKS = GetCatIKTargs CParent
			if Pelvis != undefined do (
				CurrentFrame = (slidertime as string) as integer
				W = Pelvis.max.x - Pelvis.min.x
				L = Pelvis.max.y - Pelvis.min.y
				-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
				fn GetLayerIndex TheNode =
				(
					Local Index = 0
					try (
						while true do (
							Index += 1
							if TheNode.transform.controller.LayerTrans[Index] != undefined then (
								ret = #(Index)
								ControllerType = Pelvis.transform.controller.LayerTrans[Index].controller as string
								isPrs = ControllerType == "Controller:Position_Rotation_Scale"
								isLink = ControllerType == "Controller:Link_Constraint"
								if isPrs or isLink do (
									exit
								)
							)
							else(
								Index = 0
								exit
							)
						)
					)
					catch (
						Index = 0
					)
					return Index
				)

				fn AddTarget TheNode Target TheTime index = if index > 0 do
				(
					ctrlType = TheNode.transform.controller.LayerTrans[index].controller as string
					if ctrlType != "Controller:Link_Constraint" do (
						TheNode.transform.controller.LayerTrans[index].controller = Link_Constraint()
					)
					TheNode.transform.controller.LayerTrans[index].controller.AddTarget Target TheTime
				)

				index = GetLayerIndex Pelvis
				if Index > 0 do (
					ThePoint = Point pos:[0,0,0] centermarker:false axistripod:false cross:false Box:true size:((W+L) * 2)
					ThePoint.name = uniquename (Pelvis.name + "_Point")

					on animate off (
						ThePoint.transform = Pelvis.transform
					)

					Nodes = #()
					join Nodes IKS
					append Nodes Pelvis

					for N in Nodes do (
						AddTarget N ThePoint CurrentFrame index
					)
					select ThePoint
				)
			)-- end of if
		)-- end of on
	)
)

create_cat_pelvis_helper =
(
	createdialog CatPelvisLegLinkerro width:120
)