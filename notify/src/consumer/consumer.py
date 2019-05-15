#!/usr/bin/python3

import json
import requests
import boto3
import time
import os
from datetime import datetime

session = boto3.Session(
    aws_access_key_id=os.environ['ACCESS_KEY'],
    aws_secret_access_key=os.environ['SECRET_KEY']
)

dyn = session.client('dynamodb',region_name='us-east-1')
TBL_NAME = 'eks-traefik-notify'
TBL_KEY = 'recordSet'

URL_TRAEFIK = os.environ['HOST_TRAEFIK']
API_URI = "api"

def dynamodbPut(body,timestamp):
    response = dyn.put_item(
        TableName=TBL_NAME,
        Item={
            'recordSet': {
                'S': '%s'%(body)
                },
            'timestamp': {
                'S': '%s'%(timestamp)
            }
        }
    )
    #log.info(body)
    return response['ResponseMetadata']['RequestId']

def dynamodbScan():
    response = dyn.scan(
        TableName=TBL_NAME
    )
    recordsSet = []
    for n in response['Items']:
        recordsSet.append((n['recordSet']['S']))
    return recordsSet

def dynamodbDelete(item):
    response = dyn.delete_item(
    TableName=TBL_NAME,
        Key={
            TBL_KEY: {
                'S': '%s'%item
            }
        }
    )
    return response

while True:
    print(datetime.now())
    try:
        response = requests.get("%s/%s"%(URL_TRAEFIK,API_URI))
        rBody = json.loads(response.content)

        recordsSetDyn = dynamodbScan()
        recordsSetTra = []
        for n in rBody['kubernetes']['frontends']:
            recordSet = n.replace('/','')
            recordsSetTra.append(recordSet)
            if recordSet not in recordsSetDyn:
                print('Gravando novo RecordSet: %s'%(recordSet))
                dynamodbPut(recordSet,str(datetime.timestamp(datetime.now())).split('.')[0])
        print("[INFO] Frontend encontrado:")
        for recordSet in recordsSetDyn:
            print(recordSet)
            if recordSet not in recordsSetTra:
                print('Apagando RecordSet: %s'%(recordSet))
                dynamodbDelete(recordSet)
        print()
    except Exception as error:
        print('Erro na execucao:')
        print(error)
        print()
    time.sleep(5)
