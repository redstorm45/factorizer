'''

    Copyright 2014 Pierre Cadart


    This file is part of Factory Maker.

    Factory Maker is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Factory Maker is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Factory Maker.  If not, see <http://www.gnu.org/licenses/>.


    Description:
        This file is made to write a basic test level
'''

level = open("1.level","w")
level.write("transport\n")#level name is "transport"
level.write("6,6\n")      #level has 6*6 cells

for i in range(6):
    for j in range(6):
        if i == 2 and j == 1:
            level.write("in(0,white,-1)\n") #input is white, direction 0, and standard
        elif i == 2 and j == 4:
            level.write("out(-1,any,1)\n")  #output is omnidirectionnal, accept any color, and is refered as output '1'
        else:
            level.write("n\n") #nothing
level.write("1\n") #there is 1 objective
level.write("1.10\n")#output '1' will need 10 cubes

level.write("1\n") #there is 1 object available
level.write("2xbelt(0)\n")#it is a stack of 2 conveyor belts

level.close()
print("wrote level 1")


level = open("2.level","w")
level.write("turning\n")#level name is "turning"
level.write("6,6\n")      #level has 6*6 cells

for i in range(6):
    for j in range(6):
        if i == 1 and j == 1:
            level.write("in(0,white,-1)\n") #input is white, direction 0, and standard
        elif i == 4 and j == 4:
            level.write("out(-1,any,1)\n")  #output is omnidirectionnal, accept any color, and is refered as output '1'
        else:
            level.write("n\n") #nothing
level.write("1\n") #there is 1 objective
level.write("1.10\n")#output '1' will need 10 cubes

level.write("2\n") #there are 2 objects available
level.write("2xbelt(0)\n")#it is a stack of 2 conveyor belts (to right)
level.write("3xbelt(1)\n")#  and a stack of 2 conveyor belts (to down)

level.close()
print("wrote level 2")


level = open("3.level","w")
level.write("turning more\n")#level name is "turning more"
level.write("6,6\n")      #level has 6*6 cells

for i in range(6):
    for j in range(6):
        if i == 1 and j == 1:
            level.write("in(0,white,-1)\n") #input is white, direction 0, and standard
        elif i == 4 and j == 4:
            level.write("out(-1,any,1)\n")  #output is omnidirectionnal, accept any color, and is refered as output '1'
        else:
            level.write("n\n") #nothing
level.write("1\n") #there is 1 objective
level.write("1.10\n")#output '1' will need 10 cubes

level.write("4\n") #there are 2 objects available
level.write("2xbelt(0)\n")#it is a stack of 2 conveyor belts (to right)
level.write("2xbelt(1)\n")#  and a stack of 2 conveyor belts (to down)
level.write("2xbelt(2)\n")#  and a stack of 2 conveyor belts (to left)
level.write("2xbelt(3)\n")#  and a stack of 2 conveyor belts (to top)

level.close()
print("wrote level 3")






level = open("4.level","w")
level.write("basic sorting\n")#level name is "basic sorting"
level.write("6,6\n")          #level has 6*6 cells

for i in range(6):       #y
    for j in range(6):   #x
        if i == 2 and j == 1:
            level.write("in(0,any,0)\n") #input is special, direction 0, and has inputconfig 0
        elif i == 1 and j == 4:
            level.write("out(-1,red,1)\n")  #output is omnidirectionnal, accept any color, and is refered as output '1'
        elif i == 3 and j == 4:
            level.write("out(-1,blue,2)\n")  #output is omnidirectionnal, accept any color, and is refered as output '2'
        else:
            level.write("n\n") #nothing

#special input
level.write("[blue,red]r[0.5,0.5]\n")#inputconfig 0 is a random choice between red and blue, 1/2 chances each

level.write("2\n") #there are 2 objectives
level.write("1.10\n")#output '1' will need 10 cubes
level.write("2.10\n")#output '2' will need 10 cubes

level.write("3\n") #there are 3 objects available
level.write("2xbelt(0)\n")#it is a stack of 2 conveyor belts (to right)
level.write("1xadvbelt(1,3)\n")#  and a stack of 2 conveyor belts (to down or up when active)
level.write("1xdetect(blue)\n")#  a blue detector

level.close()
print("wrote level 4")
