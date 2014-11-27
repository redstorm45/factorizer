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
        This class stores a particular texture, with all other metadata
        associated with it (name, dimension, loaded or not, priority, etc...)
'''

class Texture:
    
    def __init__(self , data): #initialise the texture with metadata in the "data" dict
        
        #only load texture if there is a name
        if "name" in data.keys() and "create" in data.keys():
            self.name = data["name"]     #name of the texture
            self.create = data["create"] #method used to create the texture
            self.loaded = False          #if the texture is currently in memory (surf arg. exists)
            self.surf = None             #the pygame surface of the texture
            
            try:
                self.priority = data["priority"]
            except:
                self.priority = 1 #only need basic priority checks
            
            #if a texture is marked as temporary, it will be deleted as soon as not in use
            #and regenerated when needed
            try:
                self.temp = data["temp"]
            except:
                self.temp = False #can be deleted at any time, but not ASAP
            
            try:
                self.links = data["links"]
            except:
                self.links = []
            
        else:
            self.name = "unvalid"
        
