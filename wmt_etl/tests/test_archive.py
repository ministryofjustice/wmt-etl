'''Tests for extract file archival'''
import os
import pytest
import wmt_etl.etl_config as config
import wmt_etl.archive as archive

DUMMY_TIMESTAMP = '20170703-120530'

@pytest.yield_fixture(autouse=True)
def mock_known_timestamp(mocker):
    '''Fixture to inject dummy time for testing filename generation'''
    mocker.patch('time.strftime', return_value=DUMMY_TIMESTAMP)
    yield

def test_get_archive_file_name():
    '''Test archive filename generation'''
    filename = archive.get_archive_file_name()
    assert filename == 'delius-extract-{0}.gz'.format(DUMMY_TIMESTAMP)

def test_get_archive_file_path():
    '''Test archive file path generation'''
    file_path = archive.get_archive_file_path()
    assert file_path == os.path.join(
        config.ARCHIVE_FILE_PATH,
        'delius-extract-{0}.gz'.format(DUMMY_TIMESTAMP))
