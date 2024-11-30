import boto3
import discord
import os

s3 = boto3.client('s3')


def cached_file_exists(clip_location):
    print(f'Cached file exists for {clip_location}: {os.path.exists(clip_location)}')

    return os.path.exists(clip_location)


async def download_clip(clip, map, location, nade_type):

    clip_location = f'clips/{map.lower()}/{clip}'

    if (cached_file_exists(clip_location) is not True):
        print(f'Buffer NOT found for {clip_location}. Downloading from S3...')
        s3.download_file('lineup-clips', f'{map.lower()}/{clip}', clip_location)
    else:
        print(f'Cached file found for {clip_location}. Using cache...')
    
    with open(clip_location, 'rb') as file:
        return discord.File(file, f'{'Smoke' if nade_type == 'Smokes' else 'Molly' if nade_type == 'Mollies' else 'Flash'}-for-{location}.gif')