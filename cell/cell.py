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
        This class defines a basic Cell of a level,
        and is used for subclassing
'''


import pygame
from pygame.locals import *

class Cell:
    def __init__(self,infos):
        self.baseSurf = None  #the basic surface that doesn't move
        self.animSurf = None  #the surface wich is animated
    
    #making the basic surfaces
    def makeSurf(self,size):
        pass
    
    #making the current anim surf
    def makeAnimSurf(self,size):
        pass

    #drawing this cell
    def draw(self,window):
        pass
    
    #initialising animation variables
    def initAnim(self):
        pass
    
    #updating animation variables
    def updateAnim(self):
        pass
