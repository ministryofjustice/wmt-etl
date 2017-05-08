
import unittest
import wmt_etl.etl_config as config

class EtlConfigTestCase(unittest.TestCase):
    '''
    TestCase for ETL process configuration
    '''

    def test_default_configuration(self):
        ''' Test default config values are as expected '''
        assert config.DB_NAME == "wmt_db"
        assert config.IMPORT_FILE_PATH == "./data/"
        assert config.ARCHIVE_FILE_PATH == "./data/archive/"
        assert config.DB_USERNAME == "wmt"
        assert config.DB_PASSWORD == "wmt"
        assert config.DB_SCHEMA == "staging"
        assert config.DB_SERVER == "localhost"
