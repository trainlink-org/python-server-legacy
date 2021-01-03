import Server

assert Server.main("test") == 0
assert Server.main("test","nonexistant.xml") == 1