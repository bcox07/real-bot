import os

from moviepy import VideoFileClip
from pygifsicle import gifsicle

from pathlib import Path

parentDirectoryString = './clips/anubis'

directory = os.fsencode(parentDirectoryString)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filenameWithoutExtension = Path(filename).stem
    
    if filename.endswith(".mp4"): 
        fileLocation = os.path.join(parentDirectoryString, filename)
        gifLocation = os.path.join(parentDirectoryString, f'{filenameWithoutExtension}.gif')

        videoClip = VideoFileClip(fileLocation).resized(0.4)
        videoClip.write_gif(gifLocation, fps=15)

        gifsicle(sources=[f"{gifLocation}"], optimize=False, options=["--verbose", "--lossy=80"]) # Options to use.
        continue