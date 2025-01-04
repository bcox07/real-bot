import os

class Cache:
    def __init__(self):
        self.parent_directory = './clips'
        self.get_file_dict()
        self.get_size()

        print('Cache class initialized. . .')

    def get_file_dict(self):
        file_dict = {}
        for dir_path, dir_names, file_names in os.walk(self.parent_directory):
            for file_name in file_names:           
                filepath = os.path.join(dir_path, file_name)
                if os.path.isfile(filepath):
                    file_dict[filepath] = {os.path.getatime(filepath), os.path.getsize(filepath)}

        file_dict = sorted(file_dict.items(), key=lambda x: x[1])
        for file, value in file_dict:
            print(f'{file} - {value}')

        print(f'get_file_dict set: {len(file_dict)}')
        self.file_dict = dict((file_path, values) for file_path, values in file_dict)

    def file_exists(self, clip_location: str):
        return self.file_dict.get(clip_location, 'none') != 'none'

    def get_size(self):
        size = 0
        for dirpath, dirnames, filenames in os.walk(self.parent_directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                size += (os.path.getsize(fp) / 1024 / 1024)
        
        print(f'get_size set: {size}')
        self.size = size

    async def evict(self, max_size):
        if self.size > max_size:
            updated_file_dict = dict((f, a) for f, a in self.file_dict.items())
            for file_path, values in self.file_dict.items():
                print(f'Size: {self.size} MB - Max Size: {max_size} MB')
                if self.size < max_size:
                    print(f'Cache size lower than {max_size} MB')
                    return

                os.remove(file_path)
                updated_file_dict.pop(file_path)
                print(f'File removed: {file_path} - {values}')                
                self.get_size()
            
            self.file_dict = updated_file_dict