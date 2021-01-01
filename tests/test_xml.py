import trainlinkUtils


def test_answer():
    utils = trainlinkUtils.xmlUtils('config/config.default.xml')
    assert utils.loadXml() != 1
