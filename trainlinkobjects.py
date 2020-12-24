class train:
    "A single model train"

    name = ""
    address = 0
    speed = 0
    direction = 1
    functions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", None)
        self.address = kwargs.get("address", 3)
        
    def setSpeed(self, speed): self.speed = speed

    def getSpeed(self): return self.speed

    def setDirection(self, direction): self.direction = direction

    def getDirection(self): return self.direction
    
    def setFunction(self, funcNum, state): self.functions[funcNum] = state

    def getFunction(self, funcNum): return self.functions[funcNum]