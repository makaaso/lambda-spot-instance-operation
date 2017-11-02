#!/usr/bin/env python
# -*- coding: utf-8 -*-

import botocore
import boto3
import datetime
import os

# Spot request Specification
#spot_price        = "0.030"
#instance_count    = 1
#request_type      = "one-time"
#image_id          = "ami-xxxxxxxx"
#security_groups   = ["sg-xxxxxxxx", "sg-yyyyyyyy"]
#incetance_type    = "m3.large"
#availability_zone = "ap-northeast-1c"
#subnet_id         = "subnet-xxxxxxxx"
#queue_name        = "sqs_name"

client            = boto3.client('ec2')
sqs               = boto3.resource('sqs')

def lambda_handler(event, context):

    print(os.environ['SPOT_PRICE'])
    print(os.environ['INSTANCE_COUNT'])
    print(os.environ['REQUEST_TYPE'])
    print(os.environ['IMAGE_ID'])
    print(os.environ['SECURITY_GROUPS'])
    print(os.environ['INSTANCE_TYPE'])
    print(os.environ['AVAILABILITY_ZONE'])
    print(os.environ['SUBNET_ID'])

    # Request Spot Instance
    response = client.request_spot_instances(
        SpotPrice            = os.environ['SPOT_PRICE'],
        InstanceCount        = int(os.environ['INSTANCE_COUNT']),
        Type                 = os.environ['REQUEST_TYPE'],
        LaunchSpecification  = {
            "ImageId"          : os.environ['IMAGE_ID'],
            "SecurityGroupIds" : os.environ['SECURITY_GROUPS'],
            "InstanceType"     : os.environ['INSTANCE_TYPE'],
            "Placement"        : {
                "AvailabilityZone" : os.environ['AVAILABILITY_ZONE']
            },
            "SubnetId"         : os.environ['SUBNET_ID']
        }
    )
 
    request_ids  =[]
    request_body = list(response['SpotInstanceRequests'])
    for request_id in request_body:
        request_ids.append(request_id['SpotInstanceRequestId'])
 
    # Send Request IDs to SQS
    queue        = sqs.get_queue_by_name(QueueName = queue_name)
    que_response = queue.send_message( MessageBody = ",".join(request_ids))
 
    return request_ids
