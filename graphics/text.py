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
        This file can create textures of text, for use in buttons for example
        
'''

import globalVars as g

#
# first argument is the name of the font
# second argument is the text to write
def createText(self):
    color = None
    try:
        color = self.links[2]
    except:
        color = g.color.textButtonMenu
    self.surf = g.tManager.fonts[self.links[0]].render(self.links[1],True,color)
    
    
    
