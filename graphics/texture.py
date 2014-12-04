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
            self.name       = None     #name of the texture
            self.create     = None     #method used to create the texture
            self.loaded     = False    #if the texture is currently in memory (surf arg. exists)
            self.surf       = None     #the pygame surface of the texture
            self.priority   = 1        #priority of the surface
            self.temp       = False    #temporary textures (to make other ones)
            self.links      = []       #links needed to make the texture (to buttons, texts , etc... )
            self.unfinished = False    #some data is still missing
            
            for i in data.keys():
                self.setData( i ,data[i] )
            
            # if a texture is marked as temporary, it will be deleted as soon as not in use
            # and regenerated when needed. else, it
            # can be deleted at any time, but not ASAP
            
        else:
            self.name = "unvalid"
            
    def setData(self,name,data):
        if name == "name":
            self.name = data
        elif name == "create":
            self.create = data
        elif name == "priority":
            self.priority = data
        elif name == "temp":
            self.temp = data
        elif name == "links":
            if self.links:
                for i in range(len(data)):
                    if data[i]:
                        self.links[i] = data[i]
            else:
                self.links = data
        elif name == "unfinished":
            self.unfinished = data
        return self #to make multiple assignation
    
    def finish(self):
        self.setData("unfinished",False)
            
        return self #to make multiple assignation
