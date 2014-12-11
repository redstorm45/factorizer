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
        The "AdvancedBelt" cell is more advanced than the simple one,
        such that it can respond to control signals
'''


import pygame
import math
from pygame.locals import *
import cell.belt
import util
import graphics.colors as colors
import globalVars as g

class AdvancedBelt(cell.belt.Belt):
    def __init__(self,infos):
        self.orient = int(infos[0])
        self.activeOrient = int(infos[1])

    def makeSurf(self,size):#size is the size of the base square
        outSize = size * 5/4
        
        self.offset = ( -size/4 , -size/4 )

        self.baseSurf = pygame.Surface( (outSize,outSize) , SRCALPHA)
        self.staticSurf = pygame.Surface( (outSize,outSize) , SRCALPHA)
        pointsTop = [ #borders around
                      (0,0) ,
                      (size,0) ,
                      (size,size),
                      (0,size) ]
        pointsRight = [ (size,0) ,
                        (outSize,outSize-size) ,
                        (outSize,outSize),
                        (size,size) ]
        pointsFront = [ (0,size) ,
                        (outSize-size,outSize) ,
                        (outSize,outSize),
                        (size,size) ]
        baseArrowPoints = [ ( size* 1/18,0),
                            ( size* 5/18,size*0.15),
                            ( size* 5/18,-size*0.15)]
        listArrowsPoints=[]
        for i in range(3):
            arrow = util.translatePoints(baseArrowPoints,(size/3 * i - size/2,0) )
            arrow = util.rotatePoints(arrow, self.orient*math.pi/2 +math.pi)
            arrow = util.translatePoints(arrow, (size/2,size/2) )
            listArrowsPoints.append(arrow)

        #colors
        colBase  = g.color.getForCell("any","base")
        colRight = g.color.getForCell("any","right")
        colFront = g.color.getForCell("any","front")
        colArrow = g.color.getForCell("any","arrow")
        #draw the basic shape
        pygame.draw.polygon( self.baseSurf , colBase  , pointsTop   )
        pygame.draw.polygon( self.baseSurf , colRight , pointsRight )
        pygame.draw.polygon( self.baseSurf , colFront , pointsFront )
        #draw outputting arrow
        for i in range(3):
            pygame.draw.polygon( self.staticSurf , colArrow , listArrowsPoints[i] )
        

    def draw(self,window,pos):
        window.blit( self.baseSurf , pos )
        window.blit( self.staticSurf , pos )

    def initAnim(self):
        self.iterAnim = 0

    def updateAnim(self,speed):
        self.iterAnim += 3*speed
        if self.iterAnim >= 50.0:
            self.iterAnim -= 50.0

    def makeAnimSurf(self,size,adjCell = [None,None,None,None]):
        #detect adjacent cells
        nextPresent = False
        prevPresent = False
        
        if isinstance( adjCell[self.orient] , cell.belt.Belt ):
            if adjCell[self.orient].orient == self.orient:
                nextPresent = True
        if isinstance( adjCell[(self.orient+2)%4] , cell.belt.Belt ):
            if adjCell[(self.orient+2)%4].orient == self.orient:
                prevPresent = True
                
        xSubOffset = size*0.1
        ySubOffset = size*0.1
        
        if ((self.orient == 0 and prevPresent) or (self.orient == 2 and nextPresent)):
            xSubOffset = 0
        if ((self.orient == 1 and prevPresent) or (self.orient == 3 and nextPresent)):
            ySubOffset = 0
        
        
        #build surfaces
        outSize = size * 5/4
        
        self.animSurf = pygame.Surface( (outSize,outSize) , SRCALPHA )
        
        subSurf = pygame.Surface( (size,size) , SRCALPHA )
        
        #recalculate positions
        baseArrowPoints = [ ( size* 1/18,0),
                            ( size* 5/18,size*0.15),
                            ( size* 5/18,-size*0.15)]
        listArrowsPoints=[]
        for i in range(4):
            arrow = util.translatePoints(baseArrowPoints,(size/3 * (i - self.iterAnim/50) - size/2,0) )
            arrow = util.rotatePoints(arrow, self.orient*math.pi/2 +math.pi)
            arrow = util.translatePoints(arrow, (size/2,size/2) )
            listArrowsPoints.append(arrow)
            
        #drawing arrows
        colArrow = g.color.getForCell("any","arrow")
        for i in range(4):
            pygame.draw.polygon( subSurf , colArrow , listArrowsPoints[i] )
        
        #blitting
        subSize = int(size*(0.8 + 0.1*nextPresent + 0.1*prevPresent))+1
        self.animSurf.blit( subSurf, (xSubOffset,ySubOffset) , (xSubOffset,ySubOffset,subSize,subSize) )





    

