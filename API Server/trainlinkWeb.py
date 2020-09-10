#imports the sub-modules
import webUtils as utils
#imports the required external modules
import websockets, asyncio, json



class web:
    """ Serves websocket users """

    # The variables needed for configuration
    address = ""
    port = ""

    # Arrays used for storing runtime data
    users = set()
    cabID = {}
    cabSpeeds = {}
    cabDirections = {}
    
    
    # Assigns config variables from arguments
    def __init__ (self, address, port, cabIDxml):
        self.address = address
        self.port = port
        self.cabID = cabIDxml
        for cab in cabIDxml:
            self.cabSpeeds[cabIDxml[cab]] = 0
            self.cabDirections[cabIDxml[cab]] = 0

    def start(self):
        print("Starting server at %s:%s" %(self.address,self.port))
        start_server = websockets.serve(self.main, self.address, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    
    async def notifyState(self, websocket):
        if self.users:
            for user in self.users:
                await self.stateEvent(user)
    
    async def main (self, websocket, path):
        await self.register(websocket)
        try:
            await self.stateEvent(websocket)
            async for message in websocket:
                data = json.loads(message)
                #print(data)
                if data["class"] == "cabControl":
                    #print("cabControl")
                    self.cabControl(data)
                    await self.notifyState(websocket)
                elif data["class"] == "directCommand":
                    #print(data)
                    pass
                elif data["class"] == "power":
                    pass
        finally:
            await self.unregister(websocket)

    async def register(self, websocket):
        self.users.add(websocket)
        await websocket.send(json.dumps({"type": "config", "cabs": self.cabID}))

    async def unregister(self, websocket):
        web.users.remove(websocket)

    async def stateEvent(self, websocket):
        for cab in self.cabSpeeds:
            await websocket.send(json.dumps({"type": "state", "cab": cab, "speed": self.cabSpeeds[cab], "direction": self.cabDirections[cab]}))
    
    def cabControl(self, data):
        if data["action"] == "setSpeed":
            address = utils.obtainAddress(data["cabAddress"], self.cabID)
            self.cabSpeeds[address] = data["cabSpeed"]
            self.cabDirections[address] = data["cabDirection"]
        elif data["action"] == "stop":
            address = utils.obtainAddress(data["cabAddress"], self.cabID)
            self.cabSpeeds[address] = "0"
        elif data["action"] == "estop":
            address = utils.obtainAddress(data["cabAddress"], self.cabID)
            self.cabSpeeds[address] = "-1"
    