import trainlinkSerial
import asyncio

def test_serial():
    serial = trainlinkSerial.comms('/dev/ttyNonexistant')
    serial.updateCabs([0,0],[1,1])
    serial.directCommand("<nonexistant>")