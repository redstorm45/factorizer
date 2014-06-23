'''

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

    def tickModel(self):
        #output boxes
        for b in self.listBoxes:
            theCell = self.level.table[int(b.x)][int(b.y)]
            if isinstance(theCell , cell.output.Output):
                xMid = int(b.x) + 0.5
                yMid = int(b.y) + 0.5
                
                if ( abs(b.x-xMid) < 0.02 and abs(b.y-yMid) < 0.02 ):#box is 1 iteration to the output
                    #give bos to the output
                    theCell.takeBox(b)
                    self.listBoxes.remove(b)
        
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
            
            b.baseForce = (totalForceX , totalForceY)
        
        #TODO : add here a test for collisions
        
        #apply resulting force to the box
        for b in self.listBoxes:
            fx,fy = b.baseForce
            b.x += fx*0.02
            b.y += fy*0.02
            
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
        #only outputs are different
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
            
        #all other cells are directional
        #making a copy of the force
        x,y = c.force
        return (x+0,y+0)
    
    def addBox(self,added):
        self.listBoxes.append(added)

