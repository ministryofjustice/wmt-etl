#pylint: disable=W0613,W0621
'''Tests for extract file archival'''
import os
from shutil import copyfile
import pytest
from openpyxl import Workbook
import wmt_etl.etl_config as config
import wmt_etl.archive as archive

DUMMY_TIMESTAMP = '20170703-120530'
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DUMMY_FILE_SOURCE_PATH = os.path.join(THIS_DIR, 'data/full_inputs')
DUMMY_FILE_NAMES = ['ND01.xlsx', 'ND02.xlsx', 'ND03.xlsx']
DUMMY_FILE_PATHS = [os.path.join(config.IMPORT_FILE_DIR, name) for name in DUMMY_FILE_NAMES]
SOURCE_FILE_PATHS = [os.path.join(DUMMY_FILE_SOURCE_PATH, name) for name in DUMMY_FILE_NAMES]

@pytest.fixture(autouse=True)
def mock_known_timestamp(mocker):
    '''Fixture to inject dummy time for testing filename generation'''
    mocker.patch('time.strftime', return_value=DUMMY_TIMESTAMP)
    yield

@pytest.fixture()
def file_setup_teardown():
    ''' Generates and tears down dummy files to test archival'''
    for src, dest in zip(SOURCE_FILE_PATHS, DUMMY_FILE_PATHS):
        copyfile(src, dest)

    for file_name in DUMMY_FILE_PATHS:
        workbook = Workbook()
        workbook.save(file_name)

    try:
        yield
    finally:
        for archive_path in [f for f in os.listdir(config.ARCHIVE_FILE_DIR)
                             if f.endswith('.gz')]:
            os.remove(os.path.join(config.ARCHIVE_FILE_DIR, archive_path))

def test_get_archive_file_name():
    '''Test archive filename generation'''
    filename = archive.get_archive_file_name()
    assert filename == 'delius-extract-{0}.gz'.format(DUMMY_TIMESTAMP)

def test_get_archive_file_path():
    '''Test archive file path generation'''
    file_path = archive.get_archive_file_path()
    assert file_path == os.path.join(
        config.ARCHIVE_FILE_DIR,
        'delius-extract-{0}.gz'.format(DUMMY_TIMESTAMP))

@pytest.mark.integration
def test_file_archived(file_setup_teardown):
    '''Tests archival of files'''
    archive_name = archive.archive_files(DUMMY_FILE_PATHS)
    assert os.path.isfile(archive_name)
    for path in DUMMY_FILE_NAMES:
        assert not os.path.isfile(path)
