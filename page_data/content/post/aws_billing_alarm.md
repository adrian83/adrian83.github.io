---
title: "Cloudformation Stack with Billing Alarm"
date: 2019-05-13
draft: true
tags:
- aws
- cloudformation
- stack
- sns
- python
- boto 3
---

If you're starting your adventure with AWS and you'ar afraid that our bill will be too high you should do two things: create CloudWatch Alarm that will notify you if your bill reaches set limit and use Cloudformation Stacks to simplify managing your resources.
<!--more-->


#### Introduction

First steps in AWS can sometimes end with supprisingly high bill. Not everyone knows pricing of every created resource. Some AWS resources will cost you money just because they exist (Load Balancers). Other services can exist and will not increase your bill if not used and some are extremly cheap and will definitly not rouin you if you use them for education purposes.
Fortunately for us there is simple way we can be notified if your bill is growing too fast. It's called Alarm and it can send you an email or sms message. 

But Alert is only part of the solution. We also need a way to controll created resources. For that we will use service called Cloudformation. It will allow us to build infrastructure from files. Resources defined in such files will be bound in so called Stacks which in turn make managing resources easier.  

#### Infrastructure

As stated before infrastructure can be kept in text files (in JSON or YAML format). Below you can find almost everything which is needed for describing notification system to work. The only things that are missing are values for the parameters defined in the upper part of the template. Those values have to be provided while building our infrastructure.

```
AWSTemplateFormatVersion: 2010-09-09
Description: Billing Alarm to Monitor Your Estimated AWS Charges


Parameters:

  Email:
    Type: String
    Description: Email address on which alarm email will be sent
  Threshold:
    Type: Number
    Description: The amount of money over which the alarm will be sent


Resources:

  BillingAlarmSNSTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: billing_alarm_topic
      Subscription:
      - Endpoint: !Ref Email
        Protocol: email

  BillingAlarm:
    Type: AWS::CloudWatch::Alarm
    DependsOn: BillingAlarmSNSTopic
    Properties:
      AlarmName: AWS Billing Alarm
      AlarmDescription: Billing Alarm to Monitor My Estimated AWS Charges
      AlarmActions:
        - !Ref BillingAlarmSNSTopic
      Period: 86400               # 1 day - time in seconds (multiples of 60)
      ComparisonOperator: GreaterThanOrEqualToThreshold
      EvaluationPeriods: 1
      Threshold: !Ref Threshold
      Dimensions:
        - Name: currency
          Value: USD
      TreatMissingData: ignore
      Statistic: Maximum
      MetricName: EstimatedAWSCharges
      Namespace: AWS/Billing
```


#### Building infrastructure

Building infrastructure can be done in a multitude way. More complicated systems requires more spohisticated deployment tools but for our purposes the simplest solutions will do. We can use AWS CLI and write shell script, or use AWS SDK and use one of supported programming languages.

As a result all resources defined in Cloudformation template will be created as well as so called Stack. Stack can be defined as a bundle of all defined in template resources. Since now on all modification of those resources should be done in the template and applied by updating Stack. Removing all resouces will be easy because it can be achieved by removing stack. This way keeping our AWS account clean is much easier (and thus cheeper).

I've decided to use Python and AWS SDK called [Boto 3](https://wiki.python.org/TODO). Below you can find script that I use to create, update and delete the stack

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import io
import boto3
import sys

create_cmd = "create"
update_cmd = "update"
delete_cmd = "delete"

stack_name = 'EDU-BILLING-ALARM'
stack_tags = [{"Key": "project", "Value": "edu"}]


def to_param(item):
    return {"ParameterKey": item[0], "ParameterValue": str(item[1])}


def params():
    with open("parameters.yml", 'r') as params_file:
        params_dict = yaml.load(params_file)
        return [to_param(item) for item in params_dict.items()]
    raise ValueError("Couldn't read parameters")


def template():
    with open('cloudformation.yml', 'r') as cfn_template:
        return cfn_template.read()
    raise ValueError("Couldn't read template")


def create_stack(cf_client):
    cf_client.create_stack(
        StackName=stack_name,
        TemplateBody=template(),
        TimeoutInMinutes=10,
        OnFailure='DELETE',
        Parameters=params(),
        Tags=stack_tags
    )
    waiter = cf_client.get_waiter('stack_create_complete')
    waiter.wait(StackName=stack_name)
    print(cf_client.describe_stacks(StackName=stack_name))


def update_stack(cf_client):
    cf_client.update_stack(
        StackName=stack_name,
        TemplateBody=template(),
        Parameters=params(),
        Tags=stack_tags
    )
    waiter = cf_client.get_waiter('stack_update_complete')
    waiter.wait(StackName=stack_name)
    print(cf_client.describe_stacks(StackName=stack_name))


def delete_stack(cf_client):
    return cf_client.delete_stack(
        StackName=stack_name,
    )
    waiter = cf_client.get_waiter('stack_delete_complete')
    waiter.wait(StackName=stack_name)
    print(cf_client.describe_stacks(StackName=stack_name))


def print_menu():
    print("Usage: ./run.py <command>")
    print("possible commands:")
    print("\t{0} - creates cloudformation stack".format(create_cmd))
    print("\t{0} - updates existing stack".format(update_cmd))
    print("\t{0} - removes stack".format(delete_cmd))
    print("\tmenu - prints menu")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("provide command: '{0}', '{1}' or '{2}'".format(create_cmd,
              update_cmd, delete_cmd))
        exit(1)

    client = boto3.client('cloudformation')

    command = sys.argv[1].lower()
    if command == create_cmd:
        create_stack(client)
    elif command == update_cmd:
        update_stack(client)
    elif command == delete_cmd:
        delete_stack(client)
    else:
        print("\nunknown command: '{0}'\n".format(command))
        print_menu()
        print()
        exit(1)

    exit(0)
```

Cloudformation template and build script can be found [here](https://github.com/adrian83/aws-samples/tree/master/billing-alarm).

If you want to run the script please provide propper values in `parameters.yml` file. After that you can run `./run.sh create` to build the Cloudformation stack and `./run.sh update` to update it (if you change something in the template or any of the parameters) or `./run.sh delete` it if you don't need it.

When the stack will be build successfully you will receive an email by which you can 'Confirm subscription'. Only this way AWS will be able to sent you emails with alerts.


#### Summary

Building infrastructure is not an easy task. Keeping it as a code is a first and very importants step. Code presented above is just a very basic example of how you can create infrastructure in AWS. Beside that it will help you to keep your resouces and money under controll 



#### Sources
1. [Working with stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html)
2. [Using Amazon CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
3. [Boto 3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
