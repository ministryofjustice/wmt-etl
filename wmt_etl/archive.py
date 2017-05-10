'''Module to compress and archive processed extract files'''
import os
import time
import gzip
import shutil
import errno
import wmt_etl.etl_config as config

def archive_files(file_paths):
    '''Add all region files to a single compressed archive'''
    archive_name = get_archive_file_path()
    create_data_directories()
    for file_name in file_paths:
        with open(file_name, 'rb') as file_in, gzip.open(archive_name, 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)

def create_data_directories():
    '''Create the data and archive directories if they do not already exist'''
    try:
        os.makedirs(config.ARCHIVE_FILE_DIR)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def get_archive_file_path():
    '''Get full archive file path'''
    return os.path.join(config.ARCHIVE_FILE_DIR, get_archive_file_name())

def get_archive_file_name():
    '''Returns a date-time stamped archive file name'''
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    return "{0}-{1}.gz".format(config.ARCHIVE_FILE_NAME, timestamp)
