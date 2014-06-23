

level = open("1.level","w")
level.write("transport\n")#level name is "transport"
level.write("6,6\n")      #level has 6*6 cells

for i in range(6):
    for j in range(6):
        if i == 2 and j == 1:
            level.write("in(0,white,-1)\n") #input is white, direction 0, and standard
        elif i == 2 and j == 4:
            level.write("out(-1,any,1)\n")  #output is omnidirectionnal, accept any color, and is refered as output '1'
        else:
            level.write("n\n") #nothing
level.write("1\n") #there is 1 objective
level.write("1.10\n")#output '1' will need 10 cubes

level.write("1\n") #there is 1 object available
level.write("2xbelt(0)\n")#it is a stack of 2 conveyor belts

level.close()
