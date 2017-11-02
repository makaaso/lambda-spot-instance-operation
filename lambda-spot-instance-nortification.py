#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import boto3
 
sqs         = boto3.resource('sqs')
queue_name  = "mj2-ope-sqs"
queue       = sqs.get_queue_by_name(QueueName = queue_name)
 
spot_client = boto3.client('ec2')
sns         = boto3.client('sns')
 
def lambda_handler(event, context):
 
    #Receive Spot Request IDs from SQS
     
    entries     = []
    messages    = queue.receive_messages()
    entries.append({
        "Id"            : messages[0].message_id,
        "ReceiptHandle" : messages[0].receipt_handle
    })
    receive_msg   = messages[0].body
    request_ids   = receive_msg.split(",")
 
    if len(entries) != 0:
        response  = queue.delete_messages(Entries = entries)
 
    spot_response = spot_client.describe_spot_instance_requests(
        SpotInstanceRequestIds = request_ids
    )
 
    print(spot_response)
    instance_ids  = []
    err_message   = []
    spot_request  = list(spot_response['SpotInstanceRequests'])
 
    for result in spot_request:
        if 'InstanceId' in result:
            instance_ids.append(result['InstanceId'])
        else:
            request_status = result['Status']
            err_message.append({result['SpotInstanceRequestId']:request_status['Message']})
 
    # Send Result to SNS
     
    if len(instance_ids) != 0:
        request = {
            'TopicArn' : "arn:aws:sns:ap-northeast-1:360078877034:mj2-ope-sns",
            'Message'  : str(instance_ids),
            'Subject'  : "Spot request is fulfilled"
        }
        response = boto3.client('sns').publish(**request)
 
    if len(err_message) != 0:
        request = {
            'TopicArn' : "arn:aws:sns:ap-northeast-1:360078877034:mj2-ope-sns",
            'Message'  : str(err_message),
            'Subject'  : "Spot request is Not fulfilled"
        }
        response = boto3.client('sns').publish(**request)
