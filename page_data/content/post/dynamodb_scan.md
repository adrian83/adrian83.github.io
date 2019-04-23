---
title: "Scan through all items in DynamoDB table"
date: 2019-01-13
draft: true
tags:
- dynamodb
- aws
- python
- generator
thumbnailImagePosition: left
thumbnailImage: https://upload.wikimedia.org/wikipedia/commons/f/fd/DynamoDB.png
---

When working with AWS DynamoDB I sometimes have to modify each document in table. Most of the times executing update statement is just not enough and i have to programmatically access each document and modify it.
<!--more-->


Getting documents can be achieved by executing `scan` operation on table. Each execution of `scan` method will return max 1MB of data so for most tables multiple calls are needed.

Python script presented below simplifies iterating through given DynamoDB table. We can basically treat DynamoDB table as a Python sequence. What is worth noting is that every next part of the sequence is fetched lazyly that is after all previous elements were processed. This lazines decreases probability of working with stale data.

```
import boto3

lastEvalKeyLabel = "LastEvaluatedKey"
itemsLabel = "Items"

dynamoDB = "dynamodb"
region = "eu-west-1"

tableName = "USERS-DEV"

def scan_all(table):

    lastEvaluatedKey = None

    while True:

        scanResp = table.scan() if not lastEvaluatedKey \
            else table.scan(ExclusiveStartKey=lastEvaluatedKey)

        items = scanResp[itemsLabel]
        if not items:
            print("No more items to process")
            break

        print("Scan fetched {0} items".format(len(items)))

        for item in items:
            yield item

        if lastEvalKeyLabel in scanResp:
            lastEvaluatedKey = scanResp[lastEvalKeyLabel]
        else:
            print("No more items to process")
            break

    print("End of scanning")


if __name__ == "__main__":

    dynamoDB = boto3.resource(dynamoDB, region_name=region)
    table = dynamoDB.Table(tableName)

    count = 0
    for item in scan_all(table):
        # processing items goes here
        count += 1

    print("Items processed: {0}".format(count))


```

When we execute this script we should see something like this:

```
[adrian@adrian-pc decorators]$ python table_scan.py
Scan fetched 5386 items
Scan fetched 4508 items
No more items to process
End of scanning
Items processed: 9894
```


If we take a look at table summary (in AWS web console) we'll see that it matches logs above.


```
Last increase time    ...
Storage size (in bytes) 1.85 MB
Item count  9,894
Region  EU West (Ireland)
Amazon Resource Name (ARN)  arn:aws:dynamodb:eu-west-1:...
```



#### Sources
1. [Python Generators](https://wiki.python.org/moin/Generators)
2. [DynamoDB Scan](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html)