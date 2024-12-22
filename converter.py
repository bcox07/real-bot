"""Module providing functionality to convert MP4 video files to compressed GIF files"""
import os
import sys

from pathlib import Path
from moviepy import VideoFileClip
from pygifsicle import gifsicle

class Converter():
    """Class for converting MP4 files to compressed GIF files"""
    def __init__(self, directory):
        self.directory = directory

    def validate_directory(self):
        """Validate directory exists"""
        if not os.path.isdir(self.directory):
            print(f'Directory: {self.directory} does not exist')
            return False
        print(f'Directory validated: {self.directory}')
        return True

    def convert_files(self):
        """Convert files in directory to a copy of GIF files"""
        encoded_directory = os.fsencode(self.directory)
        conversion_count = 0
        for file in os.listdir(encoded_directory):
            filename = os.fsdecode(file)
            filename_without_extension = Path(filename).stem

            if filename.endswith(".mp4"):         
                file_location = os.path.join(self.directory, filename)
                gif_location = os.path.join(self.directory, f'{filename_without_extension}.gif')
                print(f'Converting {file_location} to {gif_location}')

                video_clip = VideoFileClip(file_location).resized(0.4)
                video_clip.write_gif(gif_location, fps=15)

                if os.path.getsize(gif_location) > 15000000:
                    print(f'File size greater than 15 MB, optimizing: {gif_location} - Actual size: {os.path.getsize(gif_location) / 1000000} MB')
                    gifsicle(sources=[f"{gif_location}"], optimize=True, options=["--verbose", "--lossy=95"]) # Options to use.

                conversion_count += 1
                continue

        if conversion_count == 0:
            print('No files in directory or no files valid for conversion')

converter = Converter(sys.argv[1])

if converter.directory is None:
    print('No directory was provided')
    sys.exit(1)

if not converter.validate_directory():
    print('Invalid directory')
    sys.exit(1)

converter.convert_files()
