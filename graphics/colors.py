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
        This class contains all the colors
'''

import util


class Color:
    def __init__(self):
        self.background     = (50 ,50 ,50 )
        self.levelActive    = (250,250,250)
        self.levelInnactive = (100,100,100)
        self.buttonMenu     = (180,180,180)
        self.buttonMenuTest = (230,230,230)
        self.textButtonMenu = (50 ,50 ,50 )
        self.titleFront     = (200,200,200)
        self.titleShadow    = (100,100,100)
        self.endBackground  = (100,100,100)
        self.playGreen      = (13 ,125,27 )
        self.playBlue       = (11 ,83 ,145)
        self.playRed        = (192,13 ,0  )
        
        self.cellBase       = (200,200,200)
        self.cellRight      = (160,160,160)
        self.cellFront      = (100,100,100)
        self.cellArrow      = (100,100,100)
        
        self.detector       = (120,120,120)
        self.activeDetector = (220,220,220)
        
        self.baseColors = {
            "red":  (250,20 ,20 ) ,
            "green":(20 ,250,20 ) ,
            "blue": (20 ,20 ,250) ,
            "any":  (200,200,200) ,
            "white":(250,250,250) ,
            }
            
    def getForCell(self,col,side):
        try:
            if side == "base":
                return util.multColors( self.baseColors[col] , self.cellBase )
            elif side == "right":
                return util.multColors( self.baseColors[col] , self.cellRight )
            elif side == "front":
                return util.multColors( self.baseColors[col] , self.cellFront )
            elif side == "arrow":
                return util.multColors( self.baseColors[col] , self.cellArrow )
            elif side == "detector":
                return util.multColors( self.baseColors[col] , self.detector )
            elif side == "activeDetector":
                return util.multColors( self.baseColors[col] , self.activeDetector )
        except:
            pass
        return (0,0,0)

theColors = Color()
        
        
