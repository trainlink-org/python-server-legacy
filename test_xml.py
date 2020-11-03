import trainlinkUtils


def test_answer():
    utils = trainlinkUtils.xmlUtils('config/config.xml')
    assert utils.loadXml() != 1