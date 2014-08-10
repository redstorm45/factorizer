
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
        This class is the basic game menu

        It is composed of different screens, which you can scroll through.
        You can select of your level (local only for now),
        and have a preview of it.

        TO DO:
            -finish preview
            -add levels
            -make online playing
              -create a level server
              -create editor
              -make a rank board ?

'''



import pygame
import button
import math
import levelManager
import game
import colors
from pygame.locals import *

SCR_MENU     = 0  #selection local game / challenge
SCR_LEVELS   = 1  #selection of local levels
SCR_PREVIEW  = 2  #previewing of a level
SCR_EDIT     = 3  #when solving the level
SCR_PLAY     = 4  #level is being played
SCR_LEVELEND = 5  #level has finished
#transitions
TRANS_MENU_LEVEL        = 10
TRANS_LEVEL_MENU        = 11
TRANS_LEVEL_PREVIEW     = 12
TRANS_PREVIEW_LEVEL     = 13
TRANS_PREVIEW_EDIT      = 14
TRANS_EDIT_LEVEL        = 15
TRANS_EDIT_PLAY         = 16
TRANS_PLAY_EDIT         = 17
TRANS_PLAY_LEVELEND     = 18
TRANS_LEVELEND_EDIT     = 19
TRANS_LEVELEND_LEVEL    = 20
TRANS_LEVELEND_EDITNEXT = 21


class GameMenu:
    def __init__(self):
        pygame.init()
        
        self.size = (500,500)
        self.currentScreen = SCR_MENU
        self.color = colors.theColors

        self.manager = levelManager.LevelManager()
        self.manager.loadLevels()
        
        self.initMenu()

    def initMenu(self):
        #fonts
        self.fontTitle = pygame.font.Font(None,60)
        self.fontButtons = pygame.font.Font(None,40)
        #generate texts
        self.menuTitleSurf = self.fontTitle.render("MENU",True,self.color.titleFront)
        self.menuTitleShad = self.fontTitle.render("MENU",True,self.color.titleShadow)
        menuTxtBtLvl = self.fontTitle.render("Levels",True,self.color.textButtonMenu)
        menuTxtBtChal = self.fontTitle.render("Challenges",True,self.color.textButtonMenu)
        menuTxtBtBack = self.fontButtons.render("Back",True,self.color.textButtonMenu)
        #buttons
        self.menuBtLvl = button.Button( menuTxtBtLvl , self.color.buttonMenu , (350,75) , 1.05 )
        self.menuBtChal= button.Button( menuTxtBtChal, self.color.buttonMenu , (350,75), 1.05 )
        self.menuBtLvl.pos = (250,175)
        self.menuBtChal.pos = (250,325)
        self.menuBtBack= button.Button( menuTxtBtBack, self.color.buttonMenu , (100,50), 1.15 )
        self.menuBtBack.pos = (250,425)
        self.listBtLevels = []
        for y in range(4):
            lvlLine = []
            for x in range(4):
                if self.manager.levelNb >= 4*y + x + 1:
                    txt = str(4*y + x + 1)
                    txtBt = self.fontButtons.render(txt,True,self.color.textButtonMenu)
                    color = self.color.levelInnactive
                    if y <= 0:
                        color = self.color.levelActive
                    newButton = button.Button( txtBt , color , (50,50) , 1.25 )
                    newButton.pos = (130+80*x,100+80*y)
                    newButton.lvlNum = 4*y + x + 1
                    lvlLine.append( newButton )
                else:
                    lvlLine.append( None )
            self.listBtLevels.append(lvlLine)

    def run(self):
        self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Factory Maker")
        self.clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    self.click( pygame.mouse.get_pos() )
                if event.type == MOUSEMOTION:
                    self.motion( pygame.mouse.get_pos() )
                    
            #draw
            self.draw()

            #update
            self.update()
            self.clock.tick(50)

        pygame.quit()

    def click(self,pos):
        if self.currentScreen == SCR_MENU:
            if(self.menuBtLvl.isClick(pos)):
                self.currentScreen = TRANS_MENU_LEVEL
                self.idleTransition = 0
                self.offsetTransition = 0
        if self.currentScreen == SCR_LEVELS:
            if(self.menuBtBack.isClick(pos)):
                self.currentScreen = TRANS_LEVEL_MENU
                self.idleTransition = 0
                self.offsetTransition = 0
            for x in range(4):
                for y in range(4):
                    if self.listBtLevels[x][y]:
                        if(self.listBtLevels[x][y].isClick(pos)):
                            self.makePreviewForLevel( self.listBtLevels[x][y].lvlNum )
                            self.currentScreen = TRANS_LEVEL_PREVIEW
                            self.idleTransition = 0
                            self.offsetTransition = 0
        if self.currentScreen == SCR_PREVIEW:
            if(self.playground.previewBtBack.isClick(pos)):
                self.currentScreen = TRANS_PREVIEW_LEVEL
                self.idleTransition = 0
                self.offsetTransition = 0
            if(self.playground.previewBtPlay.isClick(pos)):
                self.currentScreen = TRANS_PREVIEW_EDIT
                self.idleTransition = 0
                self.offsetTransition = 0
        if self.currentScreen == SCR_EDIT:
            if(self.playground.editorBtBack.isClick(pos)):
                self.currentScreen = TRANS_EDIT_LEVEL
                self.idleTransition = 0
                self.offsetTransition = 0
            if(self.playground.editorBtTest.isClick(pos)):
                self.playground.initAnim()
                self.currentScreen = TRANS_EDIT_PLAY
                self.idleTransition = 0
                self.offsetTransition = 0
            self.playground.clickEdit(pos)
        if self.currentScreen == SCR_PLAY:
            if(self.playground.playBtStop.isClick(pos)):
                self.currentScreen = TRANS_PLAY_EDIT
                self.idleTransition = 0
                self.offsetTransition = 0
                self.playground.destPlaySpeed = 1.0
                self.playground.playSpeed = 1.0
                self.playground.playing = False
                self.playground.stopped = False
            if(self.playground.playBtPlay.isClick(pos)):
                if not self.playground.stopped:
                    self.playground.initAnim()
                self.playground.playing = True
            if(self.playground.playBtFast.isClick(pos)):
                if self.playground.destPlaySpeed < 16.0:
                    self.playground.destPlaySpeed *= 2.0
            if(self.playground.playBtPause.isClick(pos)):
                self.playground.playing = False
                self.playground.stopped = True
        if self.currentScreen == SCR_LEVELEND:
            if(self.playground.endBtReplay.isClick(pos)):
                self.currentScreen = TRANS_LEVELEND_EDIT
                self.idleTransition = 0
                self.offsetTransition = 0
                self.playground.destPlaySpeed = 1.0
                self.playground.playSpeed = 1.0
                self.playground.playing = False
                self.playground.stopped = False
            if(self.playground.endBtLevels.isClick(pos)):
                self.currentScreen = TRANS_LEVELEND_LEVEL
                self.idleTransition = 0
                self.offsetTransition = 0
            if(self.playground.endBtNext.isClick(pos)):
                nextLvlNum = self.playground.level.number + 1
                nextLvl = self.manager.getLevelByNum(nextLvlNum)
                if nextLvl:
                    self.oldPlayground = self.playground
                    self.makePreviewForLevel(nextLvlNum)
                    self.currentScreen = TRANS_LEVELEND_EDITNEXT
                    self.idleTransition = 0
                    self.offsetTransition = 0
                else:#get back to level selection for now
                    self.currentScreen = TRANS_LEVELEND_LEVEL
                    self.idleTransition = 0
                    self.offsetTransition = 0
    
    def motion(self,pos):
        if self.currentScreen == SCR_EDIT:
            self.playground.moveEdit(pos)

    def update(self):
        #transitions
        if self.currentScreen == TRANS_MENU_LEVEL:
            if self.updateTransition():
                self.currentScreen = SCR_LEVELS
        if self.currentScreen == TRANS_LEVEL_MENU:
            if self.updateTransition(-1):
                self.currentScreen = SCR_MENU
        if self.currentScreen == TRANS_LEVEL_PREVIEW:
            if self.updateTransition():
                self.currentScreen = SCR_PREVIEW
        if self.currentScreen == TRANS_PREVIEW_LEVEL:
            if self.updateTransition(-1):
                self.currentScreen = SCR_LEVELS
        if self.currentScreen == TRANS_PREVIEW_EDIT:
            if self.updateTransition():
                self.currentScreen = SCR_EDIT
        if self.currentScreen == TRANS_EDIT_LEVEL:
            if self.updateTransition(-1):
                self.currentScreen = SCR_LEVELS
        if self.currentScreen == TRANS_EDIT_PLAY:
            if self.updateTransition():
                self.currentScreen = SCR_PLAY
        if self.currentScreen == TRANS_PLAY_EDIT:
            if self.updateTransition(-1):
                self.currentScreen = SCR_EDIT
        if self.currentScreen == TRANS_PLAY_LEVELEND:
            if self.updateTransition(-1):
                self.currentScreen = SCR_LEVELEND
        if self.currentScreen == TRANS_LEVELEND_EDIT:
            if self.updateTransition():
                self.currentScreen = SCR_EDIT
        if self.currentScreen == TRANS_LEVELEND_LEVEL:
            if self.updateTransition(-1):
                self.currentScreen = SCR_LEVELS
        if self.currentScreen == TRANS_LEVELEND_EDITNEXT:
            if self.updateTransition():
                self.currentScreen = SCR_EDIT
                self.oldPlayground = None #clears out the old playground
        #playing field
        if self.currentScreen == SCR_PLAY:
            if self.playground.playing:
                self.playground.tickPlay()
                if self.playground.levelComplete:
                    self.playground.destPlaySpeed = 1.0
                    self.currentScreen = TRANS_PLAY_LEVELEND
                    self.idleTransition = 0
                    self.offsetTransition = 0
        elif (self.currentScreen == TRANS_PLAY_LEVELEND or self.currentScreen == SCR_LEVELEND):
            self.playground.tickPlay()
                
    def updateTransition(self,m = 1): # m: positive or negative multiplier
        self.idleTransition += 1.0
        angle = float(math.pi / 75.0 * self.idleTransition)
        self.offsetTransition = m * 250.0 * ( math.cos( angle ) - 1.0)
        return self.idleTransition >= 75
    
    def makePreviewForLevel(self,levelNum):
        level = self.manager.levelList[levelNum -1]
        self.playground = game.Game(level)
        self.playground.makePreview()
        self.playground.initEditor()
        self.playground.initPlayer()

    def draw(self):
        #background
        self.window.fill(self.color.background)

        if self.currentScreen == SCR_MENU:
            self.drawTitle()
            self.drawMenu()
        if self.currentScreen == SCR_LEVELS:
            self.drawTitle()
            self.drawLevels()
        if self.currentScreen == SCR_PREVIEW:
            self.drawPreview()
        if self.currentScreen == SCR_EDIT:
            self.playground.drawEdit()
        if self.currentScreen == SCR_PLAY:
            self.playground.drawPlay()
        if self.currentScreen == SCR_LEVELEND:
            self.playground.drawPlay((0,0),-500,0)

        #menu<>level
        if self.currentScreen == TRANS_MENU_LEVEL:
            self.drawTitle()
            self.drawMenu( ( self.offsetTransition , 0))
            self.drawLevels( ( 500+self.offsetTransition , 0))
        if self.currentScreen == TRANS_LEVEL_MENU:
            self.drawTitle()
            self.drawMenu( ( self.offsetTransition - 500, 0))
            self.drawLevels( ( self.offsetTransition , 0))
        #level<>preview
        if self.currentScreen == TRANS_LEVEL_PREVIEW:
            self.drawTitle( ( self.offsetTransition , 0))
            self.drawLevels( ( self.offsetTransition , 0))
            self.drawPreview( ( 500+self.offsetTransition , 0))
        if self.currentScreen == TRANS_PREVIEW_LEVEL:
            self.drawTitle( ( self.offsetTransition - 500, 0))
            self.drawLevels( ( self.offsetTransition - 500, 0))
            self.drawPreview( ( self.offsetTransition , 0))
        #preview>edit
        if self.currentScreen == TRANS_PREVIEW_EDIT:
            self.drawPreview( ( 0 , self.offsetTransition ))
            self.playground.drawEdit( ( 0 , 500+self.offsetTransition ))
        #edit>level
        if self.currentScreen == TRANS_EDIT_LEVEL:
            self.drawTitle( ( 0 , self.offsetTransition - 500))
            self.drawLevels( ( 0 , self.offsetTransition - 500))
            self.playground.drawEdit( ( 0 , self.offsetTransition ))
        #edit<>play
        if self.currentScreen == TRANS_EDIT_PLAY:
            self.playground.drawPlay( ( 0 , 0 ) , self.offsetTransition)
        if self.currentScreen == TRANS_PLAY_EDIT:
            self.playground.drawPlay( ( 0 , 0 ) , self.offsetTransition - 500 )
        #play>levelend
        if self.currentScreen == TRANS_PLAY_LEVELEND:
            self.playground.drawPlay( ( 0 , 0 ) , -500 , self.offsetTransition-500 )
        #levelend>edit
        if self.currentScreen == TRANS_LEVELEND_EDIT:
            self.playground.drawPlay( ( 0 , 0 ) , -self.offsetTransition-500 , self.offsetTransition )
        #levelend>level
        if self.currentScreen == TRANS_LEVELEND_LEVEL:
            self.playground.drawPlay( ( self.offsetTransition , 0 ) , -500 , 0 )
            self.drawLevels(( self.offsetTransition-500 , 0 ))
            self.drawTitle( ( self.offsetTransition-500 , 0 ))
        #levelend>next level
        if self.currentScreen == TRANS_LEVELEND_EDITNEXT:
            self.oldPlayground.drawPlay( ( self.offsetTransition , 0 ) , -500 , 0 )
            self.playground.drawEdit( ( self.offsetTransition+500 , 0 ) )

        #update screen
        pygame.display.flip()

    def drawTitle(self,offset = (0,0)):
        xOff , yOff =offset
        self.window.blit( self.menuTitleShad, (188+xOff,53+yOff) )
        self.window.blit( self.menuTitleSurf, (185+xOff,50+yOff) )

    def drawMenu(self,offset = (0,0)):
        #boutons
        self.menuBtLvl.draw(self.window,offset)
        self.menuBtChal.draw(self.window,offset)

    def drawLevels(self,offset = (0,0)):
        self.menuBtBack.draw(self.window,offset)
        for i in range(4):
            for j in range(4):
                if self.listBtLevels[i][j]:
                    self.listBtLevels[i][j].draw(self.window,offset)

    def drawPreview(self,offset = (0,0)):
        self.window.blit( self.playground.preview , offset )



        













        
