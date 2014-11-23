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
import objectiveTooltip
import colors
from pygame.locals import *

colorGround = (100,100,100)

class Game:
    def __init__(self,level):
        self.window = pygame.display.get_surface()
        self.size = self.window.get_size()
        self.level = level
        self.color = colors.theColors

    def initEditor(self):
        #fonts
        self.fontButtons = pygame.font.Font(None,20)
        #generate texts
        textBtBack = self.fontButtons.render("Back",True,self.color.textButtonMenu)
        textBtTest = self.fontButtons.render("Test",True,self.color.textButtonMenu)
        
        #make buttons
        self.editorBtBack = button.Button( textBtBack, self.color.buttonMenu     , (75,30), 1.15 )
        self.editorBtTest = button.Button( textBtTest, self.color.buttonMenuTest , (75,30), 1.15 )
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
        # TODO : only load these textures once
        maxDim = max(self.level.height,self.level.width)
        cellSize = 350/maxDim
        for t in self.listTools:
            t.makeDispSurf(cellSize)
            t.phantomPos = (-1,-1)
            
        #make level surface
        self.makeLvlSurf()

    def initPlayer(self):
        #making button textures
        surfPlay  = pygame.Surface( (40,40) , SRCALPHA)
        surfFast  = pygame.Surface( (40,40) , SRCALPHA)
        surfPause = pygame.Surface( (40,40) , SRCALPHA)
        surfStop  = pygame.Surface( (40,40) , SRCALPHA)
        
        surfReplay  = pygame.Surface( (40,40) )
        surfLevels  = pygame.Surface( (40,40) , SRCALPHA)
        surfNext    = pygame.Surface( (40,40) , SRCALPHA)
        #drawing on the button textures
        pygame.draw.polygon( surfPlay  , self.color.playGreen , [ (10,12)  , (10,28) , (30,20) ] )
        pygame.draw.polygon( surfFast  , self.color.playGreen , [ (8,13)   , (8,27)  , (20,20) ] )
        pygame.draw.polygon( surfFast  , self.color.playGreen , [ (20,13)  , (20,27) , (32,20) ] )
        pygame.draw.polygon( surfPause , self.color.playBlue  , [ (10,10)  , (15,10) , (15,30) , (10,30) ] )
        pygame.draw.polygon( surfPause , self.color.playBlue  , [ (30,10)  , (25,10) , (25,30) , (30,30) ] )
        pygame.draw.polygon( surfStop  , (192,13,0)  , [ (10,10)  , (30,10) , (30,30) , (10,30) ] )
        
        surfReplay.fill( (180,180,180) )
        pygame.draw.circle(  surfReplay , self.color.playBlue   , (20,20) , 15 )
        pygame.draw.circle(  surfReplay , self.color.buttonMenu , (20,20) , 10 )
        pygame.draw.polygon( surfReplay , self.color.buttonMenu , [ (20,0)  , (40,0)  , (40,20) , (20,20) ] )
        pygame.draw.polygon( surfReplay , self.color.playBlue   , [ (20,2)  , (20,14) , (28,8)  ] )
        pygame.draw.polygon( surfLevels , self.color.playBlue   , [ (8,7)   , (13,7)  , (13,12) , (8,12)  ] )
        pygame.draw.polygon( surfLevels , self.color.playBlue   , [ (8,17)  , (13,17) , (13,22) , (8,22)  ] )
        pygame.draw.polygon( surfLevels , self.color.playBlue   , [ (8,27)  , (13,27) , (13,32) , (8,32)  ] )
        pygame.draw.polygon( surfLevels , self.color.playBlue   , [ (18,7)  , (30,7)  , (30,12) , (18,12) ] )
        pygame.draw.polygon( surfLevels , self.color.playBlue   , [ (18,17) , (30,17) , (30,22) , (18,22) ] )
        pygame.draw.polygon( surfLevels , self.color.playBlue   , [ (18,27) , (30,27) , (30,32) , (18,32) ] )
        pygame.draw.polygon( surfNext   , self.color.playGreen  , [ (25,10) , (30,10) , (30,30) , (25,30) ] )
        pygame.draw.polygon( surfNext   , self.color.playGreen  , [ (10,10) , (10,30) , (25,20) ] )
        #buttons
        self.playBtPlay  = button.Button( surfPlay  , self.color.buttonMenu , (50,50), 1.2 )
        self.playBtFast  = button.Button( surfFast  , self.color.buttonMenu , (50,50), 1.2 )
        self.playBtPause = button.Button( surfPause , self.color.buttonMenu , (50,50), 1.2 )
        self.playBtStop  = button.Button( surfStop  , self.color.buttonMenu , (50,50), 1.2 )
        self.endBtReplay = button.Button( surfReplay, self.color.buttonMenu , (50,50), 1.2 , True , None )
        self.endBtLevels = button.Button( surfLevels, self.color.buttonMenu , (50,50), 1.2 , True , None )
        self.endBtNext   = button.Button( surfNext  , self.color.buttonMenu , (50,50), 1.2 , True , None )
        self.playBtPlay.pos  = (100,420)
        self.playBtFast.pos  = (200,420)
        self.playBtPause.pos = (300,420)
        self.playBtStop.pos  = (400,420)
        self.endBtReplay.pos = (120,420)
        self.endBtLevels.pos = (250,420)
        self.endBtNext.pos   = (380,420)
        
        #variable
        self.playing = False
        self.stopped = False
        self.playSpeed = 1.0
        self.destPlaySpeed = 1.0
        
        #level : physic manager
        self.level.physicManager = boxPhysic.BoxPhysic(self.level)
        self.level.makeCellReference()
        
        #make the end level surface
        self.endLvlSurf = pygame.Surface( (500,500) , SRCALPHA )
        pygame.draw.polygon( self.endLvlSurf, (100,100,100) , [
                              (40,40) , (460,40) , (460,480) , (40,480)
                              ] )
        self.endLvlSurf.lock()
        for x in range(self.endLvlSurf.get_width()):
            for y in range(self.endLvlSurf.get_height()):
                r,g,b,a = self.endLvlSurf.get_at( (x,y) )
                self.endLvlSurf.set_at( (x,y) , (r,g,b,a*0.5) )
        self.endLvlSurf.unlock()
                
        
    def makePreview(self):
        #fonts
        self.fontTitle = pygame.font.Font(None,50)
        self.fontButtons = pygame.font.Font(None,30)
        #generate texts
        self.titleSurf = self.fontTitle.render(self.level.name,True,(200,200,200))
        textBtBack = self.fontButtons.render("Back",True,self.color.textButtonMenu)
        textBtPlay = self.fontButtons.render("Play",True,self.color.textButtonMenu)
        #make buttons
        self.previewBtBack = button.Button( textBtBack, self.color.buttonMenu , (100,50), 1.15 )
        self.previewBtPlay = button.Button( textBtPlay, self.color.buttonMenu , (100,50), 1.15 )
        self.previewBtBack.pos = (75,200)
        self.previewBtPlay.pos = (75,300)
        #create surface
        self.preview = pygame.Surface( self.size )
        self.preview.fill( self.color.background )
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
                levelCell = self.getCellAt(x,y)
                if (isinstance( levelCell, cell.input.Input   ) or
                    isinstance( levelCell, cell.output.Output )):
                    levelCell.makeSurf(cellSize)
                    xOffset,yOffset = levelCell.offset
                    xPos = xOffset + 150 + cellSize*x
                    yPos = yOffset + 150 + cellSize*y
                    self.preview.blit( levelCell.baseSurf , (xPos,yPos) )
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
        self.cellSize = int(350/maxDim) #round to integer as to make less holes between tiles

        #add level surfaces
        for y in range(self.level.height):
            for x in range(self.level.width):
                levelCell = self.getCellAt(x,y)
                if (isinstance( levelCell, cell.input.Input   ) or
                    isinstance( levelCell, cell.output.Output ) or
                    isinstance( levelCell, cell.belt.Belt )):
                    levelCell.makeSurf(self.cellSize)
                    xOffset,yOffset = levelCell.offset
                    xPos = xOffset + 50 + self.cellSize*x
                    yPos = yOffset + 50 + self.cellSize*y
                    self.editorLvlSurf.blit( levelCell.baseSurf , (xPos,yPos) )
                    if levelCell.staticSurf:
                        self.editorLvlSurf.blit( levelCell.staticSurf , (xPos,yPos) )
                elif self.selectedTool:
                    if ( (x,y) == self.selectedTool.phantomPos) and self.selectedTool.number > 0:
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
    
    #draw the level (when it may be moving)
    def drawPlay(self,offset=(0,0),iterate= -500,iterateEnd= -500):
        #calculate all offsets
        xOff,yOff = offset
        offsetButtons = (xOff, yOff + iterate)
        offsetToolbar = (xOff, yOff - iterate)
        offsetPlaybar = (xOff  + iterate + iterateEnd + 1000, yOff)
        offsetLevel   = (xOff  + iterate/10 + 100, yOff)
        offsetEnd     = (xOff ,yOff - iterateEnd )
        
        #draw buttons
        self.editorBtBack.draw(self.window,offsetButtons)
        self.editorBtTest.draw(self.window,offsetButtons)
        
        if iterateEnd != 0:
            self.playBtPlay.draw(self.window,offsetPlaybar)
            self.playBtFast.draw(self.window,offsetPlaybar)
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
        
        
        #draw output tooltip
        for y in range(self.level.height):
            for x in range(self.level.width):
                xOffLvl,yOffLvl = offsetLevel
                if isinstance(self.level.table[x][y],cell.output.Output):
                    for o in self.objectives:
                        if o.pos == (x,y):
                            xOffset,yOffset = o.offset
                            offProgress = int( self.cellSize*0.6*(1.0+(iterate+iterateEnd+500)/500.0))
                            xPos = xOffset + 50 + self.cellSize*x + xOffLvl
                            yPos = yOffset + 50 + self.cellSize*y + yOffLvl + offProgress
                            self.window.blit( o.surf , (xPos,yPos) , (0,0,self.cellSize,int(self.cellSize*0.6 - offProgress)))
        #draw toolbar
        #TODO : make centered
        for i in range(len(self.visibleTools)):
            self.visibleTools[i].draw(self.window,offsetToolbar)
            
        #draw end screen
        self.window.blit( self.endLvlSurf , offsetEnd )
        
        self.endBtReplay.draw(self.window,offsetEnd)
        self.endBtLevels.draw(self.window,offsetEnd)
        self.endBtNext.draw(self.window,offsetEnd)
    
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
                    
        #initialize objectives
        self.objectives = []
        for o in self.level.objectives:
            self.objectives.append( objectiveTooltip.objectiveTooltip( self.getCellAt( *o[0] ) , self.cellSize , o[1] ) )
    
    def tickPlay(self):
        #update animations
        for y in range(self.level.height):
            for x in range(self.level.width):
                if isinstance(self.level.table[x][y],cell.cell.Cell):
                    self.level.table[x][y].updateAnim(self.playSpeed)
        
        #update physics (of boxes)
        self.level.physicManager.tickModel(self.playSpeed)
        
        #check if the level is finished
        self.levelComplete = True
        for o in self.objectives:
            if not o.complete:
                self.levelComplete = False
                
        #update speed
        diff = self.destPlaySpeed - self.playSpeed
        if abs(diff) > 0.75:
            diff = diff*0.75 /abs(diff)
        self.playSpeed += diff / 10.0
        












        
