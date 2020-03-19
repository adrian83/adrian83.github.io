---
title: Building Serverless API on AWS
date: 2020-03-15
draft: true
categories:
- aws
- python
- lambda
- dynamodb
- api gateway
- cloudformation
- serverless
tags:
- aws
- python
- lambda
- dynamodb
- api gateway
- cloudformation
- serverless
---


What is serverless

Simple serverless stack on AWS

Cloudformation

DynanoDB + IAM role 

API Gateway + Permission

Lambdas 

Inline python code

Writing lambda code can be done in almost any programming language thanks to [](), but if you want to interact with other AWS services it's much easer writing code in one of languages that have official AWS SDK.

If code executed by lambda will be rather short you can decide to inline it inside your cloudformation script. 

Let's look at two such lambdas:

#### 1. 

```
  CreateUserLambda:
    Type: "AWS::Lambda::Function"
    Properties:
      FunctionName: !Sub 'user-create-${Env}'
      Role: !GetAtt UserLambdaRole.Arn 
      Handler: index.lambda_handler
      Runtime: python3.6
      Environment:
        Variables:
          USERS_TABLE_NAME: !Ref UsersDynamoDBTable
      Code:
        ZipFile: |
          from __future__ import print_function
          import boto3
          import json
          import os
          import uuid
          def lambda_handler(event, context):
            print(str(event))
            users_table = os.environ['USERS_TABLE_NAME']
            body = json.loads(event['body'])
            if 'firstName' not in body or 'lastName' not in body:
              print("invalid data: " + str(body))
              return {"statusCode": 400, "body": "Invalid input"}
            userId = str(uuid.uuid4())
            dynamodb_client = boto3.client('dynamodb')
            response = dynamodb_client.put_item(
              TableName=users_table, 
              Item={'id':{'S':userId}, 'firstName':{'S':body['firstName']}, 'lastName':{'S':body['lastName']}})
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
              print("cannot store data: " + str(response))
              return {"statusCode": 500, "body": "Internal server error:" + str(response)}
            return {"statusCode": 201, "body": json.dumps({'id':userId, 'firstName':body['firstName'], 'lastName':body['lastName']})}
```