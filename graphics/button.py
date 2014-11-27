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
        This file can create textures for buttons
        
'''

import pygame
import util
import globalVars as g
from pygame.locals import *

def createButton(self):
    but = self.links[0]
    
    #generate colors
    color = but.color
    colorBot = util.multColor(color,0.5)
    colorRig = util.multColor(color,0.8)
    #make surface
    surf = None
    if but.backColor:
        surf = pygame.Surface( but.size )
        surf.fill( but.backColor )
    else:
        surf = pygame.Surface( but.size , SRCALPHA )
    #add polygons
    pygame.draw.polygon( surf, color   , but.middle )
    pygame.draw.polygon( surf, colorBot, but.bottom )
    pygame.draw.polygon( surf, colorRig, but.right  )
    #add text
    difX = but.inW - g.tManager.get(but.textSurf).surf.get_width()
    difY = but.inH - g.tManager.get(but.textSurf).surf.get_height()
    g.tManager.blit( surf , but.textSurf , (difX / 2 , difY / 2) )
    self.surf = surf

    
    
    
    
