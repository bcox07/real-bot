import subprocess
from moviepy import VideoFileClip

fileLocation = './clips/anubis-a-molly.mp4'
gifLocation = './clips/anubis-a-molly.gif'

videoClip = VideoFileClip(fileLocation).resized(0.4)

videoClip.write_gif(gifLocation, fps=15)
