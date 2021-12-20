import snap7


def clientCreate(ip, rack, slot):
    client__ = snap7.client.Client()
    client__.connect(ip, rack, slot)
    connect__ = client__.get_connected()
    return client__, connect__