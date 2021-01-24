import trainlinkSerial
import trainlinkObjects
import asyncio, pyaddons

def test_serial():
    logfile = pyaddons.logger()
    serial = trainlinkSerial.comms('/dev/ttyNonexistant',logfile)
    serial.updateCabs({"1":trainlinkObjects.cab("train",1),"2":trainlinkObjects.cab("train2", 2)})
#    serial.updateCabs([0,0],[1,1])
    asyncio.get_event_loop().run_until_complete(serial.directCommand("<nonexistant>"))
    asyncio.get_event_loop().run_until_complete(serial.setPower(0))
    asyncio.get_event_loop().run_until_complete(serial.setPower(1))
    asyncio.get_event_loop().run_until_complete(serial.setPower(2))
    asyncio.get_event_loop().run_until_complete(serial.setPower('not a int'))
    asyncio.get_event_loop().run_until_complete(serial.setFunction(3,functionStates=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    serial.readInLoop()
    assert serial.getLatest() == False
