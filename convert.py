import os

from moviepy import VideoFileClip
from pygifsicle import gifsicle

from pathlib import Path

parentDirectoryString = './clips/vertigo'

directory = os.fsencode(parentDirectoryString)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filenameWithoutExtension = Path(filename).stem
    
    if filename.endswith(".mp4"): 
        fileLocation = os.path.join(parentDirectoryString, filename)
        gifLocation = os.path.join(parentDirectoryString, f'{filenameWithoutExtension}.gif')

        videoClip = VideoFileClip(fileLocation).resized(0.4)
        videoClip.write_gif(gifLocation, fps=15)

        if os.path.getsize(gifLocation) > 15000000:
            print(f'File size greater than 15 MB, optimizing: {gifLocation} - Actual size: {os.path.getsize(gifLocation) / 1000000} MB')
            gifsicle(sources=[f"{gifLocation}"], optimize=True, options=["--verbose", "--lossy=95"]) # Options to use.
        continue