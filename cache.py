import os


def file_exists(clip_location):
    return os.path.exists(clip_location)


def check_size(directory = 'clips'):
    total_size = 0
    start_path = directory
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    
    return total_size / 1024 / 1024

def evict(size):
    cache_files = list_files_by_access_date('clips')

    for file_path, access_time in cache_files:
        print(f'Size: {check_size('clips')} - Max Size: {size}')
        if check_size('clips') < size:
            print(f'Cache size lower than {size} MB')
            return
        
        os.remove(file_path)
        print(f'File removed: {file_path} - {access_time}')


def list_files_by_access_date(path: str):
    files = []
    for dir_path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            
            filepath = os.path.join(dir_path, file_name)
            if os.path.isfile(filepath):
                files.append((filepath, os.path.getatime(filepath)))

    # Sort files by access time in descending order (most recent first)
    files.sort(key=lambda x: x[1], reverse=False)

    return files
