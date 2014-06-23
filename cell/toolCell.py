import pygame
import copy
from pygame.locals import *
import cell.input
import cell.output
import cell.belt

class ToolCell:
    def __init__(self,infos):
        self.number = infos[0]
        self.object = infos[1]
        self.object.placed = True #when copying on the board
        self.selected = False

    def makeSurf(self,width):
        height = width * 1.5
        self.width = width
        
        #make object surface
        self.object.makeSurf(width)
        
        #make base surface
        self.surf = pygame.Surface( (width - min(self.object.offset),height - min(self.object.offset) ) , SRCALPHA)
        
        #make second surface (when selected)
        incr = 0.08 * ( width - min(self.object.offset))
        self.selOffset = -0.5*incr
        self.selSurf = pygame.Surface( ( width - min(self.object.offset) + incr, height - min(self.object.offset) +incr) )
        self.selSurf.fill( ( 203, 56 , 56 ) )
        
        #make new text and font
        self.font = pygame.font.Font(None,int(height/3.5))
        self.numSurf = self.font.render( "x"+str(self.number) , True , (250,250,250) )
        
        #blit all on baseSurf
        self.surf.blit( self.object.baseSurf , (0,0))
        if self.object.staticSurf:
            self.surf.blit( self.object.staticSurf , (0,0))
        offX,offY = self.object.offset
        self.surf.blit( self.numSurf , ( -offX , -offY + width*1.05) )
    
    def rebuildNumSurf(self):
        #make new surface
        self.surf = pygame.Surface( (self.width - min(self.object.offset),self.width*1.5 - min(self.object.offset) ) , SRCALPHA)
        
        #make new text
        self.numSurf = self.font.render( "x"+str(self.number) , True , (250,250,250) )
        
        #blit all on baseSurf
        self.surf.blit( self.object.baseSurf , (0,0))
        if self.object.staticSurf:
            self.surf.blit( self.object.staticSurf , (0,0))
        offX,offY = self.object.offset
        self.surf.blit( self.numSurf , ( -offX , -offY + self.width*1.05) )
    
    def buildCell(self):
        return copy.copy(self.object)
    
    def matchItem(self, i):
        if not isinstance( i , self.object.__class__ ):
            return False
        if (isinstance( i , cell.input.Input ) or 
            isinstance( i , cell.output.Output ) or 
            isinstance( i , cell.belt.Belt )):
            if i.orient != self.object.orient:
                return False
        return True
        
    def makeDispSurf(self,width):#make the surface that will be displayed on the level (when not yet put)
        #create surface
        self.dispObject = copy.copy(self.object)
        self.dispObject.makeSurf(width)
        
        self.dispSurf = self.dispObject.baseSurf.copy()
        if self.dispObject.staticSurf:
            self.dispSurf.blit(self.dispObject.staticSurf,(0,0))
        
    def draw(self,window,offset):
        xOff,yOff = self.object.offset
        xOff2,yOff2 = offset
        x,y = self.drawPos
        if self.selected:
            window.blit(self.selSurf, (x+xOff+xOff2+self.selOffset , y+yOff+yOff2+self.selOffset ))
        window.blit(self.surf, (x+xOff+xOff2 , y+yOff+yOff2 ))
