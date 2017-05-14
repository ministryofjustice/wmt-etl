'''Test for WMT configuration'''

import wmt_etl.etl_config as config

def test_default_configuration():
    ''' Test default config values are as expected '''
    assert config.DB_NAME == "wmt_db"
    assert config.IMPORT_FILE_DIR == "./data/"
    assert config.ARCHIVE_FILE_DIR == "./data/archive/"
    assert config.DB_USERNAME == "wmt_etl"
    assert config.DB_PASSWORD == "wmt_etl"
    assert config.DB_SCHEMA == "staging"
    assert config.DB_SERVER == "localhost"
    assert len(config.VALID_SHEET_NAMES) == 7
