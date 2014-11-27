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
        This file can create textures for all the menu
        
'''

import pygame
from pygame.locals import *
import globalVars as g

def createTitle(self):
    surfFront = g.tManager.fonts["title"].render("MENU",True,g.color.titleFront)
    surfShad  = g.tManager.fonts["title"].render("MENU",True,g.color.titleShadow)
    
    self.surf = pygame.Surface( (surfShad.get_width()+3,surfShad.get_height()+3) , SRCALPHA )
    self.surf.blit( surfShad , (3,3) )
    self.surf.blit( surfFront, (0,0) )

        
        
        
        
