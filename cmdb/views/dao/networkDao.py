from cmdb.models import Network


def getFromNetworkByHostId(hostId, networkName):
    network = Network.objects.filter(host_id=hostId, network_name=networkName).first()
    return network


def updFromNetworkByHostId(id, ipAddress, hostId=None, networkName=None):
    network = Network.objects.get(id=id)
    if hostId:
        network.host_id = hostId
    if networkName:
        network.network_name = networkName
    network.state=0
    network.ip_address = ipAddress
    network.save()


def setFromNetworkByHostId(hostId, networkName, ipAddress):
    network = Network.objects.create(
        host_id=hostId,
        network_name=networkName,
        ip_address=ipAddress
    )
    network.save()


def delFromNetworkById(hostId):
    Network.objects.filter(host_id=hostId).update(state=1)


def getAllFromNetworkByHostId(hostId, state=None):
    networkList = None
    if state is not None:
        networkList = Network.objects.filter(host_id=hostId, state=0).iterator()
    else:
        networkList = Network.objects.filter(host_id=hostId).iterator()
    return networkList
