import math

#blend a new color by multiplying
def multColor(col,ratio):
    r,g,b = col
    return (r*ratio,g*ratio,b*ratio)

def getColorFromStr(name):
    if name == "red":
        return (250,10,10)
    if name == "green":
        return (10,250,10)
    if name == "blue":
        return (10,10,250)
    if name == "any":
        return (128,128,128)
    if name == "white":
        return (250,250,250)
    return (0,0,0)

def translatePoints(listOfPoints,offset):
    secondList= []
    xOff,yOff = offset
    for x,y in listOfPoints:
        secondList.append( (x+xOff,y+yOff) )
    return secondList

def scalePoints(listOfPoints,mult):
    secondList= []
    xMult,yMult = mult
    for x,y in listOfPoints:
        secondList.append( (x*xMult,y*yMult) )
    return secondList

def rotatePoints(listOfPoints,angle):
    secondList= []
    for x,y in listOfPoints:
        rotX = x*math.cos(angle) - y*math.sin(angle)
        rotY = x*math.sin(angle) + y*math.cos(angle)
        secondList.append( (rotX,rotY) )
    return secondList
