import requests
def getAllBuckets(serverIp,loginName,loginSecret):
    try:
        urlForHealth = f"http://{serverIp}:8091/pools/default/buckets"
        getNodeDetails = requests.get(
            url=urlForHealth, auth=(loginName, loginSecret))
        resultParsed = getNodeDetails.json()
        bucketList=[]
        for bucket in resultParsed:
            bucketList.append(bucket.get('name'))
        return bucketList
    except Exception as exceptionReis:
        return "fakyu"
def getCocuhbaseServerHealth(serverIp,loginName,loginSecret):
    """
    docstring
    """
    try:
        urlForHealth = f"http://{serverIp}:8091/pools/default"
        getNodeDetails = requests.get(
            url=urlForHealth, auth=(loginName, loginSecret))
        resultParsed = getNodeDetails.json()
        nodeStatus = "not reached"
        for node in resultParsed['nodes']:
            if node.get('hostname') == f"{serverIp}:8091":
                nodeStatus = node
        return True
    except Exception as exceptionReis:
        return False


def checkBucket(serverIp,bucketName,loginName,loginSecret):
    try:
        urlForHealth = f"http://{serverIp}:8091/pools/default/buckets"
        getNodeDetails = requests.get(
            url=urlForHealth, auth=(loginName, loginSecret))
        resultParsed = getNodeDetails.json()
        for bucket in resultParsed:
            existingBucket=bucket.get('name')
            if existingBucket==bucketName:
                return True
        return False
    except Exception as exceptionReis:
        return False
    

def getAllBuckets(serverIp,loginName,loginSecret):
    try:
        urlForHealth = f"http://{serverIp}:8091/pools/default/buckets"
        getNodeDetails = requests.get(
            url=urlForHealth, auth=(loginName, loginSecret))
        resultParsed = getNodeDetails.json()
        bucketList=[]
        for bucket in resultParsed:
            bucketList.append(bucket.get('name'))
        return bucketList
    except Exception as exceptionReis:
        return "fakyu"


def createBucketonDestination(sourceIp, destinationIP, bucketName,loginName,loginSecret):
       try:
            urlForHealth = f"http://{sourceIp}:8091/pools/default/buckets"
            getNodeDetails = requests.get(
                url=urlForHealth, auth=(loginName, loginSecret))
            resultParsed = getNodeDetails.json()
            for bucket in resultParsed:
                existingBucket = bucket.get('name')
                if existingBucket == bucketName:
                    bucketType = bucket.get('bucketType')
                    replicaCount = bucket.get('vBucketServerMap')
                    replicaCount = replicaCount['numReplicas']
                    memoryLimit = bucket.get('quota')
                    memoryLimit = memoryLimit['rawRAM']
                    memoryLimit = int(memoryLimit/1024/1024)
                    bucketRecord = {
                        'name': bucketName,
                        'replicaNumber': replicaCount,
                        'bucketType': bucketType,
                        "ramQuotaMB": memoryLimit
                        }
                    destinationBucketUrl = f"http://{destinationIP}:8091/pools/default/buckets"
                    postNewBucket = requests.post(
                        url=destinationBucketUrl,data=bucketRecord, auth=(loginName, loginSecret))
                    return postNewBucket.text
       except Exception as exceptionReis:
           return exceptionReis



def createReplication(sourceIp, destinationIP, referanceName,bucketName,loginName,loginSecret):
       try:
           hostName=destinationIP+':8091'
           bucketRecord = {
                        'name': referanceName,
                        'hostname': hostName,
                        'username': loginName,
                        "password": loginSecret
                        }
           replRecord = {
                        'fromBucket': bucketName,
                        'toCluster': referanceName,
                        'toBucket': bucketName,
                        "replicationType" : 'continuous'
                        }
           destinationBucketUrl = f"http://{sourceIp}:8091/pools/default/remoteClusters"
           postNewBucket = requests.post(
                url=destinationBucketUrl,data=bucketRecord, auth=(loginName, loginSecret))
           print(postNewBucket.text)
           replicationBucketUrl = f"http://{sourceIp}:8091/controller/createReplication"
           replicationBucket = requests.post(
                url=replicationBucketUrl,data=replRecord, auth=(loginName, loginSecret))
           print(replicationBucket.text)
           return replicationBucket.text
       except Exception as exceptionReis:
           return exceptionReis