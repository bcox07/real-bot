import os
import boto3
import discord
from classes.cache import Cache
from classes.enums import Map

s3 = boto3.client('s3')

class AWS_Connection:
    def __init__(self, clip: str, cs_map: Map, location: str, nade_type: str):
        self.clip  = clip
        self.cs_map = cs_map
        self.location = location
        self.nade_type = nade_type
        print('AWS_Connection initialized. . .')

    async def download_clip(self, cache: Cache):
        clip_location = os.path.join(cache.parent_directory, self.cs_map.name.lower(), self.clip)

        if (not cache.file_exists(clip_location)):
            print(f'Buffer NOT found for {clip_location}. Downloading from S3...')
            if not os.path.exists(os.path.dirname(clip_location)):
                os.makedirs(os.path.dirname(clip_location))

            s3.download_file('lineup-clips', f'{self.cs_map.name.lower()}/{self.clip}', clip_location)
            cache.file_dict[clip_location] = {os.path.getatime(clip_location), os.path.getsize(clip_location)}
        else:
            print(f'Cached file found for {clip_location}. Using cache...')

        with open(clip_location, 'rb') as file:
            return discord.File(file, f'{'Smoke' if self.nade_type == 'Smokes' else 'Molly' if self.nade_type == 'Mollies' else 'Flash'}-for-{self.location}.gif')