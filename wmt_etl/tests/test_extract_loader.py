''' Tests for extract loader'''
from os.path import dirname, abspath, join
from sqlalchemy.exc import ProgrammingError
import pytest
import wmt_etl.etl_config as config
import wmt_etl.extract_loader as loader
import wmt_etl.extract_parser as parser

THIS_DIR = dirname(abspath(__file__))
TEST_DATA_FILE_PATH = join(THIS_DIR, 'data/full_inputs/ND01.xlsx')

def cleanup_staging(connection):
    ''' Clean up staging records created for testing'''
    for name in config.VALID_SHEET_NAMES:
        delete = 'DELETE FROM {0}.{1}'.format(config.DB_SCHEMA, name)
        connection.execute(delete)

@pytest.mark.integration
def test_should_import_extract():
    '''Should import valid dataframes to staging schema'''
    workbook = parser.load_workbook(TEST_DATA_FILE_PATH)
    dataframes = parser.parse_workbook(workbook)
    loader.import_extract(dataframes)
    engine = loader.get_db_engine()
    connection = engine.connect()

    try:
        for name in config.VALID_SHEET_NAMES:
            select = 'SELECT COUNT(*) FROM {0}.{1}'.format(config.DB_SCHEMA, name)
            results = connection.execute(select)
            for row in results:
                assert row[0] == 2
    finally:
        cleanup_staging(connection)
        connection.close()

@pytest.mark.integration
def test_import_extract_rollback():
    '''Failed staging load should roll back all operations'''
    workbook = parser.load_workbook(TEST_DATA_FILE_PATH)
    dataframes = parser.parse_workbook(workbook)
    engine = loader.get_db_engine()
    connection = engine.connect()

    try:
        with pytest.raises(ProgrammingError, message='Expecting ProgrammingError') as error:
            config.DB_SCHEMA = 'invalid'
            loader.import_extract(dataframes)
        assert '''schema "invalid" does not exist''' in str(error.value)
    finally:
        config.DB_SCHEMA = 'staging'
        cleanup_staging(connection)
        connection.close()



@pytest.mark.integration
def test_get_db_engine():
    '''Should create a new database engine instance for connection'''
    engine = loader.get_db_engine()
    assert engine is not None
    try:
        connection = engine.connect()
        assert connection is not None
        assert connection.engine == engine
    finally:
        connection.close()

def test_get_connection_string():
    '''Test connection strings are correctly constructed'''
    expected_conn_string = '{0}://{1}:{2}@{3}/{4}'.format(
        config.DB_ENGINE,
        config.DB_USERNAME,
        config.DB_PASSWORD,
        config.DB_SERVER,
        config.DB_NAME)
    actual_conn_string = loader.get_connection_string()
    assert expected_conn_string == actual_conn_string