import trainlinkUtils

def test_os():
    utils = trainlinkUtils.osUtils()
    assert utils.getOS() == "linux"