#pylint: disable=W0613,W0621,W0611
'''Tests for import top level run module'''
from os.path import join, dirname, abspath
import pytest
import wmt_etl.run as job
import wmt_etl.etl_config as config
import wmt_etl.extract_loader as loader
from wmt_etl.tests.test_extract_loader import cleanup_staging
from wmt_etl.tests.test_archive import file_setup_teardown

THIS_DIR = dirname(abspath(__file__))
DUMMY_FILE_SOURCE_PATH = join(THIS_DIR, 'data/full_inputs')
DUMMY_FILE_NAMES = [
    'ND01.xlsx', 'ND02.xlsx', 'ND03.xlsx', 'ND04.xlsx', 'ND05.xlsx', 'ND06.xlsx', 'ND07.xlsx'
    ]
DUMMY_FILE_PATHS = [join(config.IMPORT_FILE_DIR, name) for name in DUMMY_FILE_NAMES]
SOURCE_FILE_PATHS = [join(DUMMY_FILE_SOURCE_PATH, name) for name in DUMMY_FILE_NAMES]

@pytest.mark.integration
def test_run_import(file_setup_teardown):
    ''' Test that the job runs under default configuration'''
    engine = loader.get_db_engine()
    connection = engine.connect()

    try:
        job.run()

        for name in config.VALID_SHEET_NAMES:
            select = 'SELECT COUNT(*) FROM {0}.{1}'.format(config.DB_STG_SCHEMA, name)

            results = connection.execute(select)
            for row in results:
                assert row[0] == 14

        task_select = 'SELECT COUNT(*) FROM {0}.tasks'.format(config.DB_APP_SCHEMA)
        results = connection.execute(task_select)
        for row in results:
            assert row[0] == 1

    finally:
        cleanup_staging(connection)
        connection.close()
