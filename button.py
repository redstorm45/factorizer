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
import graphics.button
import globalVars as g
from pygame.locals import *

class Button:
    def __init__(self,textSurf,color,inSize,depthRatio,squareView = True,backColor = (50,50,50)):
        #check for valid inputs
        if textSurf == None:
            return
        if depthRatio < 1:
            depthRatio = 1.1
        
        self.textSurf = textSurf
        self.textName = "BT."+textSurf
        self.color = color
        self.backColor = backColor
        insideSurf = g.tManager.get(textSurf).surf
        
        #get the size of inside rect
        inW , inH = inSize
        inW = max(inW,insideSurf.get_width())
        inH = max(inH,insideSurf.get_height())
        
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

        #create the texture
        g.tManager.addTexture( { "name" : "BT."+textSurf ,
                                 "create" : graphics.button.createButton ,
                                 "links" : [ self ] } )

    def isClick(self,pos):
        surf = g.tManager.get(self.textName).surf
        x,y = self.pos
        xLeft = x- surf.get_width()/2
        yTop = y
        xRight = xLeft + surf.get_width()
        yBottom = yTop + surf.get_height()

        xM,yM = pos
        if( xLeft< xM and xRight > xM and yTop<yM and yBottom>yM):
            return True
        return False
        
    def draw(self,dest,offset=(0,0)):
        x,y = self.pos
        offX , offY = offset
        surf = g.tManager.get(self.textName).surf
        g.tManager.blit(dest , self.textName , (x- surf.get_width()/2 + offX,y + offY) )

    def blitCenter(self,dest,pos):
        x,y = pos
        surf = g.tManager.get(self.textName).surf
        g.tManager.blit( dest , self.textName , (x- surf.get_width()/2,y) )















    
