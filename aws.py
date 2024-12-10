import os
import boto3
import discord
import cache

s3 = boto3.client('s3')


async def download_clip(clip, map, location, nade_type):
    clip_location = os.path.join(cache.PARENT_DIRECTORY, map.lower(), clip)

    if (not cache.file_exists(clip_location)):
        print(f'Buffer NOT found for {clip_location}. Downloading from S3...')
        if not os.path.exists(os.path.dirname(clip_location)):
            os.makedirs(os.path.dirname(clip_location))

        s3.download_file('lineup-clips', f'{map.lower()}/{clip}', clip_location)
    else:
        print(f'Cached file found for {clip_location}. Using cache...')
    
    with open(clip_location, 'rb') as file:
        return discord.File(file, f'{'Smoke' if nade_type == 'Smokes' else 'Molly' if nade_type == 'Mollies' else 'Flash'}-for-{location}.gif')