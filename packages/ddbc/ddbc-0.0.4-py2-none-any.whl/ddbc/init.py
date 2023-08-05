# -*- coding: utf-8 -*-

import boto3


def create_table(table_name, region=None, read_units=5, write_units=5):
    dynamodb = boto3.resource('dynamodb', region)
    table = dynamodb.Table(table_name)

    try:
        table.creation_date_time
    except botocore.exceptions.ClientError as e:

        if e.response['ResponseMetadata']['Code'] == 'ResourceNotFoundException':
            dynamodb.create_table(
                TableName=self.table.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'key',
                        'KeyType': 'HASH'
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'data',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'until',
                        'AttributeType': 'N'
                    },

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': read_units,
                    'WriteCapacityUnits': write_units
                }
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
