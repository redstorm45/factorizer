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
        This class is made to have a tooltip of objectives over outputs
        (which appears more when hovered)
'''

import pygame
from pygame.locals import *

class objectiveTooltip:
    def __init__(self,linkedCell,size,requested):
        self.pos = ( linkedCell.x , linkedCell.y )
        linkedCell.tooltip = self
        
        self.requested = requested
        self.complete = False
        self.accepted = 0
        self.size = size
        self.makeSurf()
    
    def accept(self,box):
        self.accepted += 1
        self.makeSurf()
        
        if self.accepted >= self.requested:
            self.complete = True

    def makeSurf(self):
        self.offset = (-self.size * 0.25, -self.size*0.85)
        sizeNear = int(self.size*0.1)
        sizeFar = int(self.size*0.9)
        sizeFarY = int(self.size*0.4)
        sizeY = int(self.size*0.5)
        
        offProgress = int(self.size*0.15)
        maxProgress = int(self.size*0.7)
        heightProgress = int(self.size*0.2)
        
        self.surf = pygame.Surface( (self.size,self.size*0.6) , SRCALPHA )
        pygame.draw.circle( self.surf , (150,150,150) , (sizeNear,sizeNear) , sizeNear )
        pygame.draw.circle( self.surf , (150,150,150) , (sizeFar ,sizeNear) , sizeNear )
        pygame.draw.circle( self.surf , (150,150,150) , (sizeFar,sizeFarY) , sizeNear )
        pygame.draw.circle( self.surf , (150,150,150) , (sizeNear,sizeFarY) , sizeNear )
        pygame.draw.rect( self.surf , (150,150,150) , ( sizeNear , 0.0 , sizeFar-sizeNear , sizeY ) )
        pygame.draw.rect( self.surf , (150,150,150) , ( 0.0 , sizeNear , self.size , (sizeFarY-sizeNear) ) )
        
        pygame.draw.polygon( self.surf , (150,150,150) , [ (sizeY-sizeNear,sizeY),\
                                                           (sizeY+sizeNear,sizeY),\
                                                           (sizeY,sizeY+sizeNear)] )
        
        pygame.draw.rect( self.surf , (230,230,230) , ( offProgress , offProgress , maxProgress , heightProgress ) )
        if self.accepted > 0:
            progress = min(self.accepted / self.requested , 1.0)
            pygame.draw.rect( self.surf , (230,40,40) , ( offProgress , offProgress , int(maxProgress * progress), heightProgress ) )
        
        #make the tooltip transparent
        self.surf.lock()
        for x in range( self.surf.get_width() ):
            for y in range( self.surf.get_height() ):
                r,g,b,a = self.surf.get_at( (x,y) )
                self.surf.set_at( (x,y) , (r,g,b,a*0.6) )
        self.surf.unlock()
        
