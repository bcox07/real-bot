import os

PARENT_DIRECTORY = 'clips'

def file_exists(clip_location):
    return os.path.exists(clip_location)


def check_size():
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(PARENT_DIRECTORY):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    
    return total_size / 1024 / 1024

async def evict(max_size):
    cache_files = list_files_by_access_date()

    for file_path, access_time in cache_files:
        size_utilized = check_size()
        print(f'Size: {size_utilized} MB - Max Size: {max_size} MB')
        if size_utilized < max_size:
            print(f'Cache size lower than {max_size} MB')
            return
        
        os.remove(file_path)
        print(f'File removed: {file_path} - {access_time}')


def list_files_by_access_date():
    files = []
    for dir_path, dir_names, file_names in os.walk(PARENT_DIRECTORY):
        for file_name in file_names:           
            filepath = os.path.join(dir_path, file_name)
            if os.path.isfile(filepath):
                files.append((filepath, os.path.getatime(filepath)))

    # Sort files by access time in ascending order
    files.sort(key=lambda x: x[1], reverse=False)

    return files
