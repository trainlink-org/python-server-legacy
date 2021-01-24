'''
Handles the websocket connections
Copyright (C) 2020  TrainLink Organisation (matt-hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

#imports the sub-modules
import webUtils as utils
import trainlinkObjects
#imports the required external modules
import websockets, asyncio, json



class web:
    """ Serves websocket users """

    # The trainlinkSerial instance
    serialUtils = None

    # The variables needed for configuration
    address = ""
    port = ""
    websocket = None
    mode = "normal"
    debug = False

    # Arrays used for storing runtime data
    power = 0
    users = set()

    cabs = {}
    '''
    cabID = {}
    cabSpeeds = {}
    cabDirections = {}
    cabFunctions = {}
    '''

    logfile = None
    
    # Assigns config variables from arguments
    def __init__ (self, address, port, logfile, debug, cabIDxml, serialUtils):
        self.serialUtils = serialUtils
        self.debug =debug
        self.address = address
        self.port = port
        self.cabID = cabIDxml
        self.logfile = logfile
        for cab in cabIDxml:
            self.cabs[cabIDxml[cab]] = trainlinkObjects.cab(name=cab,address=cabIDxml[cab],functions=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            

    def start(self, mode):
        self.mode = mode
        logfile = self.logfile

        logfile.log("Starting server at %s:%s" %(self.address,self.port))
        logfile.log("Debug enabled", "d")

        start_server = websockets.serve(self.main, self.address, self.port)
        if self.mode == "test":
            logfile.log("Test mode", "dw")
            raise KeyboardInterrupt
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    
    async def notifyState(self, websocket):
        if self.users:
            for user in self.users:
                await self.stateEvent(user)
    
    async def main (self, websocket, path):
        logfile = self.logfile
        self.websocket = websocket
        await self.register(websocket)
        try:
            await self.stateEvent(websocket)
            try:
                async for message in websocket:
                    data = json.loads(message)
                    if data["class"] == "cabControl":
                        self.cabControl(data)
                        await self.notifyState(websocket)
                    elif data["class"] == "directCommand":
                        await self.directCommand(data["command"])
                    elif data["class"] == "power":
                        await self.setPower(data["state"])
                        await self.notifyState(websocket)
                    elif data["class"] == "cabFunction":
                        await self.cabFunction(data)
                        await self.notifyState(websocket)
            except websockets.exceptions.ConnectionClosedError:
                logfile.log("Websocket closed", "d")
        finally:
            await self.unregister(websocket)

    async def register(self, websocket):
        self.logfile.log("New user connected", "d")
        self.users.add(websocket)
        await websocket.send(json.dumps({"type": "config", "cabs": self.cabID,"debug": self.debug}))

    async def unregister(self, websocket):
        self.logfile.log("User disconnected", "d")
        web.users.remove(websocket)

    async def stateEvent(self, websocket):
        for cab in self.cabs:
            await websocket.send(json.dumps({"type": "state", "updateType": "cab", "cab": cab, "speed": self.cabs[cab].getSpeed(), "direction": self.cabs[cab].getDirection(), "functions": self.cabs[cab].getFunctions()}))
        await websocket.send(json.dumps({"type": "state", "updateType": "power", "state": self.power}))
    
    def cabControl(self, data):
        logfile = self.logfile
        try:
            if data["action"] == "setSpeed":
                address = utils.obtainAddress(data["cabAddress"], self.cabID)

                self.cabs[address].setSpeed(data["cabSpeed"])
                self.cabs[address].setDirection(data["cabDirection"])

                #self.cabSpeeds[address] = data["cabSpeed"]
                #self.cabDirections[address] = data["cabDirection"]
            elif data["action"] == "stop":
                address = utils.obtainAddress(data["cabAddress"], self.cabID)
                
                self.cabs[address].setSpeed("0")
                self.cabs[address].setDirection("0")

                #self.cabSpeeds[address] = "0"
                #self.cabDirections[address] = "0"
            elif data["action"] == "estop":
                address = utils.obtainAddress(data["cabAddress"], self.cabID)
                
                self.cabs[address].setSpeed("0")
                self.cabs[address].setDirection("0")
                
        except UnboundLocalError:
            logfile.log("Unknowen Address!", "ed")

    async def directCommand(self, packet):
        await self.serialUtils.directCommand(packet)
    
    async def setPower(self, powerState):
        await self.serialUtils.setPower(powerState)
        self.power = powerState

    async def cabFunction(self, data):
        logfile = self.logfile
        print(data)
        try:
            address = utils.obtainAddress(data["cab"], self.cabID)
            if data["state"] != -1:
                self.cabs[address].setFunction(data["func"],data["state"])
            else:
                print("switching")
                self.cabs[address].setFunction(data["func"],int(not self.cabs[address].getFunction(data["func"])))
            
            legacyMode = True
            if legacyMode:
                await self.serialUtils.setFunction(address, functionStates=self.cabs[address].getFunctions())
            else:
                await self.serialUtils.setFunction(address, function=data["func"], state=data["state"])
        except KeyError:
            logfile.log("Received bad data! (Probably a cab address)", "de")

    def update(self):
        asyncio.run(self.notifyState(self.websocket))