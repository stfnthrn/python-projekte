from fritzconnection import FritzConnection
fc = FritzConnection(address='192.168.178.1')
fc.reconnect()
print(fc)
