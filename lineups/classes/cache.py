import os

class Cache:
    def __init__(self, p = ''):
        self._parent_directory = p

        if self._parent_directory is not None and len(self._parent_directory) > 0:
            print(f'file_dict: {self.file_dict}')
            print(f'size: {self.size}')

    @property
    def parent_directory(self):
        return self._parent_directory
    
    @parent_directory.setter
    def parent_directory(self, directory):
        self._parent_directory = directory

    @property
    def file_dict(self):
        file_dict = {}
        for dir_path, dir_names, file_names in os.walk(self.parent_directory):
            for file_name in file_names:           
                filepath = os.path.join(dir_path, file_name)
                if os.path.isfile(filepath):
                    file_dict[filepath] = (os.path.getatime(filepath), os.path.getsize(filepath))

        file_dict = sorted(file_dict.items(), key=lambda x: x[1])

        self._file_dict = dict((file_path, values) for file_path, values in file_dict)
        return self._file_dict

    @file_dict.setter
    def file_dict(self, file_dict):
        self._file_dict = file_dict

    @property
    def size(self):
        self._size = 0
        for dirpath, dirnames, filenames in os.walk(self.parent_directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                self._size += (os.path.getsize(fp) / 1024 / 1024)
        
        return self._size

    @size.setter
    def size(self, size):  
        self._size = size

    def file_exists(self, clip_location):
        return os.path.exists(clip_location)

    async def evict(self, max_size):
        if self.size > max_size:
            updated_file_dict = dict(self.file_dict)
            for file_path, values in self.file_dict.items():
                print(f'Size: {self.size} MB - Max Size: {max_size} MB')
                if self.size < max_size:
                    print(f'Cache size lower than {max_size} MB')
                    return

                os.remove(file_path)
                updated_file_dict.pop(file_path)
                print(f'File removed: {file_path}')                
            
            self.file_dict = updated_file_dict