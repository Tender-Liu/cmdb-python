from cmdb.models import DiskInfo


def getFromDiskInfoById(hostId, diskName):
    diskInfo = DiskInfo.objects.filter(host_id=hostId, disk_name=diskName).first()
    return diskInfo


def setFromDiskInfo(hostId, diskName, sizeGb, sizeBytes):
     diskInfo = DiskInfo.objects.create(
        host_id=hostId,
        disk_name=diskName,
        size_gb=sizeGb,
        size_bytes=sizeBytes
     )
     diskInfo.save()


def updFromDiskInfoByHostId(id, sizeGb, sizeBytes , hostId=None, diskName=None):
    diskInfo = DiskInfo.objects.get(id=id)
    if hostId:
        diskInfo.host_id = hostId
    if diskName:
        diskInfo.disk_name = diskName
    diskInfo.size_gb = sizeGb
    diskInfo.size_bytes = sizeBytes
    diskInfo.state=0
    diskInfo.save()


def delFromDiskInfoByHostId(hostId):
    DiskInfo.objects.filter(host_id=hostId).update(state=1)


def getAllFromDiskInFoByHostId(hostId):
    diskInfoList = DiskInfo.objects.filter(host_id=hostId).iterator()
    return diskInfoList