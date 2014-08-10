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
        This class store a level
'''



class Level:
    def __init__(self,number,name,table,inputConfigs,objectives,listTools):
        self.number = number
        self.name = name
        self.table = table
        self.inputConfigs = inputConfigs
        self.objectives = objectives
        self.listTools = listTools
        
        self.width = len(table)
        self.height = len(table[0])
        
    def makeCellReference(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.table[x][y]:
                    self.table[x][y].level = self
                    self.table[x][y].x = x
                    self.table[x][y].y = y
