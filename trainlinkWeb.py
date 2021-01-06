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
from logging import debug, raiseExceptions
import webUtils as utils
#imports the required external modules
import websockets, asyncio, json
from pyaddons import logger



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
    cabID = {}
    cabSpeeds = {}
    cabDirections = {}
    #cabFunctions = {"1": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "2":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    cabFunctions = {}
    logfile = None
    
    # Assigns config variables from arguments
    def __init__ (self, address, port, logfile, debug, cabIDxml, serialUtils):
        self.serialUtils = serialUtils
        self.debug =debug
        self.address = address
        self.port = port
        self.cabID = cabIDxml
        self.logfile = logfile
        functionFormat = []
        for i in range(0,29):
            functionFormat.append(0)
        cabNames = ['Train1', 'Train2'] 
        for cab in cabIDxml:
            self.cabSpeeds[cabIDxml[cab]] = 0
            self.cabDirections[cabIDxml[cab]] = 0
            self.cabFunctions[str(cabIDxml[cab])] = []
            for i in range(0,29):
                self.cabFunctions[cabIDxml[cab]].append(0)
        self.cabFunctions['1'].append(0)

    def start(self, mode):
        self.mode = mode
        logfile = self.logfile

        logfile.log("Starting server at %s:%s" %(self.address,self.port))
        logfile.log("Debug enabled", "d")
        '''
        print("Starting server at %s:%s" %(self.address,self.port))

        if self.debug == "True":
            print("Debug enabled")
        '''
        start_server = websockets.serve(self.main, self.address, self.port)
        if self.mode == "test":
            logfile.log("Test mode", "dw")
            '''
            print("test mode")
            '''
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
                '''
                if debug:
                    print("websocket closed")
                '''
        finally:
            await self.unregister(websocket)

    async def register(self, websocket):
        self.users.add(websocket)
        await websocket.send(json.dumps({"type": "config", "cabs": self.cabID,"debug": self.debug}))

    async def unregister(self, websocket):
        web.users.remove(websocket)

    async def stateEvent(self, websocket):
        for cab in self.cabSpeeds:
            await websocket.send(json.dumps({"type": "state", "updateType": "cab", "cab": cab, "speed": self.cabSpeeds[cab], "direction": self.cabDirections[cab], "functions": self.cabFunctions[cab]}))
        await websocket.send(json.dumps({"type": "state", "updateType": "power", "state": self.power}))
    
    def cabControl(self, data):
        logfile = self.logfile
        try:
            if data["action"] == "setSpeed":
                address = utils.obtainAddress(data["cabAddress"], self.cabID)
                self.cabSpeeds[address] = data["cabSpeed"]
                self.cabDirections[address] = data["cabDirection"]
            elif data["action"] == "stop":
                address = utils.obtainAddress(data["cabAddress"], self.cabID)
                self.cabSpeeds[address] = "0"
                self.cabDirections[address] = "0"
            elif data["action"] == "estop":
                address = utils.obtainAddress(data["cabAddress"], self.cabID)
                self.cabSpeeds[address] = "-1"
                self.cabDirections[address] = "0"
        except UnboundLocalError:
            logfile.log("Unknowen Address!", "ed")
            '''
            if self.debug:
                print("Unknowen Address!")
            '''

    async def directCommand(self, packet):
        await self.serialUtils.directCommand(packet)
    
    async def setPower(self, powerState):
        await self.serialUtils.setPower(powerState)
        self.power = powerState

    async def cabFunction(self, data):
        logfile = self.logfile
        try:
            address = utils.obtainAddress(data["cab"], self.cabID)
            if data["state"] != -1:
                self.cabFunctions[address][data["func"]] = data["state"]
            else:
                newState = self.cabFunctions[address]
                newState[data["func"]] = int(not newState[data["func"]])
            
            legacyMode = True
            if legacyMode:
                await self.serialUtils.setFunction(address, functionStates=self.cabFunctions[address])
            else:
                await self.serialUtils.setFunction(address, function=data["func"], state=data["state"])
        except KeyError:
            logfile.log("Received bad data! (Probably a cab address)", "de")
            '''
            if debug:
                print("Received bad data! (Probably a cab address)")
            '''
        

    def update(self):
        asyncio.run(self.notifyState(self.websocket))