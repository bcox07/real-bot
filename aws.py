import boto3
import discord
import os

s3 = boto3.client('s3')


def buffer_exists(buffer_clip_location):
    print(f'Buffer file exists: {os.path.exists(buffer_clip_location)}')
    print('Omitting downloading from S3...')

    return os.path.exists(buffer_clip_location)


async def download_clip(clip, map, location, nade_type, interaction: discord.Interaction):

    buffer_clip_location = f'clips/{map.lower()}/{clip}'

    if (buffer_exists(buffer_clip_location) is not True):
        print('Buffer not found. Downloading from S3...')
        s3.download_file('lineup-clips', f'{map.lower()}/{clip}', buffer_clip_location)
    
    with open(buffer_clip_location, 'rb') as file:
        await interaction.followup.send(content=f'{'Smoke' if nade_type == 'Smokes' else 'Molly' if nade_type == 'Mollies' else 'Flash'} for {location}', file=discord.File(file, 'file.gif'), delete_after=600)