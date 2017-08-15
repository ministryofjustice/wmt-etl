'''Test for WMT configuration'''

import wmt_etl.etl_config as config

def test_default_configuration():
    ''' Test default config values are as expected '''
    assert config.IMPORT_FILE_DIR == "./wmt_etl/tests/data/import"
    assert config.ARCHIVE_FILE_DIR == "./archive/"
    assert config.DB_STG_SCHEMA == "staging"
    assert config.DB_APP_SCHEMA == "app"
    assert len(config.VALID_SHEET_NAMES) == 7
