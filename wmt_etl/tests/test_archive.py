'''Tests for extract file archival'''
import os
import pytest
from openpyxl import Workbook
import wmt_etl.etl_config as config
import wmt_etl.archive as archive

DUMMY_TIMESTAMP = '20170703-120530'
DUMMY_FILE_NAMES = ['ND01.xlsx', 'ND02.xlsx', 'ND03.xlsx']
DUMMY_FILE_PATHS = [os.path.join(config.IMPORT_FILE_DIR, name) for name in DUMMY_FILE_NAMES]

@pytest.fixture(autouse=True)
def mock_known_timestamp(mocker):
    '''Fixture to inject dummy time for testing filename generation'''
    mocker.patch('time.strftime', return_value=DUMMY_TIMESTAMP)
    yield

@pytest.fixture()
def file_setup_teardown():
    ''' Generates and tears down dummy files to test archival'''
    for file_name in DUMMY_FILE_PATHS:
        workbook = Workbook()
        workbook.save(file_name)

    try:
        yield
    finally:
        for path in DUMMY_FILE_PATHS:
            os.remove(path)
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
