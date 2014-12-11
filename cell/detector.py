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
        The "Detector" cell 
'''


import pygame
import math
from pygame.locals import *
import cell.cell
import util
import graphics.colors as colors
import globalVars as g

class Detector(cell.cell.Cell):
    
    def __init__(self,infos):
        self.color = infos[0]
        
        self.hasDetector = False

    def makeSurf(self,size):#size is the size of the base square
        outSize = size * 5/4
        
        self.offset = ( -size/4 , -size/4 )

        self.baseSurf   = pygame.Surface( (outSize,outSize) , SRCALPHA)
        self.staticSurf = self.baseSurf
        self.dispSurf   = self.baseSurf
        
        dim1 = size/2
        dim2 = size/8
        points = [ (-dim1     ,dim1     ) ,
                   (-dim1+dim2,dim1-dim2) ,
                   ( dim1-dim2,dim1-dim2) ,
                   ( dim1     ,dim1     ) ]
            
        #colors
        col  = g.color.getForCell(self.color,"detector")
        
        for i in range(4):
            pts = util.translatePoints( util.rotatePoints( points, i*math.pi/2) , (dim1,dim1) )
            pygame.draw.polygon( self.baseSurf , col , pts )
        

    def draw(self,window,pos):
        window.blit( self.baseSurf , pos )

    def makeAnimSurf(self,size,adjCell = [None,None,None,None]):
        
        outSize = size * 5/4
        self.animSurf = pygame.Surface( (outSize,outSize) , SRCALPHA )
        
        dim1 = size/2
        dim2 = size/8
        points = [ (-dim1     ,-dim1     ) ,
                   (-dim1+dim2,-dim1     ) ,
                   (-dim1+dim2,-dim1+dim2) ,
                   (-dim1     ,-dim1+dim2) ]
            
        #colors
        col  = g.color.getForCell(self.color,"activeDetector")
        
        for i in range(4):
            pts = util.translatePoints( util.rotatePoints( points, i*math.pi/2) , (dim1,dim1) )
            pygame.draw.polygon( self.animSurf , col , pts )


