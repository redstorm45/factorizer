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
        This class defines a simple rectangle,
        and an intersect method
        
        it can have floating point coordinates, unlike pygame.Rect
'''

class Rect:
    def __init__(self,coord,size):
        x,y = coord
        w,h = size
        
        if w<0:
            x = x+w
            w = -w
        if h<0:
            y = y+h
            h = -h
        
        self.left = x
        self.top = y
        self.right = x+w
        self.bottom = y+h
        self.w = w
        self.h = h
    
    def hasCommonPoint(self,r):
        if r.top > self.bottom:
            return False
        if r.left > self.right:
            return False
        if r.bottom < self.top:
            return False
        if r.right < self.left:
            return False
        return True
        
    def intersect(self,r):
        if not self.hasCommonPoint(r):
            return Rect((self.left,self.top),(0,0))
        top = max( r.top , self.top )
        left = max( r.left , self.left )
        bottom = min( r.bottom , self.bottom )
        right = min( r.right , self.right )
        
        return Rect((left,top),(right-left , bottom-top ))
