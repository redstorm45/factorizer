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
        This file can create textures for game.py
        
'''

import pygame
import globalVars as g
from pygame.locals import *

#   ***  button textures   ***
    
#editor
def createBtPlayTx(self):
    self.surf  = pygame.Surface( (40,40) , SRCALPHA)
    pygame.draw.polygon( self.surf , g.color.playGreen , [ (10,12)  , (10,28) , (30,20) ] )

def createBtFastTx(self):
    self.surf  = pygame.Surface( (40,40) , SRCALPHA)
    pygame.draw.polygon( self.surf , g.color.playGreen , [ (8,13)   , (8,27)  , (20,20) ] )
    pygame.draw.polygon( self.surf , g.color.playGreen , [ (20,13)  , (20,27) , (32,20) ] )
    
def createBtRewindTx(self):
    self.surf  = pygame.Surface( (40,40) , SRCALPHA)
    pygame.draw.polygon( self.surf , g.color.playGreen , [ (20,13)  , (20,27) , (8,20)  ] )
    pygame.draw.polygon( self.surf , g.color.playGreen , [ (32,13)  , (32,27) , (20,20) ] )
    
def createBtPauseTx(self):
    self.surf  = pygame.Surface( (40,40) , SRCALPHA)
    pygame.draw.polygon( self.surf , g.color.playBlue  , [ (10,10)  , (15,10) , (15,30) , (10,30) ] )
    pygame.draw.polygon( self.surf , g.color.playBlue  , [ (30,10)  , (25,10) , (25,30) , (30,30) ] )
    
def createBtStopTx(self):
    self.surf  = pygame.Surface( (40,40) , SRCALPHA)
    pygame.draw.polygon( self.surf , g.color.playRed  , [ (10,10)  , (30,10) , (30,30) , (10,30) ] )

#player
def createBtReplayTx(self):
    self.surf  = pygame.Surface( (40,40) )
    self.surf.fill( g.color.buttonMenu )
    pygame.draw.circle(  self.surf , g.color.playBlue   , (20,20) , 15 )
    pygame.draw.circle(  self.surf , g.color.buttonMenu , (20,20) , 10 )
    pygame.draw.polygon( self.surf , g.color.buttonMenu , [ (20,0)  , (40,0)  , (40,20) , (20,20) ] )
    pygame.draw.polygon( self.surf , g.color.playBlue   , [ (20,2)  , (20,14) , (28,8)  ] )
    
def createBtLevelsTx(self):
    self.surf  = pygame.Surface( (40,40) , SRCALPHA)
    pygame.draw.polygon( self.surf , g.color.playBlue   , [ (8,7)   , (13,7)  , (13,12) , (8,12)  ] )
    pygame.draw.polygon( self.surf , g.color.playBlue   , [ (8,17)  , (13,17) , (13,22) , (8,22)  ] )
    pygame.draw.polygon( self.surf , g.color.playBlue   , [ (8,27)  , (13,27) , (13,32) , (8,32)  ] )
    pygame.draw.polygon( self.surf , g.color.playBlue   , [ (18,7)  , (30,7)  , (30,12) , (18,12) ] )
    pygame.draw.polygon( self.surf , g.color.playBlue   , [ (18,17) , (30,17) , (30,22) , (18,22) ] )
    pygame.draw.polygon( self.surf , g.color.playBlue   , [ (18,27) , (30,27) , (30,32) , (18,32) ] )

def createBtNextTx(self):
    self.surf  = pygame.Surface( (40,40) , SRCALPHA)
    pygame.draw.polygon( self.surf   , g.color.playGreen  , [ (25,10) , (30,10) , (30,30) , (25,30) ] )
    pygame.draw.polygon( self.surf   , g.color.playGreen  , [ (10,10) , (10,30) , (25,20) ] )

def createEndLvlTx(self):
    #create surface
    self.surf = pygame.Surface( (500,500) , SRCALPHA )
    
    #draw big rectangle
    pygame.draw.polygon( self.surf, g.color.endBackground , [
                         (40,40) , (460,40) , (460,500) , (40,500)
                         ] )
    
    #make transparent
    self.surf.lock()
    for x in range(self.surf.get_width()):
        for y in range(self.surf.get_height()):
            red,green,blue,a = self.surf.get_at( (x,y) )
            self.surf.set_at( (x,y) , (red,green,blue,a*0.5) )
    self.surf.unlock()
    
    #add buttons
    for name in [ "BT.player.btTx.replay" , "BT.player.btTx.levels" , "BT.player.btTx.next" ]:
        g.tManager.blit(self.surf , name , g.tManager.get(name).links[0].pos )

