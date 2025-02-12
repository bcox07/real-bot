import os
import boto3
import discord
from classes.cache import Cache

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


async def download_clip(cache: Cache, clip, map, location, nade_type):
    clip_location = os.path.join(cache.parent_directory, map.lower(), clip)

    
    if (cache.file_dict.get(clip_location, 'none') == 'none'):
        print(f'Cached file NOT found for {clip_location}. Downloading from S3...')
        if not os.path.exists(os.path.dirname(clip_location)):
            os.makedirs(os.path.dirname(clip_location))

        client.download_file('lineup-clips', f'{map.lower()}/{clip}', clip_location)
        cache.file_dict[clip_location] = {os.path.getatime(clip_location), os.path.getsize(clip_location)}
    else:
        print(f'Cached file found for {clip_location}. Using cache...')
    
    with open(clip_location, 'rb') as file:
        return discord.File(file, f'{'Smoke' if nade_type == 'Smokes' else 'Molly' if nade_type == 'Mollies' else 'Flash'}-for-{location}.gif')