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
        This class is where all movements of boxes are calculated
        it is a simplified physic model
'''


import pygame
import cell.cell
import cell.input
import cell.output
import cell.belt
import math
import rect
from pygame.locals import *

class BoxPhysic:
    def __init__(self,level):
        self.level = level
        self.initModel()

    def initModel(self):
        self.listBoxes = []
        self.unprocessedTick = 0
        
        #make force field
        for x in range(self.level.width):
            for y in range(self.level.height):
                if isinstance( self.level.table[x][y] , cell.input.Input ):
                    orient = self.level.table[x][y].orient * math.pi / 2
                    forcePower = 1.0
                    self.level.table[x][y].force = ( forcePower * math.cos(orient) , forcePower * math.sin(orient) )
                elif isinstance( self.level.table[x][y] , cell.belt.Belt ):
                    orient = self.level.table[x][y].orient * math.pi / 2
                    forcePower = 1.0
                    self.level.table[x][y].force = ( forcePower * math.cos(orient) , forcePower * math.sin(orient) )
                elif isinstance( self.level.table[x][y] , cell.cell.Cell ):
                    self.level.table[x][y].force = ( 0 , 0 )

    def tickModel(self,speed):
        self.unprocessedTick += speed
        while self.unprocessedTick >= 1.0:
            self.singleTick()
            self.unprocessedTick -= 1.0
        
    def singleTick(self):
        #output boxes
        for b in self.listBoxes:
            theCell = None
            if int(b.x) in range(self.level.width) and int(b.y) in range(self.level.height):
                theCell = self.level.table[int(b.x)][int(b.y)]
                #make the box disapear in an output
                if isinstance(theCell , cell.output.Output):
                    xMid = int(b.x) + 0.5
                    yMid = int(b.y) + 0.5
                    
                    if ( abs(b.x-xMid) < 0.02 and abs(b.y-yMid) < 0.02 ):#box is 1 iteration to the output
                        #give box to the output
                        theCell.takeBox(b)
                        self.listBoxes.remove(b)
            #the box falls in the void
            if not theCell:
                xDim , yDim = (2 , 2)
                
                #only select cells which the box is on
                if (abs(b.x-int(b.x)) > 0.25) and (abs(b.x-int(b.x+1)) > 0.25): #not near line
                    xDim = 1
                if (abs(b.y-int(b.y)) > 0.25) and (abs(b.y-int(b.y+1)) > 0.25):
                    yDim = 1
                    
                #try to get adjacent cells
                adjCells = [[None,None],[None,None]]
                for x in range(xDim):
                    xCell = int(b.x-0.25)+x
                    for y in range(yDim):
                        yCell = int(b.y-0.25)+y
                        if xCell in range(self.level.width) and yCell in range(self.level.height):
                            adjCells[x][y] = self.level.table[xCell][yCell]
                
                #check for every present cell if the box is on it
                onSthg = False
                for row in adjCells:
                    for c in row:
                        if c:
                            onSthg = True
                
                #TODO : finish check for cell presence under box
                
                if ( not onSthg ):
                    if not b.falling:
                        b.falling = True
                        b.fallIter = 30 
        
        #get each box's applied force
        for b in self.listBoxes:
            #make a rect describing the base of the box
            posBox = rect.Rect( (b.x-0.25,b.y-0.25) , (0.5,0.5) )
            
            totalForceX , totalForceY = (0,0)
            
            #calculate incoming forces
            for i in range(2):
                for j in range(2):
                    #get true position of cell
                    xCell = int(posBox.left+i)
                    yCell = int(posBox.top+j)
                    
                    #extract the cell
                    theCell = None
                    if xCell in range(self.level.width) and yCell in range(self.level.height):
                        theCell = self.level.table[xCell][yCell]
                    
                    force = (0,0)
                    if theCell:
                        #get action area of the cell
                        actionRect = self.getActionRect( theCell  )
            
                        #crop to match with the box (get intersection)
                        interRect = actionRect.intersect( posBox )
            
                        #get area of cropped rect
                        area = interRect.w * interRect.h
                        
                        #get the generated force
                        forceX,forceY = self.getCellForce( theCell , (b.x,b.y))
                        
                        #apply area modification (0.5 * 0.5 = 0.25 is max area)
                        forceX *= (area*4)
                        forceY *= (area*4)
                        
                        totalForceX += forceX
                        totalForceY += forceY
            
            #make the speed tend to these numbers
            diffx = totalForceX*0.2 - b.velx
            diffy = totalForceY*0.2 - b.vely
            
            if abs(diffx) > 0.5:
                diffx = diffx/abs(diffx)*0.5
            if abs(diffy) > 0.5:
                diffy = diffy/abs(diffy)*0.5
            b.baseForce = (diffx,diffy)
        
        #IN PROGRESS : adding a collision test for boxes
        
        self.checkCollisions()
        
        #apply resulting force to the box
        for b in self.listBoxes:
            if b.falling:
                b.fallIter -= 1
                if b.fallIter >0:
                    b.makeSurf( b.fallIter / 30.0 )
                else:
                    self.listBoxes.remove(b)
            else:
                fx,fy = b.baseForce
                b.velx *= 0.9
                b.vely *= 0.9
                b.velx += fx*0.02  #0.02 = 1/50 = multiplier for 1 frame -> 1 s
                b.vely += fy*0.02
                
                b.x += b.velx
                b.y += b.vely
        
        #set display order for the boxes
        self.displaySort()
    
    def checkCollisions(self):
        #step 1: detect collisions
        collisions = []
        for b1 in self.listBoxes:
            for b2 in self.listBoxes:
                c1 = b1 != b2 and (not (b2,b1) in collisions )                    #not taking 2 times the same
                c2 = b1.squareDist(b2) < 2                                        #only take boxes near each other
                c3 = not (b1.falling or b2.falling)  #check not taking a falling box
                if c1 and c2 and c3:
                    r1 = rect.Rect( (b1.x-0.25,b1.y-0.25) , (0.5,0.5) )
                    r2 = rect.Rect( (b2.x-0.25,b2.y-0.25) , (0.5,0.5) )
                    if r1.hasCommonPoint(r2):
                        collisions.append( (b1,b2) )
        
        #step 2: add impulse to them
        # hyp : mass are all equals to 1
        for pair in collisions:
            #get data
            b1,b2 = pair
            r1 = rect.Rect( (b1.x-0.25,b1.y-0.25) , (0.5,0.5) )
            r2 = rect.Rect( (b2.x-0.25,b2.y-0.25) , (0.5,0.5) )
            intersect = r1.intersect(r2)
            
            #get smaller dimension
            little = 1 #width
            if intersect.w > intersect.h:
                little = 2 #height
            
            #build impulse
            impulse = 40*min(intersect.w,intersect.h)
            
            #limit impulse
            if abs(impulse)>0.2:
                impulse= (impulse/abs(impulse))*0.2
            
            #apply to velocities
            b1x,b1y = b1.baseForce
            b2x,b2y = b2.baseForce
            if little == 1:
                b2x += impulse
                b1x -= impulse
            else:
                b2y += impulse
                b1y -= impulse
            b1.baseForce = (b1x,b1y)
            b2.baseForce = (b2x,b2y)
            
    def getActionRect(self,c):
        #belt (cropped edges)
        if isinstance( c , cell.belt.Belt ):
            if c.orient == 0 or c.orient == 2:
                return rect.Rect((c.x,c.y+0.1),(1.0,0.8))
            elif c.orient == 1 or c.orient == 3:
                return rect.Rect((c.x+0.1,c.y),(0.8,1.0))
        #all other cells affect everything
        return rect.Rect((c.x,c.y),(1.0,1.0))
    
    def getCellForce(self,c,posBox):
        #outputs tend to center
        if isinstance( c , cell.output.Output ):
            xBox,yBox = posBox
            toOutX = c.x+0.5-xBox
            toOutY = c.y+0.5-yBox
            dist = math.sqrt( (toOutX)**2 + (toOutY)**2 )
            mult = 1
            if dist <= 0.02:
                mult = dist/0.02
            if dist != 0:
                return ( mult*toOutX / dist , mult*toOutY / dist )
                
        #belt tend to directional axis
        if isinstance( c , cell.belt.Belt ):
            fx,fy = c.force
            
            orientX = False
            if c.orient == 1 or c.orient == 3:
                orientX = True
            xBox,yBox = posBox
            
            dirPosX = c.x+0.5
            dirPosY = c.y+0.5
            
            if orientX:
                dirPosY = yBox
            else:
                dirPosX = xBox
                
            toPosX = dirPosX - xBox
            toPosY = dirPosY - yBox
            
            fx,fy = c.force
            
            toEndX = toPosX*2 + fx
            toEndY = toPosY*2 + fy
            
            distTot = math.sqrt( toEndX**2 + toEndY**2 )
            
            mult = 1
            if distTot <= 0.02:
                mult = distTot/0.02
                
            if distTot != 0:
                return ( mult*toEndX / distTot , mult*toEndY / distTot )
            
        #all other cells are directional
        #making a copy of the force
        x,y = c.force
        return (x+0,y+0)
    
    def displaySort(self):#this function will sort boxes for display
        sortDone = 0
        while (not self.boxSorted()) and (sortDone<len(self.listBoxes)):
            sortDone += 1
            for i in range(len(self.listBoxes)-sortDone):
                b1 = self.listBoxes[i]
                b2 = self.listBoxes[i+1]
                if b1.x+b1.y > b2.x+b2.y:
                    self.listBoxes[i]   = b2
                    self.listBoxes[i+1] = b1
    
    def boxSorted(self):
        for i in range(len(self.listBoxes)-1):
            b1 = self.listBoxes[i]
            b2 = self.listBoxes[i+1]
            if b1.x+b1.y > b2.x+b2.y:
                return False
        return True
    
    def addBox(self,added):
        self.listBoxes.append(added)

