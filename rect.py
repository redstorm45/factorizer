

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
        
    def intersect(self,r):
        top = max( r.top , self.top )
        left = max( r.left , self.left )
        bottom = min( r.bottom , self.bottom )
        right = min( r.right , self.right )
        
        return Rect((left,top),(right-left , bottom-top ))
