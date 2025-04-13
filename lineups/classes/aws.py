import os
import json
import boto3
import discord
from classes.cache import Cache
from classes.enums import Map
from botocore.exceptions import ClientError


class AWS_Connection:
    def __init__(self, access_key, secret, region: str, service: str):
        self.client = boto3.client(
            service_name=service,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret,
            region_name=region
        )

        print(f'AWS Connection initialized with {service}...')


class DynamdDB_Client:
    def __init__(self, client, table: str):
        self.client = client
        self.table  = table

        try:
            client.describe_table(TableName=table)
            print('DynamoDb client initialized. . .')

        except ClientError as ce:
            if ce.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f'Table {table} does not exist. Create the table first and try again.')
            else:
                print(f'Unknown exception occurred while querying for the {table} table. Printing full error: {ce.response}')

    async def get_lineups(self, map_name: str, team: str, site: str):
        response = self.client.query(
            TableName=self.table,
            KeyConditionExpression='CS_Map = :pk_val',
            FilterExpression='Team = :team AND Site = :site',
            ExpressionAttributeValues={
                ':pk_val': {'S': map_name},
                ':team': {'S': team},
                ':site': {'S': site},
            }
        )

        return response

class S3_Client:
    def __init__(self, client, clip: str, cs_map: Map, location: str, nade_type: str):
        self.client = client
        self.clip  = clip
        self.cs_map = cs_map
        self.location = location
        self.nade_type = nade_type

        try:
            self.client.list_buckets()
            print("Boto3 S3 client is working correctly.")
        except Exception as e:
            print("Error: ", e)

        print('S3 client initialized. . .')

    async def download_clip(self, cache: Cache):
        clip_location = os.path.join(cache.parent_directory, self.cs_map.name.lower(), os.path.basename(self.clip))

        if (not cache.file_exists(clip_location)):
            print(f'Buffer NOT found for {clip_location}. Downloading from S3...')
            if not os.path.exists(os.path.dirname(clip_location)):
                os.makedirs(os.path.dirname(clip_location))

            self.client.download_file('lineup-clips', f'{self.cs_map.name.lower()}/{os.path.basename(self.clip)}', clip_location)
            cache.file_dict[clip_location] = {os.path.getatime(clip_location), os.path.getsize(clip_location)}
        else:
            print(f'Cached file found for {clip_location}. Using cache...')

        with open(clip_location, 'rb') as file:
            return discord.File(file, f'{'Smoke' if self.nade_type == 'Smoke' else 'Molly' if self.nade_type == 'Molotov' else 'Flash'}-for-{self.location}.gif')
