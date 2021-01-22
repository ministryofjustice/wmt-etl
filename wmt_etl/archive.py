'''Module to compress and archive processed extract files'''
from __future__ import absolute_import
import os
import time
from shutil import make_archive
import errno
import wmt_etl.etl_config as config

def archive_files(file_paths):
    '''Add all region files to a single compressed archive'''
    archive_name = get_archive_file_path()
    create_data_directories()
    make_archive(archive_name, 'gztar', config.IMPORT_FILE_DIR)
    for path in file_paths:
        os.unlink(path)
    return archive_name

def create_data_directories():
    '''Create the data and archive directories if they do not already exist'''
    try:
        os.makedirs(config.IMPORT_FILE_DIR)
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
    return "{0}-{1}".format(config.ARCHIVE_FILE_NAME, timestamp)
