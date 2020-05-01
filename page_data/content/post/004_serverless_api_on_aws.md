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

### Writing serverless applications on AWS can be really easy. Below you can find description of how to build simplified CRUD application for user management.

The full source code with instructions, how to run and test it, can be found [here](https://github.com/adrian83/aws-samples/tree/master/004-serverless-api-demo).

### Infrastructure as a Code

Defining Serverless applications in CloudFormation became a bit simpler since AWS realised set of resources under `AWS::Serverless::*` namespace. In fact code presented in this post is defined in single yaml file. Both infrastructure (database, security roles, lambda functions and API gateway) and logic (code executed by lambda functions) is defined in CloudFormation. Most of resources from that namespace have equivalent in standard CloudFormation resources. For example, used in this post, `AWS::Serverless::Function` is just `AWS::Lambda::Function` with some improvements, or also used `AWS::Serverless::Api` which simplifies creation of API Gateways (by creating `AWS::ApiGateway::RestApi` and few other resources from `AWS::ApiGateway::*` resource). Of course as usually is such situations using resources from `AWS::Serverless::*` allows you to build infrastructure quicker and on the other hand using standard CloudFormation resources gives you more configuration options.

### Database

Since we are building serverless application, it is important to choose proper Database. We definitely need database, that will scale regarding the traffic, and also we don't want to manage any server. DynamoDB fulfills both of thoses requirements, and thus it makes perfect sense to use it.

Lets look at the definition of DynamoDB table:

```
  UsersDynamoDBTable:
    Type: 'AWS::DynamoDB::Table'
    Properties:
      TableName: 'users'
      BillingMode: 'PAY_PER_REQUEST'
      AttributeDefinitions:
        - AttributeName: 'id'
          AttributeType: 'S'
      KeySchema:
        - AttributeName: 'id'
          KeyType: 'HASH'
```

There are basically three important information in this definition: 

- name of the table 
- billing mode (we will pay only for what we use)
- key definition (every element in `KeySchema` needs to be defined in `AttributeDefinitions`)


### Functions

Writing lambda code can be done in almost any programming language thanks to possibility of defining [Custom AWS Lambda Runtimes](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-custom.html). However if you want to interact with other AWS services, it’s much easer to write code in language, that have [official AWS SDK](https://aws.amazon.com/tools/).

If the code executed by Lambda will be rather short, you can decide to inline it inside your CloudFormation script. 

Let's look at sample lambda definitions:

```
CreateUserLambda:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: 'user-create'
      Handler: index.lambda_handler
      Runtime: python3.6
      Timeout: 25
      MemorySize: 128
      Policies:
      - DynamoDBCrudPolicy:
          TableName: !Ref UsersDynamoDBTable
      Environment:
        Variables:
          USERS_TABLE_NAME: !Ref UsersDynamoDBTable
      Events:
        Api:
          Type: Api
          Properties:
            Method: post
            Path: /v1/users
            RestApiId: 
              Ref: UserAPIGateway
      InlineCode: |
          from __future__ import print_function
          import boto3
          import json
          import os
          import uuid

          users_table = os.environ['USERS_TABLE_NAME']

          dynamodb_client = boto3.client('dynamodb')

          def lambda_handler(event, context):
            print("event: {0}".format(event))

            body = json.loads(event['body'])
            if 'firstName' not in body or 'lastName' not in body:
              print("cannot persist user, invalid data: {0}".format(body))
              return {"statusCode": 400, "body": "Invalid input"}

            user_id = str(uuid.uuid4())
            first_name = body['firstName']
            last_name = body['lastName']

            response = dynamodb_client.put_item(
              TableName=users_table, 
              Item={'id': {'S': user_id}, 'firstName': {'S': first_name}, 'lastName': {'S': last_name}})

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
              print("cannot put item: {0}".format(response))
              return {"statusCode": 500, "body": "Internal server error: {0}".format(response)}

            return {"statusCode": 201, "body": json.dumps({'id': user_id, 'firstName': first_name, 'lastName': last_name})}


  DeleteUserLambda:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: 'user-delete'
      Handler: index.lambda_handler
      Runtime: python3.6
      Timeout: 25
      MemorySize: 128
      Policies:
      - DynamoDBCrudPolicy:
          TableName: !Ref UsersDynamoDBTable
      Environment:
        Variables:
          USERS_TABLE_NAME: !Ref UsersDynamoDBTable
      Events:
        Api:
          Type: Api
          Properties:
            Method: delete
            Path: /v1/users/{userId}
            RestApiId: 
              Ref: UserAPIGateway
      InlineCode: |
          from __future__ import print_function
          import boto3
          import os

          users_table = os.environ['USERS_TABLE_NAME']

          dynamodb_client = boto3.client('dynamodb')

          def lambda_handler(event, context):
            print("event: {0}".format(event))

            user_id = event['pathParameters']['userId']

            response = dynamodb_client.delete_item(
              TableName=users_table, 
              Key={'id': {'S': user_id}})

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
              print("cannot delete item: {0}".format(response))
              return {"statusCode": 500, "body": "Internal server error: {0}".format(response)}

            return {"statusCode": 200}
```

Let's take a look at few most important properties:

- `FunctionName` - name of the Lambda function
- `Handler` - name of the function (in source code), that will be called when Lambda will be executed
- `Runtime` - defines runtime of the Lambda (programming language and it's version)
- `Timeout` - max duration of the Lambda (in seconds)
- `MemorySize` - describes, how powerfull will be the hardware (not only memory but also CPU), running your function
- `Policies` - describe security policies, in this cases functions can execute CRUD operations on created previously DynamoDB table
- `Environment.Variables` - defines variables, that can be assigned in CloudFormation and used in code
- `Events` - events that will trigger this lambda, in these cases they are events from API Gateway 
- `InlineCode` - code of the Lambda function

### API Gateway

Exposing API to the world can be done through API Gateway service.

Basic definition of API Gateway looks like this:

```
  UserAPIGateway:
    Type: AWS::Serverless::Api
    Properties:
      Name: 'users-api-gateway'
      StageName: 'api-demo'
```

### Summary

As you can see knowing three types of Cloudformation resources is enough to create simple CRUD application. Thanks to resources from `AWS::Serverless::*` we dont have to define a few resources. For example:
1. Defining `Policies` in `AWS::Serverless::Function` frees us from defining IAM Role (`AWS::IAM::Role`) 
2. Defining `Events.Api` in `AWS::Serverless::Function` frees us from defining integration on API Gateway as well as permission for API Gateway (`AWS::Lambda::Permission`)
3. Defining `StageName` in `AWS::Serverless::Api` frees us from defining `AWS::ApiGateway::Stage` 

