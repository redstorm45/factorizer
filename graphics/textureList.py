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
        This class contains all the textures
'''

import graphics.menu
import graphics.text
import graphics.game

import globalVars as g

class textureListing:
    
    def __init__(self):
        pass
    
    def get(self,name):
        if name == "menu":
            return self.getMenu()
        elif name == "preview":
            return self.getPreview()
        elif name == "player":
            return self.getPlayer()
        elif name == "editor":
            return self.getEditor()
    
    def getMenu(self):
        tx = []
        tx.append( { "name" : "menu.title"      , "create" : graphics.menu.createTitle } )
        tx.append( { "name" : "menu.btTxt.lvl"  , "create" : graphics.text.createText ,
                     "temp" : True , "links" : ["title","Levels"] } )
        tx.append( { "name" : "menu.btTxt.chal" , "create" : graphics.text.createText ,
                     "temp" : True , "links" : ["title","Challenges"] } )
        tx.append( { "name" : "menu.btTxt.back" , "create" : graphics.text.createText ,
                     "temp" : True , "links" : ["lButtons","Back"] } )
        return tx
        
    def getPreview(self):
        tx = []
        tx.append( { "name" : "preview.levelTitle"  , "create" : graphics.text.createText ,
                     "temp" : True , "links" : ["xlButtons",None,g.color.titleFront] , "unfinished" : True } )
        tx.append( { "name" : "preview.btText.back" , "create" : graphics.text.createText ,
                     "temp" : True , "links" : ["mButtons","Back"] } )
        tx.append( { "name" : "preview.btText.play" , "create" : graphics.text.createText ,
                     "temp" : True , "links" : ["mButtons","Play"] } )
        return tx
    
    def getEditor(self):
        tx=[]
        tx.append( { "name" : "editor.btText.back" , "create" : graphics.text.createText ,
                     "temp" : True , "links" : ["sButtons","Back"] } )
        tx.append( { "name" : "editor.btText.test" , "create" : graphics.text.createText ,
                     "temp" : True , "links" : ["sButtons","Test"] } )
        return tx
    
    def getPlayer(self):
        tx = []
        tx.append( { "name" : "editor.btTx.play"   , "create" : graphics.game.createBtPlayTx ,
                     "temp" : True} )
        tx.append( { "name" : "editor.btTx.fast"   , "create" : graphics.game.createBtFastTx ,
                     "temp" : True} )
        tx.append( { "name" : "editor.btTx.rewind" , "create" : graphics.game.createBtRewindTx ,
                     "temp" : True} )
        tx.append( { "name" : "editor.btTx.pause"  , "create" : graphics.game.createBtPauseTx ,
                     "temp" : True} )
        tx.append( { "name" : "editor.btTx.stop"   , "create" : graphics.game.createBtStopTx ,
                     "temp" : True} )
        tx.append( { "name" : "player.btTx.replay" , "create" : graphics.game.createBtReplayTx ,
                     "temp" : True} )
        tx.append( { "name" : "player.btTx.levels" , "create" : graphics.game.createBtLevelsTx ,
                     "temp" : True} )
        tx.append( { "name" : "player.btTx.next"   , "create" : graphics.game.createBtNextTx ,
                     "temp" : True} )
        return tx

theList = textureListing()

