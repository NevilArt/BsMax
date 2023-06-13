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



rollout RootCleanerro "Root Cleaner"
(
    button CustomAttributebtn "" width:150
    button ParticleFlowbtn "" width:150

    on RootCleanerro open do
    (
        CustomAttributebtn.caption = "Clear " + (custAttributes.count rootscene) as string + " CustomAttributes"
        ParticleFlowbtn.caption = "Clear " + (for h in helpers where classof h == Particle_View collect h).count as string + " ParticleViews"
    )
    
    on CustomAttributebtn pressed do
    (
        for i = custAttributes.count rootscene to 1 by -1 do custAttributes.delete rootscene 1
        CustomAttributebtn.caption = "Done"
        
    )
    
    on ParticleFlowbtn pressed do
    (
        Delete (for h in helpers where classof h == Particle_View collect h)
        ParticleFlowbtn.caption = "Done"
    )
)



function open_root_cleaner =
(
	createdialog RootCleanerro
)