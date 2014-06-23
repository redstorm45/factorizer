
import pygame
import util
from pygame.locals import *


class Box:
    def __init__(self,color,x,y,size):
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        
        self.makeSurf()
    
    def makeSurf(self):
        size = self.size
        outSize = size * 1.25
        
        self.offset = -self.size*3/4
        
        self.middle = [ (0,0)    , (size,0)    , (size,size)       , (0,size)]
        self.bottom = [ (0,size) , (size,size) , (outSize,outSize) , (outSize-size,outSize)]
        self.right  = [ (size,0) , (size,size) , (outSize,outSize) , (outSize,outSize-size)]
        
        self.surf = pygame.Surface( (outSize,outSize) , SRCALPHA )
        pygame.draw.polygon( self.surf ,                self.color      , self.middle )
        pygame.draw.polygon( self.surf , util.multColor(self.color,0.5) , self.bottom )
        pygame.draw.polygon( self.surf , util.multColor(self.color,0.8) , self.right )
