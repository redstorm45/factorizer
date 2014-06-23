

class Level:
    def __init__(self,name,table,inputConfigs,objectives,listTools):
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
