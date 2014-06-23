import pygame
import math
from pygame.locals import *
import cell.cell
import box.box
import util

colorBase = (175,175,175)

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
        pygame.draw.polygon( self.baseSurf , util.multColor(self.color,0.8) , pointsHoleLeft )
        pygame.draw.polygon( self.baseSurf , util.multColor(self.color,0.5) , pointsHoleTop )
        #translating platform
        pygame.draw.polygon( self.baseSurf , util.multColor(self.color,0.9) , pointsPlatform )
        #draw the basic shape
        pygame.draw.polygon( self.baseSurf , self.color , pointsTop )
        pygame.draw.polygon( self.baseSurf , util.multColor(self.color,0.8) , pointsRight )
        pygame.draw.polygon( self.baseSurf , util.multColor(self.color,0.5) , pointsFront )
        #draw outputting arrow
        pygame.draw.polygon( self.baseSurf , util.multColor(colorBase,0.5) , pointsArrow )
    
    def draw(self,window,pos):
        window.blit( self.baseSurf , pos )

    def initAnim(self):
        self.iterAnim = 200

    def updateAnim(self):
        self.iterAnim += 1 
        if self.iterAnim>= 150:#we want a new cube every 3 seconds
            self.iterAnim = 0
            self.level.physicManager.addBox( self.buildBox() )
    
    def buildBox(self):
        newBox = box.box.Box( self.color , self.x+0.5 , self.y+0.5 , self.size*0.5 )
        return newBox

    def makeAnimSurf(self,size):
        self.animSurf = None









    
