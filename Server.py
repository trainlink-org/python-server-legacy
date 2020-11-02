'''
The main file for server, this is the one to run
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

try:
    # Imports required trainlink modules
    import trainlinkSerial, trainlinkWeb, trainlinkUtils
    # Imports required external modules
    import threading, time, asyncio

    # Sets the location of the config file
    configFile = 'config/config.xml'

    # Continues the main logic after the server starts
    def main():
        serialMsg = serialUtils.startComms()
        if server.debug:
            print(serialMsg)
        readloop = threading.Thread(target=readLoop)
        readloop.start()
        while True:
            if killThread:
                break
            serialUtils.updateCabs(server.cabSpeeds, server.cabDirections)
            readSerial = serialUtils.getLatest()
            if readSerial != False:
                if readSerial == "<p2>":
                    if server.debug:
                        print("CURRENT OVERLOAD")
                    server.power = 0
                    server.update()
            time.sleep(0.001)

    def readLoop():
        while True:
            if killThread:
                break
            serialUtils.readInLoop()

    # Loads in the xml module
    xmlUtils = trainlinkUtils.xmlUtils(configFile)
    # Loads in the xml file and checks it actually was loaded correctly
    check = xmlUtils.loadXml()
    if check == 1:
        print("FileLoad failed")

    # Gets the cabs list from the xml
    cabs = xmlUtils.listCabs()
    # Gets the server config from the xml
    config = xmlUtils.loadConfig()

    serialUtils = trainlinkSerial.comms(config["serialPort"])
    # Creates an instance of the trainlinkWeb library
    server = trainlinkWeb.web(config['ipAddress'], config["port"], config["debug"], cabs, serialUtils)

    # Creates a main thread - the server can't run in a second thread, so the main logic has to
    killThread = False
    mainThread = threading.Thread(target=main)
    mainThread.start()


    # Starts the server
    server.start()

except KeyboardInterrupt:
    killThread = True
