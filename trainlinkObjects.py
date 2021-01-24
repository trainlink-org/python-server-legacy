class cab:
    "A single model cab"

    name = ""
    address = 0
    speed = 0
    direction = 1
    #functions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    functions = []

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", None)
        self.address = kwargs.get("address", 3)
        self.functions = kwargs.get("functions",0)
        '''for i in range(28):
            self.functions.append(0)'''

    def getName(self): return self.name

    def getAddress(self): return self.address
        
    def setSpeed(self, speed): self.speed = speed

    def getSpeed(self): return self.speed

    def setDirection(self, direction): self.direction = direction

    def getDirection(self): return self.direction
    
    def setFunction(self, funcNum, state): self.functions[funcNum] = state

    def getFunction(self, funcNum): return self.functions[funcNum]

    def getFunctions(self): return self.functions