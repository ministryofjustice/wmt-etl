''' Fixture and helper functions for reuse in tests'''
from os import path, remove, listdir
from shutil import copyfile
import wmt_etl.etl_config as config

def clear_archive():
    '''Clear down archive following test execution'''
    for archive_path in [f for f in listdir(config.ARCHIVE_FILE_DIR)
                         if f.endswith('.tar.gz')]:
        remove(path.join(config.ARCHIVE_FILE_DIR, archive_path))

def copy_source_files(source_file_paths, dest_file_paths):
    '''Copy source files to temp destination for testing'''
    for src, dest in zip(source_file_paths, dest_file_paths):
        copyfile(src, dest)
