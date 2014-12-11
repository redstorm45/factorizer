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
        This class describes the boxes,which moves around in the level
'''


import pygame
import util
from pygame.locals import *
import globalVars as g

class Box:
    def __init__(self,color,x,y,size):
        self.color = g.color.getForCell( color , "base" )
        self.size = size
        self.x = x
        self.y = y
        self.velx = 0
        self.vely = 0
        self.height = 0
        self.falling = False
        
        self.makeSurf()
    
    def squareDist(self,other):
        return (self.x-other.x)**2 + (self.y-other.y)**2
    
    def makeSurf(self,iterVoid = 1.0):
        outSize = self.size * 1.25
        size = self.size
        
        self.offset = -self.size*3/4
        
        self.middle = [ (0,0)    , (size,0)    , (size,size)       , (0,size)]
        self.bottom = [ (0,size) , (size,size) , (outSize,outSize) , (outSize-size,outSize)]
        self.right  = [ (size,0) , (size,size) , (outSize,outSize) , (outSize,outSize-size)]
        
        self.surf = pygame.Surface( (outSize,outSize) , SRCALPHA )
        pygame.draw.polygon( self.surf ,                self.color      , self.middle )
        pygame.draw.polygon( self.surf , util.multColor(self.color,0.5) , self.bottom )
        pygame.draw.polygon( self.surf , util.multColor(self.color,0.8) , self.right )
        
        if iterVoid != 1.0 and iterVoid != 0.0 :
            #make the box disapear in darkness
            self.surf.lock()
            for x in range(int(outSize)):
                for y in range(int(outSize)):
                    r,g,b,a = self.surf.get_at( (x,y) )
                    self.surf.set_at( (x,y) , (r,g,b,a*iterVoid) )
            self.surf.unlock()
