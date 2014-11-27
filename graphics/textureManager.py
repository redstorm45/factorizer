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
        This class is able to store texture for use later.
        Its memory usage should be adjustable via the options menu
'''

import graphics.texture as texture
import graphics.colors
import globalVars
from pygame.locals import *
import pygame

# TODO : add adjustable memory usage

class TextureManager:
    
    def __init__(self):
        self.textureDict = {}
        self.fonts = {}
         
    def addTexture(self,t):
        #create the texture object before adding it
        if isinstance( t , dict ):
            t = texture.Texture( t )
        #add a new texture object to the list
        if isinstance( t , texture.Texture ):
            if t.name != "undefined" and not self.hasTexture(t.name):
                self.textureDict[t.name] = t
                print("created texture data for :" , t.name)
    
    def get(self,name):
        #get the texture object
        if not name in self.textureDict.keys():
            return None
        t = self.textureDict[name]
        #check that it is created -> create it if not
        if not t.loaded:
            t.create(t)
            t.loaded = True
        return t
            
    def addFont(self,name,fontClass,size):
        self.fonts[name] = pygame.font.Font(fontClass,size)
    
    def hasTexture(self,name):
        return name in self.textureDict.keys()
    
    def blit(self,dest,name,pos):
        dest.blit( self.get(name).surf , pos )
    
    def createTexture(self,name):
        try:
            self.textureDict[name].create()
        except:
            pass
        
