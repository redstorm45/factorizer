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
        This class decribes the "Input" cell,
        which can spawn new boxes
'''


import pygame
import math
from pygame.locals import *
import cell.cell
import box.box
import util
import graphics.colors as colors

class Input(cell.cell.Cell):
    def __init__(self,infos):
        self.orient = int(infos[0])
        self.color = util.getColorFromStr(infos[1])
        self.spawnConfig = int(infos[2])

        self.standardSpawn = (self.spawnConfig < 0)

    def makeSurf(self,size):#size is the size of the base square
        self.size = size
        
        outSize = size * 5/4
        holeStart = size/4
        holeEnd = size/4 * 3
        platformStart = size/4 + size/16

        self.offset = ( -size/4 , -size/4 )

        self.baseSurf = pygame.Surface( (outSize,outSize) , SRCALPHA)
        self.staticSurf = None
        pointsTop = [ #borders around
                      (0,0) ,
                      (size,0) ,
                      (size,size),
                      (0,size) ,
                      (0,0) ,
                      #hole in the middle
                      (holeStart,holeStart),
                      (holeStart,holeEnd),
                      (holeEnd,holeEnd),
                      (holeEnd,holeStart),
                      (holeStart,holeStart)]
        pointsRight = [ (size,0) ,
                        (outSize,outSize-size) ,
                        (outSize,outSize),
                        (size,size) ]
        pointsFront = [ (0,size) ,
                        (outSize-size,outSize) ,
                        (outSize,outSize),
                        (size,size) ]
        pointsHoleLeft = [ (holeStart,holeStart) ,
                           (holeEnd,holeEnd) ,
                           (holeStart,holeEnd) ]
        pointsHoleTop = [ (holeStart,holeStart) ,
                           (holeEnd,holeEnd) ,
                           (holeEnd,holeStart) ]
        pointsPlatform = [ (platformStart,platformStart) ,
                           (platformStart,size) ,
                           (size,size) ,
                           (size,platformStart) ]
        baseArrowPoints = [ (size/2-size/16,0),
                            (size/4+size/16,size/4),
                            (size/4+size/16,-size/4)]
        pointsArrow = util.translatePoints( util.rotatePoints( baseArrowPoints , self.orient*math.pi/2 ) , (size/2,size/2) )

        #shadow inside the hole
        pygame.draw.polygon( self.baseSurf , colors.theColors.cellRight , pointsHoleLeft )
        pygame.draw.polygon( self.baseSurf , colors.theColors.cellFront , pointsHoleTop )
        #draw the basic shape
        pygame.draw.polygon( self.baseSurf , colors.theColors.cellBase , pointsTop )
        pygame.draw.polygon( self.baseSurf , colors.theColors.cellRight , pointsRight )
        pygame.draw.polygon( self.baseSurf , colors.theColors.cellFront , pointsFront )
        #draw outputting arrow
        pygame.draw.polygon( self.baseSurf , colors.theColors.cellArrow , pointsArrow )
    
    def draw(self,window,pos):
        window.blit( self.baseSurf , pos )

    def initAnim(self):
        self.iterAnim = 50
        self.inputtingBox = None

    def updateAnim(self,speed):
        self.iterAnim += speed
        if self.iterAnim < 100:#wait
            pass
        elif self.iterAnim >= 100:#making the animation
            if not self.inputtingBox:
                self.inputtingBox = self.buildBox()
            if self.iterAnim >= 150:#we want a new cube every 3 seconds
                self.iterAnim -= 150.0
                self.inputtingBox.height = self.size/4
                self.level.physicManager.addBox( self.inputtingBox )
                self.inputtingBox = None
    
    def buildBox(self):
        newBox = box.box.Box( self.color , self.x+0.5 , self.y+0.5 , self.size*0.5 )
        return newBox

    def makeAnimSurf(self,size):
        if self.inputtingBox and self.iterAnim >= 100 and self.iterAnim <= 150:
            animSize = size * 3/4
            animLength = size * 1/2 - self.inputtingBox.offset/3
            animPos = animSize - animLength * (self.iterAnim-100)/50
            self.animSurf = pygame.Surface( (animSize,animSize) ,SRCALPHA)
            self.animSurf.blit( self.inputtingBox.surf , ( animPos,animPos) )
        else:
            self.animSurf = None









    
