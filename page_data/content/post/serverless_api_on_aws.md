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

The full source code with instructions how to run and test it can be found [here](https://github.com/adrian83/aws-samples/tree/master/004-serverless-api-demo).

### Database

Since we are building serverless application we need to choose database which we won't hve to manage. One of such services in AWS Cloud is DynamoDB and this service I will use. 

Lets look at the definition of DynamoDB table:

```
  UsersDynamoDBTable:
    Type: 'AWS::DynamoDB::Table'
    Properties:
      TableName: !Sub 'users-${Env}'
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
- billing mode (i want to pay only for what i use)
- key definition (every element in KeySchema needs to be defined in AttributeDefinitions)

### Permissions

Before we go to the Lambda Functions lets look at permissions we need to add to those functions so that they can access DynamoDB table defined above.

```
  UserLambdaRole:
    DependsOn: UsersDynamoDBTable
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Effect: Allow
            Action:
            - 'sts:AssumeRole'
            Principal:
              Service:
              - 'lambda.amazonaws.com'
      Policies:
        - PolicyName: 'users-dynamodb-policy'
          PolicyDocument:
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:*
                Resource:
                    - !GetAtt UsersDynamoDBTable.Arn 
        - PolicyName: 'users-logs-policy'
          PolicyDocument:
            Statement:
              - Effect: Allow
                Action:
                  - logs:*
                Resource:
                  - "arn:aws:logs:*:*:*"
```

This resource contains information about: 

- what kind of service ('lambda.amazonaws.com') can use this Role
- policies which are bound to this role:
  - first allows to executing every operation on DynamoDB table defined previously   
  - second allows to write logs into CloudWatch service  

### Functions

Writing lambda code can be done in almost any programming language thanks to [](), but if you want to interact with other AWS services it's much easer writing code in one of languages that have official AWS SDK.

If code executed by lambda will be rather short you can decide to inline it inside your CloudFormation script. 

Let's look at sample lambda definition:

```
  CreateUserLambda:
    Type: "AWS::Lambda::Function"
    Properties:
      FunctionName: !Sub 'user-create-${Env}'
      Role: !GetAtt UserLambdaRole.Arn 
      Handler: index.lambda_handler
      Runtime: python3.6
      Timeout: 25
      MemorySize: 128
      Environment:
        Variables:
          USERS_TABLE_NAME: !Ref UsersDynamoDBTable
      Code:
        ZipFile: |
          from __future__ import print_function  # 1
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

Let's take a look at properties tahat we have to define for all our lambda functions:

- 'FunctionName' name of the function
- 'Role' permissions for the lambda function
- 'Handler' name of the funcion () that will be called when LAmbda will be executed
- 'Runtime' defines programming language and it's version in which lambda is written
- 'Timeout' max duration of the lambda in seconds
- 'MemorySize' describes how powerfull will be the hardware (not only memory but also cpu) that will host your function
- 'Environment.Variables' variables that can be defined in CloudFormation and used in code
- 'Code.ZipFile' code of our lambda function

### Endpoints

Service in AWS that allows you to create API is called API Gateway. 


Curently you can create Gateways in two ways: 

- by using resource with type AWS::ApiGateway::RestApi (and few others from AWS::ApiGateway::* namespace) which gives you way to configure everything 
- by using resource with type AWS::Serverless::Api which simplifies API Gateway creation to single resource

Integrating Lambdas with API gateway is quite easy and it looks something like this

```
  UserAPIGateway:
    Type: AWS::Serverless::Api
    Properties:
      Name: !Sub 'users-api-gateway-${Env}'
      StageName: !Ref Env
      MethodSettings:
        - HttpMethod: '*'
          MetricsEnabled: true
          ResourcePath: '/*'
      DefinitionBody:
        swagger: "2.0"
        info:
          version: "2018-06-04T13:58:30Z"
          title:
            Ref: AWS::StackName
        paths:
          /v1/users:
            post:
              x-amazon-apigateway-integration:
                httpMethod: "POST"
                type: "aws_proxy"
                uri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${CreateUserLambda.Arn}/invocations'
          /v1/users/{userId}:
            delete:
              parameters:
              - name: userId
                in: path
                required: true
                type: string
              x-amazon-apigateway-integration:
                httpMethod: "POST"
                type: "aws_proxy"
                uri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${DeleteUserLambda.Arn}/invocations'
```

The most important part of this definition is the DefinitionBody which comply with Swagger (Open API) version 2.0.
As you can see every path and method pair is integrated with lambda function. Please be aware that every such integration is done through POST method (httpMethod: "POST").

### Permissions

Each lamba runs with it's IAM Role in which we defined that it can use DynamoDB and CloudWatch (for logging) but there is no permission for Api Gateway. This short snippet below will make executing lambdas from API Gateway possible.


```
  CreateUserLambdaApiGatewayPermission:
    DependsOn: [CreateUserLambda, UserAPIGateway]
    Type: AWS::Lambda::Permission
    Properties:
      Action: lambda:invokeFunction
      FunctionName: !GetAtt CreateUserLambda.Arn
      Principal: apigateway.amazonaws.com
      SourceArn: !Sub 'arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:${UserAPIGateway}/*'
```