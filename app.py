from flask import Flask, redirect, url_for, request
from flask import abort
import json
import time
import couchbaseController.couchbaseBackendHandler as xdcrManager
app = Flask(__name__)


@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"


@app.route('/createNewReplication', methods=['POST'])
def create_task():

    replicationData = json.loads(request.data)

    replicationModel = {
        "sourceNodeAddress": replicationData['sourceNodeAddress'],
        "destinationNodeAddress": replicationData['destinationNodeAddress'],
        "referanceName": replicationData['referanceName'],
        "bucket": replicationData['bucket'],
        "loginName": replicationData['loginName'],
        "loginSecret": replicationData['loginSecret']
    }
    # Check if source and destination exists with the credentials
    isSourceNodeAvailable = xdcrManager.getCocuhbaseServerHealth(
        replicationData['sourceNodeAddress'],replicationData['loginName'],replicationData['loginSecret'])
    isDestinationNodeAvailable = xdcrManager.getCocuhbaseServerHealth(
        replicationData['destinationNodeAddress'],replicationData['loginName'],replicationData['loginSecret'])
    # Check if bucket exists on source
    isBucketAvailableOnSource = xdcrManager.checkBucket(
        replicationData['sourceNodeAddress'], replicationData['bucket'],replicationData['loginName'],replicationData['loginSecret'])

    print(replicationData)

    # Create bucket on destination with source configs
    canApiCreateBucket = isBucketAvailableOnSource and isSourceNodeAvailable and isDestinationNodeAvailable
    finalStatusReport = {
        "sourceNodeUp": isSourceNodeAvailable,
        "destinationUp": isDestinationNodeAvailable,
        "bucketExistsOnSource": isBucketAvailableOnSource,
        "isOkey": canApiCreateBucket
    }
    print(finalStatusReport)

    # Create replication reference
    if canApiCreateBucket == True:
        try:
            bucketCreate = xdcrManager.createBucketonDestination(
                replicationData['sourceNodeAddress'], replicationData['destinationNodeAddress'], replicationData['bucket'],replicationData['loginName'],replicationData['loginSecret'])
            replicatonCreate = xdcrManager.createReplication(
                replicationData['sourceNodeAddress'], replicationData['destinationNodeAddress'], replicationData['referanceName'], replicationData['bucket'],replicationData['loginName'],replicationData['loginSecret'])
            return replicatonCreate
        except Exception as exceptionReis:
           return exceptionReis, 500
    # Push message
    return finalStatusReport, 201


@app.route('/migrateAllBuckets', methods=['POST'])
def migrateBuckets():

    replicationData = json.loads(request.data)

    replicationModel = {
        "sourceNodeAddress": replicationData['sourceNodeAddress'],
        "destinationNodeAddress": replicationData['destinationNodeAddress'],
        "referanceName": replicationData['referanceName'],
        "loginName": replicationData['loginName'],
        "loginSecret": replicationData['loginSecret']
    }
    # Check if source and destination exists with the credentials
    isSourceNodeAvailable = xdcrManager.getCocuhbaseServerHealth(
        replicationData['sourceNodeAddress'],replicationData['loginName'],replicationData['loginSecret'])
    isDestinationNodeAvailable = xdcrManager.getCocuhbaseServerHealth(
        replicationData['destinationNodeAddress'],replicationData['loginName'],replicationData['loginSecret'])
    # Check if bucket exists on source

    # open a loop for all buckets
    bucketListInSource = xdcrManager.getAllBuckets(
        replicationData['sourceNodeAddress'],replicationData['loginName'],replicationData['loginSecret'])
    for bucket in bucketListInSource:
        print("1")
        isBucketAvailableOnSource = xdcrManager.checkBucket(
            replicationData['sourceNodeAddress'], bucket,replicationData['loginName'],replicationData['loginSecret'])
        print(replicationData)
        canApiCreateBucket = isBucketAvailableOnSource and isSourceNodeAvailable and isDestinationNodeAvailable
        # Create bucket on destination with source configs

        finalStatusReport = {
            "sourceNodeUp": isSourceNodeAvailable,
            "destinationUp": isDestinationNodeAvailable,
            "bucketExistsOnSource": isBucketAvailableOnSource,
            "isOkey": canApiCreateBucket
        }
        print(finalStatusReport)
        # Create replication reference
        if canApiCreateBucket == True:
            try:
                bucketCreate = xdcrManager.createBucketonDestination(
                    replicationData['sourceNodeAddress'], replicationData['destinationNodeAddress'], bucket,replicationData['loginName'],replicationData['loginSecret'])
                # sleep&wait 20 seconds
                time.sleep(10)
                replicatonCreate = xdcrManager.createReplication(
                    replicationData['sourceNodeAddress'], replicationData['destinationNodeAddress'], replicationData['referanceName'], bucket,replicationData['loginName'],replicationData['loginSecret'])
            except Exception as exceptionReis:
                return exceptionReis, 500

    # Push message
    return finalStatusReport, 201

@app.route('/migrateAllIndexes', methods=['POST'])
def migrate_indexes():

    replicationData = json.loads(request.data)

    replicationModel = {
        "sourceNodeAddress": replicationData['sourceNodeAddress'],
        "destinationNodeAddress": replicationData['destinationNodeAddress'],
        "loginName": replicationData['loginName'],
        "loginSecret": replicationData['loginSecret']
    }
    results=xdcrManager.getCouchbaseIndexDefinitions(replicationData['sourceNodeAddress'],replicationData['loginName'],replicationData['loginSecret'])
    migratedIndexes=[]
    for result in results:
        indexDefinition=result.get('definition')
        replicaCount=result.get('numReplica')
        indexBucket=result.get('bucket')
        indexDefinition=indexDefinition.split('WITH')
        defitionArrayLength=len(indexDefinition)
        if defitionArrayLength>1:
            indexDefinition.pop(1)
        for definition in indexDefinition:
            postFixOfIndex=' WITH {{"num_replica": {replicaCount} }}'.format(replicaCount=replicaCount)
            fullIndexDefinition=definition+postFixOfIndex
            migratedIndexes.append(fullIndexDefinition)
            try:
                xdcrManager.createIndexOnCouchbase(replicationData['destinationNodeAddress'],replicationData['loginName'],replicationData['loginSecret'],fullIndexDefinition)
            except Exception as exceptionDetails:
                return exceptionDetails,500
    convertJsonToIndexList=json.dumps(migratedIndexes)
    return convertJsonToIndexList,200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1994)
