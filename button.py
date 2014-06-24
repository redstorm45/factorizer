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

'''



import pygame
import util
from pygame.locals import *

class Button:
    def __init__(self,textSurf,color,inSize,depthRatio,squareView = True):
        #check for valid inputs
        if textSurf == None:
            return
        if depthRatio < 1:
            depthRatio = 1.1

        self.textSurf = textSurf
        self.color = color
        #get the size of inside rect
        inW , inH = inSize
        inW = max(inW,textSurf.get_width())
        inH = max(inH,textSurf.get_height())
        #get the size of outside rect
        outW = inW
        outH = inH
        if(squareView):
            aug = 0
            if(inW > inH):
                aug = inW * ( depthRatio -1 )
            else:
                aug = inH * ( depthRatio -1 )
            outW = inW + aug
            outH = inH + aug
        else:
            outW = inW * depthRatio
            outH = inH * depthRatio

        self.size = (outW,outH)
        self.inW = inW
        self.inH = inH
        #generate vertex list
        self.middle = [ (0,0)   , (inW,0)   , (inW,inH) , (0,inH)]
        self.bottom = [ (0,inH) , (inW,inH)   , (outW,outH) , (outW-inW,outH)]
        self.right  = [ (inW,0) , (inW,inH) , (outW,outH)  , (outW,outH-inH)]

        #generate surface
        self.regenSurf()

    def regenSurf(self,color = None):
        if not color:
            color = self.color
        #generate colors
        colorBot = util.multColor(color,0.5)
        colorRig = util.multColor(color,0.8)
        #make surface
        surf = pygame.Surface( self.size )
        surf.fill( (50,50,50) )
        #add polygons
        pygame.draw.polygon( surf,color   ,self.middle )
        pygame.draw.polygon( surf,colorBot,self.bottom )
        pygame.draw.polygon( surf,colorRig,self.right  )
        #add text
        difX = self.inW - self.textSurf.get_width()
        difY = self.inH - self.textSurf.get_height()
        surf.blit( self.textSurf, (difX / 2 , difY / 2) )

        self.surf = surf

    def isClick(self,pos):
        x,y = self.pos
        xLeft = x- self.surf.get_width()/2
        yTop = y
        xRight = xLeft + self.surf.get_width()
        yBottom = yTop + self.surf.get_height()

        xM,yM = pos
        if( xLeft< xM and xRight > xM and yTop<yM and yBottom>yM):
            return True
        return False
        
    def draw(self,dest,offset=(0,0)):
        x,y = self.pos
        offX , offY = offset
        dest.blit( self.surf, (x- self.surf.get_width()/2 + offX,y + offY) )
        

    def blitCenter(self,dest,pos):
        x,y = pos
        dest.blit( self.surf, (x- self.surf.get_width()/2,y) )















    
