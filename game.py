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
        This class is the one where the player will play!

        It is dedicated to a level of the game,
        loaded when initialised.
        It can make a preview of the level, sized to the screen,
        in order to display it in the menu screen
        (previewing is still a part of the menu)

'''

import pygame
import copy
import button
import math
import levelManager
import boxPhysic
import cell.cell
import cell.input
import cell.output
import cell.belt
from pygame.locals import *

colorGround = (100,100,100)

class Game:
    def __init__(self,level):
        self.window = pygame.display.get_surface()
        self.size = self.window.get_size()
        self.level = level

    def initEditor(self):
        #fonts
        self.fontButtons = pygame.font.Font(None,20)
        #generate texts
        textBtBack = self.fontButtons.render("Back",True,(50,50,50))
        textBtTest = self.fontButtons.render("Test",True,(50,50,50))
        
        #make buttons
        self.editorBtBack = button.Button( textBtBack, (180,180,180) , (75,30), 1.15 )
        self.editorBtTest = button.Button( textBtTest, (230,230,230) , (75,30), 1.15 )
        self.editorBtBack.pos = (60,75)
        self.editorBtTest.pos = (60,25)
        
        #init toolbar
        self.listTools = self.level.listTools
        for t in self.listTools:
            t.makeSurf(50) #prepare surfaces for all tools
        self.selectedTool = None
            
        #init visible toolbar
        # TODO : make it possible to have lot of tools
        self.visibleTools = self.listTools
        for i in range(len(self.visibleTools)):
            self.visibleTools[i].drawPos = (100 + 75*i,415)
            
        #make tool object surfaces
        maxDim = max(self.level.height,self.level.width)
        cellSize = 350/maxDim
        for t in self.listTools:
            t.makeDispSurf(cellSize)
            t.phantomPos = (-1,-1)
            
        #make level surface
        self.makeLvlSurf()

    def initPlayer(self):
        #button textures
        surfPlay  = pygame.Surface( (40,40) , SRCALPHA)
        surfPause = pygame.Surface( (40,40) , SRCALPHA)
        surfStop  = pygame.Surface( (40,40) , SRCALPHA)
        pygame.draw.polygon( surfPlay  , (13,125,27) , [ (10,12.5) , (10,27.5) , (30,20) ] )
        pygame.draw.polygon( surfPause , (11,83,145) , [ (10,10)   , (15,10) , (15,30) , (10,30) ] )
        pygame.draw.polygon( surfPause , (11,83,145) , [ (30,10)   , (25,10) , (25,30) , (30,30) ] )
        pygame.draw.polygon( surfStop  , (192,13,0)  , [ (10,10)   , (30,10)   , (30,30)   , (10,30) ] )
        
        #buttons
        self.playBtPlay  = button.Button( surfPlay, (180,180,180) , (50,50), 1.2 )
        self.playBtPause = button.Button( surfPause, (180,180,180) , (50,50), 1.2 )
        self.playBtStop  = button.Button( surfStop, (180,180,180) , (50,50), 1.2 )
        self.playBtPlay.pos = (120,420)
        self.playBtPause.pos = (250,420)
        self.playBtStop.pos = (380,420)
        
        #variable
        self.playing = False
        self.stopped = False
        
        #level : physic manager
        self.level.physicManager = boxPhysic.BoxPhysic(self.level)
        self.level.makeCellReference()
        
    def makePreview(self):
        #fonts
        self.fontTitle = pygame.font.Font(None,50)
        self.fontButtons = pygame.font.Font(None,30)
        #generate texts
        self.titleSurf = self.fontTitle.render(self.level.name,True,(200,200,200))
        textBtBack = self.fontButtons.render("Back",True,(50,50,50))
        textBtPlay = self.fontButtons.render("Play",True,(50,50,50))
        #make buttons
        self.previewBtBack = button.Button( textBtBack, (180,180,180) , (100,50), 1.15 )
        self.previewBtPlay = button.Button( textBtPlay, (180,180,180) , (100,50), 1.15 )
        self.previewBtBack.pos = (75,200)
        self.previewBtPlay.pos = (75,300)
        #create surface
        self.preview = pygame.Surface( self.size )
        self.preview.fill( (50,50,50) )
        self.preview.blit( self.titleSurf , (50,50) )

        #make empty cell surface
        maxDim = max(self.level.height,self.level.width)
        cellSize = 300/maxDim
        self.emptyCellSurf = pygame.Surface( (cellSize,cellSize) , SRCALPHA)
        emptyRect = pygame.Rect(int(0.1*cellSize),int(0.1*cellSize),int(0.9*cellSize),int(0.9*cellSize))
        pygame.draw.rect( self.emptyCellSurf, colorGround , emptyRect )

        #add level surfaces
        for y in range(self.level.height):
            for x in range(self.level.width):
                if (isinstance( self.level.table[x][y], cell.input.Input   ) or
                    isinstance( self.level.table[x][y], cell.output.Output )):
                    drawnCell = self.level.table[x][y]
                    drawnCell.makeSurf(cellSize)
                    xOffset,yOffset = drawnCell.offset
                    xPos = xOffset + 150 + cellSize*x
                    yPos = yOffset + 150 + cellSize*y
                    self.preview.blit( drawnCell.baseSurf , (xPos,yPos) )
                else:#empty cell
                    xPos = 150 + cellSize*x
                    yPos = 150 + cellSize*y
                    self.preview.blit( self.emptyCellSurf , (xPos,yPos) )
        #add buttons
        self.previewBtBack.draw(self.preview)
        self.previewBtPlay.draw(self.preview)
    
    def clickEdit(self,pos):
        x,y = pos
        if y>415:
            #test for toolbar clicks
            for t in self.visibleTools:
                rectTool = pygame.Rect(t.drawPos,t.surf.get_size())
                if( rectTool.collidepoint(pos) ):
                    t.selected = True
                else:
                    t.selected = False
            #set currently selected tool
            self.selectedTool = None
            for t in self.visibleTools:
                if t.selected:
                    self.selectedTool = t
        if( x>150 and y<400 and y>50):
            #click in the edit screen
            maxDim = max(self.level.height,self.level.width)
            cellSize = 350/maxDim
            cellX = int( (x-150) / cellSize )
            cellY = int( (y-50) / cellSize )
            if cellX < self.level.width and cellY < self.level.height and cellX >= 0 and cellY >= 0:
                if self.level.table[cellX][cellY]:
                    #remove old object (replace in toolbar)
                    if self.level.table[cellX][cellY].placed:
                        for t in self.listTools:
                            if t.matchItem( self.level.table[cellX][cellY] ):
                                t.number += 1
                                t.rebuildNumSurf()
                                self.level.table[cellX][cellY] = None
                                self.makeLvlSurf()
                if self.selectedTool:
                    if self.selectedTool.number > 0:
                        #update table (if cell not occupied)
                        if not self.level.table[cellX][cellY]:
                            self.putToolAtCell(cellX,cellY,cellSize)
    
    def putToolAtCell(self,x,y,cellSize):
        self.level.table[x][y] = self.selectedTool.buildCell()
        self.level.table[x][y].makeSurf(cellSize)
        self.selectedTool.number -= 1
        self.selectedTool.rebuildNumSurf()
        self.makeLvlSurf()
    
    def moveEdit(self,pos):
        x , y = pos
        if( x>150 and y<400 and y>50):
            maxDim = max(self.level.height,self.level.width)
            cellSize = 350/maxDim
            hoverX = int( (x-150) / cellSize )
            hoverY = int( (y-50) / cellSize )
            if hoverX < self.level.width and hoverY < self.level.height and hoverX >= 0 and hoverY >= 0:
                if self.selectedTool:
                    if (hoverX,hoverY) != self.selectedTool.phantomPos:
                        self.selectedTool.phantomPos = (hoverX,hoverY)
                        self.makeLvlSurf()
        else:
            if self.selectedTool:
                self.selectedTool.phantomPos = (-1,-1)
            self.makeLvlSurf()
    
    def makeLvlSurf(self):
        #clear surface
        self.editorLvlSurf = pygame.Surface( (400,400) , SRCALPHA) #level base is 350x350
        
        maxDim = max(self.level.height,self.level.width)
        self.cellSize = int(350/maxDim) #round to integer as not to make holes between squares

        #add level surfaces
        for y in range(self.level.height):
            for x in range(self.level.width):
                if (isinstance( self.level.table[x][y], cell.input.Input   ) or
                    isinstance( self.level.table[x][y], cell.output.Output ) or
                    isinstance( self.level.table[x][y], cell.belt.Belt )):
                    drawnCell = self.level.table[x][y]
                    drawnCell.makeSurf(self.cellSize)
                    xOffset,yOffset = drawnCell.offset
                    xPos = xOffset + 50 + self.cellSize*x
                    yPos = yOffset + 50 + self.cellSize*y
                    self.editorLvlSurf.blit( drawnCell.baseSurf , (xPos,yPos) )
                    if drawnCell.staticSurf:
                        self.editorLvlSurf.blit( drawnCell.staticSurf , (xPos,yPos) )
                elif self.selectedTool:
                    if ( (x,y) == self.selectedTool.phantomPos):
                        xOffset,yOffset = self.selectedTool.dispObject.offset
                        xPos = xOffset + 50 + self.cellSize*x
                        yPos = yOffset + 50 + self.cellSize*y
                        self.editorLvlSurf.blit( self.selectedTool.dispSurf , (xPos,yPos) )
                    else:#empty cell
                        xPos = 50 + self.cellSize*x
                        yPos = 50 + self.cellSize*y
                        self.editorLvlSurf.blit( self.emptyCellSurf , (xPos,yPos) )
                else:#empty cell
                    xPos = 50 + self.cellSize*x
                    yPos = 50 + self.cellSize*y
                    self.editorLvlSurf.blit( self.emptyCellSurf , (xPos,yPos) )

    #drawing of the editor (when solving level)
    def drawEdit(self,offset=(0,0)):
        #draw the 2 buttons
        self.editorBtBack.draw(self.window,offset)
        self.editorBtTest.draw(self.window,offset)
        
        #drawing the level
        xOff , yOff = offset
        self.window.blit(self.editorLvlSurf, (xOff + 100,yOff ))
        
        #draw toolbar
        #TODO : make centered
        for i in range(len(self.visibleTools)):
            self.visibleTools[i].draw(self.window,offset)
    
    def drawPlay(self,offset=(0,0),iterate= -500):
        #calculate all offsets
        xOff,yOff = offset
        offsetButtons = (xOff, yOff + iterate)
        offsetToolbar = (xOff, yOff - iterate)
        offsetPlaybar = (xOff  + iterate + 500, yOff)
        offsetLevel   = (xOff  + iterate/10 + 100, yOff)
        
        #draw buttons
        self.editorBtBack.draw(self.window,offsetButtons)
        self.editorBtTest.draw(self.window,offsetButtons)
        
        self.playBtPlay.draw(self.window,offsetPlaybar)
        self.playBtPause.draw(self.window,offsetPlaybar)
        self.playBtStop.draw(self.window,offsetPlaybar)
        
        #drawing the level
        for y in range(self.level.height):
            for x in range(self.level.width):
                xOffLvl,yOffLvl = offsetLevel
                if isinstance(self.level.table[x][y],cell.belt.Belt):
                    drawnCell = self.level.table[x][y]
                    drawnCell.makeAnimSurf(self.cellSize,self.getAdjCells(x,y))
                    xOffset,yOffset = drawnCell.offset
                    xPos = xOffset + 50 + self.cellSize*x + xOffLvl
                    yPos = yOffset + 50 + self.cellSize*y + yOffLvl
                    self.window.blit( drawnCell.baseSurf , (xPos,yPos) )
                    if drawnCell.animSurf:
                        self.window.blit( drawnCell.animSurf , (xPos,yPos) )
                elif isinstance(self.level.table[x][y],cell.cell.Cell):
                    drawnCell = self.level.table[x][y]
                    drawnCell.makeAnimSurf(self.cellSize)
                    xOffset,yOffset = drawnCell.offset
                    xPos = xOffset + 50 + self.cellSize*x + xOffLvl
                    yPos = yOffset + 50 + self.cellSize*y + yOffLvl
                    self.window.blit( drawnCell.baseSurf , (xPos,yPos) )
                    if drawnCell.animSurf:
                        self.window.blit( drawnCell.animSurf , (xPos,yPos) )
                else:#empty cell
                    xPos = 50 + self.cellSize*x + xOffLvl
                    yPos = 50 + self.cellSize*y + yOffLvl
                    self.window.blit( self.emptyCellSurf , (xPos,yPos) )
        
        #draw the boxes
        for b in self.level.physicManager.listBoxes:
            xOffLvl,yOffLvl = offsetLevel
            xPos = b.offset + 37.5 + self.cellSize*b.x + xOffLvl -1
            yPos = b.offset + 37.5 + self.cellSize*b.y + yOffLvl -1
            self.window.blit( b.surf , (xPos,yPos) )
        
        #draw toolbar
        #TODO : make centered
        for i in range(len(self.visibleTools)):
            self.visibleTools[i].draw(self.window,offsetToolbar)
    
    def getAdjCells(self,x,y):
        return [self.getCellAt(x+1,y),
                self.getCellAt(x,y+1),
                self.getCellAt(x-1,y),
                self.getCellAt(x,y-1)]
                
    def getCellAt(self,x,y):
        if (x>=0) and (x<self.level.width) and (y>=0) and (y<self.level.height):
            return self.level.table[x][y]
        return None
    
    def initAnim(self):
        #make cell reference the level
        self.level.makeCellReference()
        
        #build physic model
        self.level.physicManager.initModel()
        
        #initiate anim for cells
        for y in range(self.level.height):
            for x in range(self.level.width):
                if isinstance(self.level.table[x][y],cell.cell.Cell):
                    self.level.table[x][y].initAnim()
    
    def tickPlay(self):
        #update animations
        for y in range(self.level.height):
            for x in range(self.level.width):
                if isinstance(self.level.table[x][y],cell.cell.Cell):
                    self.level.table[x][y].updateAnim()
        
        #update physics (of boxes)
        self.level.physicManager.tickModel()












        
