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
        This file contains basic functions for different things
'''


import math

#blend a new color by multiplying
def multColor(col,ratio):
    r,g,b = col
    return (r*ratio,g*ratio,b*ratio)

def getColorFromStr(name):
    if name == "red":
        return (250,10,10)
    if name == "green":
        return (10,250,10)
    if name == "blue":
        return (10,10,250)
    if name == "any":
        return (128,128,128)
    if name == "white":
        return (250,250,250)
    return (0,0,0)

def translatePoints(listOfPoints,offset):
    secondList= []
    xOff,yOff = offset
    for x,y in listOfPoints:
        secondList.append( (x+xOff,y+yOff) )
    return secondList

def scalePoints(listOfPoints,mult):
    secondList= []
    xMult,yMult = mult
    for x,y in listOfPoints:
        secondList.append( (x*xMult,y*yMult) )
    return secondList

def rotatePoints(listOfPoints,angle):
    secondList= []
    for x,y in listOfPoints:
        rotX = x*math.cos(angle) - y*math.sin(angle)
        rotY = x*math.sin(angle) + y*math.cos(angle)
        secondList.append( (rotX,rotY) )
    return secondList
