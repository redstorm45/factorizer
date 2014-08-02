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
    def __init__(self,linkedCell,size):
        self.pos = ( linkedCell.x , linkedCell.y )
        linkedCell.tooltip = self
        
        self.size = size
        self.makeSurf()

    def makeSurf(self):
        self.offset = (-self.size * 0.25, -self.size*0.25)
        
        self.surf = pygame.Surface( (self.size,self.size) , SRCALPHA )
        self.surf.fill( (200,200,200,150) )
