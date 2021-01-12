from trainlinkUtils import funcToBytes

def test_functobytes():
    states = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert funcToBytes(states,0) ==  [128, None]
    assert funcToBytes(states,1) ==  [176, None]
    assert funcToBytes(states,2) ==  [160, None]
    assert funcToBytes(states,3) ==  [222, 0]
    assert funcToBytes(states,4) ==  [223, 0]
    assert funcToBytes(states,5) ==  0