import trainlinkUtils


def test_normal():
    utils = trainlinkUtils.xmlUtils('config/config.default.xml')
    assert utils.loadXml() != 1
    assert utils.listCabs() == {'Train1':'1','Train2':'2'}
    assert utils.loadConfig() == {'ipAddress': '0.0.0.0', 'port': '6789', 'serialPort': '/dev/ttyUSBx', 'debug': 'True'}

def test_alternative():
    utils = trainlinkUtils.xmlUtils('config/config.default.xml')
    utils.loadXml()
    utils.xmlFile['config']['server']['ip'] = 'local'
    utils.xmlFile['config']['cabs']['cab'].pop(1)
    assert utils.listCabs() == {'Train1':'1'}
    assert utils.loadConfig() == {'ipAddress': '127.0.0.1', 'port': '6789', 'serialPort': '/dev/ttyUSBx', 'debug': 'True'}
    
def test_erroneous():
    utils = trainlinkUtils.xmlUtils('nonexistant.xml')
    assert utils.loadXml() == 1
