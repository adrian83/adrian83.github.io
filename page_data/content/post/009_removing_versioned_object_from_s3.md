---
title: Removing versioned object from AWS S3
date: 2020-10-15
draft: false
categories:
- aws
- python
- s3
- boto3
tags:
- aws
- python
- s3
- boto3
---

### Always, when I try to remove versioned object from S3 bucket, I wonder, why there is no possibility to do this from AWS console.

If you, similary as I, wasted too much time to remove versioned objects from S3, you probably have prepared script for doing this. If not, you can use this simple Python script.



```
import boto3
import sys

maxVersions = 30

versionsLabel = "Versions"
versionIdLabel = "VersionId"
nextVersionIdMarkerLabel = "NextVersionIdMarker"


bucket = sys.argv[1]
obj = sys.argv[2]

print("Removing object {0} from bucket {1}".format(obj, bucket))

client = boto3.client('s3')

nextVersionIdMarker = None

while True:

    response = client.list_object_versions( \
        Bucket=bucket, MaxKeys=5, KeyMarker=obj, Prefix=obj, VersionIdMarker=nextVersionIdMarker) \
        if nextVersionIdMarker else client.list_object_versions(Bucket=bucket, MaxKeys=5, Prefix=obj)

    if versionsLabel not in response:
        print("No {} in response. Exiting...".format(versionsLabel))
        sys.exit(0)

    versions = response[versionsLabel]

    for version in versions:
        version = version[versionIdLabel]
        delResp = client.delete_object(Bucket=bucket, Key=obj, VersionId=version)
        print("Object {0} with version {1} from bucket {2} removed".format(obj, version, bucket))


    if nextVersionIdMarkerLabel not in response:
        print("No more versions to fetch. Exiting...")
        sys.exit(0)

    nextVersionIdMarker = response[nextVersionIdMarkerLabel]
```