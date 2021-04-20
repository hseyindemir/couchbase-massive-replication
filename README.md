# couchbase-massive-replication
It's an open source python development craft in order to handle huge amaounts of buckets and indexes from one cluster to another. The main purpose of this is provide a better operational experience when working on XDCR replications on Couchbase clusters. 

# Advantages of this project

1. There is no need to think about which buckets are missing when doing XDCR migration
2. There is no need for bucket configurations on source and destination. 
3. If you are trying to migrate huge amount of Couchbase buckets this operation can be completed by simple curl requests for each cluster
4. There is no need to think about indexes. These objects can also be migrated with the help of an endpoint

# How to deploy this project

You can you Dockerfile inside the project. The image is also available in docker hub. You can investigate and use. 

```bash
docker pull demir94/cbmigrator:0.1
docker run -d --name test demir94/cbmigrator:0.1
```

When the service up and running you can send a simple POST requests. An example request body as follows;

http://localhost:1994/migrateAllBuckets

```json
{
    "sourceNodeAddress": "172.17.0.2",
    "destinationNodeAddress": "172.17.0.3",
    "referanceName": "test",
    "loginName": "somelogin",
    "loginSecret": "somepass"

}
```

http://localhost:1994/createNewReplication

```json
{
    "sourceNodeAddress": "172.17.0.2",
    "destinationNodeAddress": "172.17.0.3",
    "referanceName": "test",
    "bucket": "somebucket",
    "loginName": "somelogin",
    "loginSecret": "somepass"

}
```

http://localhost:1994/migrateAllIndexes

```json
{
    "sourceNodeAddress": "172.17.0.2",
    "destinationNodeAddress": "172.17.0.3",
    "loginName": "somelogin",
    "loginSecret": "somepass"

}
```

# How to contribute the project

There is no rule for contributing. Please share your opinions or PRs...

