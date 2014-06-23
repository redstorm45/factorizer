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
        #get each box's applied force
        for b in self.listBoxes:
            #make a rect describing the base of the box
            posBox = pygame.Rect( (b.x-0.25,b.y-0.25) , (0.5,0.5) )
            
            print("box at "+str(b.x)+" "+str(b.y)+" rect :"+str(posBox) )
            
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
                        rect = self.getActionRect( theCell  )
            
                        #crop to match with the box (get intersection)
                        interRect = rect.clip( posBox)
            
                        #get area of cropped rect
                        area = interRect.w * interRect.h
                        print("at "+str(xCell)+" "+str(yCell)+" got r1 :"+str(rect)+" making "+str(interRect))
                        print("at "+str(xCell)+" "+str(yCell)+" got area :"+str(area) )
            
                        #get the generated force
                        forceX,forceY = self.getCellForce( theCell , (b.x,b.y))
                        
                        #apply area modification (0.5 * 0.5 = 0.25 is max area)
                        forceX *= (area*4)
                        forceY *= (area*4)
                        
                        force = (forceX,forceY)
                    fx,fy = force
                    totalForceX += fx
                    totalForceY += fy
                    #print("at "+str(xCell)+" "+str(yCell)+" got force :"+str(force) )
                    
            #apply resulting force to the box
            b.x += totalForceX*0.05
            b.y += totalForceY*0.05
            
    def getActionRect(self,c):
        #belt (cropped edges)
        if isinstance( c , cell.belt.Belt ):
            if c.orient == 0 or c.orient == 2:
                return pygame.Rect((c.x,c.y+0.1),(1,0.8))
            elif c.orient == 1 or c.orient == 3:
                return pygame.Rect((c.x+0.1,c.y),(0.8,1))
        #all other cells affect everything
        return pygame.Rect((c.x,c.y),(1,1))
    
    def getCellForce(self,c,posBox):
        
        #only outputs are different
        if isinstance( c , cell.output.Output ):
            xBox,yBox = posBox
            toOutX = abs(c.x+0.5-xBox)
            toOutY = abs(c.y+0.5-yBox)
            dist = math.sqrt( (toOutX)**2 + (toOutY)**2 )
            if dist != 0:
                return ( toOutX / dist , toOutY / dist )
            
        #all other cells are directional
        return c.force
    
    def addBox(self,added):
        self.listBoxes.append(added)

