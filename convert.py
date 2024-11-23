from moviepy import VideoFileClip
import os

from pathlib import Path

parentDirectoryString = './clips/ancient'

directory = os.fsencode(parentDirectoryString)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filenameWithoutExtension = Path(filename).stem
    
    if filename.endswith(".mp4"): 
        fileLocation = os.path.join(parentDirectoryString, filename)
        gifLocation = os.path.join(parentDirectoryString, f'{filenameWithoutExtension}.gif')

        videoClip = VideoFileClip(fileLocation).resized(0.4)
        videoClip.write_gif(gifLocation, fps=15)
        continue