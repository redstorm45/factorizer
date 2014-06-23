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
