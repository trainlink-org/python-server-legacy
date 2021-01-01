import trainlinkUtils


def test_answer():
    utils = trainlinkUtils.xmlUtils('config/config.default.xml')
    assert utils.loadXml() != 1
    assert utils.listCabs() == {'Train1':'1','Train2':'2'}
    assert utils.loadConfig() == {'ipAddress': '0.0.0.0', 'port': '6789', 'serialPort': '/dev/ttyUSBx', 'debug': 'True'}
