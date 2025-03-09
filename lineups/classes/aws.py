import os
import json
import boto3
import discord
from classes.cache import Cache
from classes.enums import Map
from botocore.exceptions import ClientError

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

try:
    response = client.list_buckets()
    print("Boto3 S3 client is working correctly.")
except Exception as e:
    print("Error: ", e)

class AWS_Connection:
    def __init__(self, clip: str, cs_map: Map, location: str, nade_type: str):
        self.clip  = clip
        self.cs_map = cs_map
        self.location = location
        self.nade_type = nade_type
        print('AWS_Connection initialized. . .')

    @staticmethod
    def get_secret():

        secret_name = "discord"
        region_name = "us-east-2"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        secret = json.loads(get_secret_value_response['SecretString'])

        return secret

    async def download_clip(self, cache: Cache):
        clip_location = os.path.join(cache.parent_directory, self.cs_map.name.lower(), self.clip)

        if (not cache.file_exists(clip_location)):
            print(f'Buffer NOT found for {clip_location}. Downloading from S3...')
            if not os.path.exists(os.path.dirname(clip_location)):
                os.makedirs(os.path.dirname(clip_location))

            client.download_file('lineup-clips', f'{self.cs_map.name.lower()}/{self.clip}', clip_location)
            cache.file_dict[clip_location] = {os.path.getatime(clip_location), os.path.getsize(clip_location)}
        else:
            print(f'Cached file found for {clip_location}. Using cache...')

        with open(clip_location, 'rb') as file:
            return discord.File(file, f'{'Smoke' if self.nade_type == 'Smokes' else 'Molly' if self.nade_type == 'Mollies' else 'Flash'}-for-{self.location}.gif')
