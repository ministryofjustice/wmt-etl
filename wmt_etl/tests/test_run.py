#pylint: disable=W0613,W0621,W0611
'''Tests for import top level run module'''
from os.path import join, dirname, abspath
import os
from shutil import copyfile
import pytest
import wmt_etl.run as job
import wmt_etl.etl_config as config
import wmt_etl.extract_loader as loader
from wmt_etl.tests.test_extract_loader import cleanup_staging

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
        EXPECTED_TASK_ROW_COUNT = 1
        EXPECTED_ROW_COUNT = 5
        job.run()

        for name in config.VALID_SHEET_NAMES:
            select = 'SELECT COUNT(*) FROM {0}.{1}'.format(config.DB_STG_SCHEMA, name)

            results = connection.execute(select)
            for row in results:
                assert row[0] == EXPECTED_ROW_COUNT, "Expected %r extract row count" % EXPECTED_ROW_COUNT

        task_select = 'SELECT COUNT(*) FROM {0}.tasks'.format(config.DB_APP_SCHEMA)
        results = connection.execute(task_select)
        for row in results:
            assert row[0] == 1, "Expected %r task count" % EXPECTED_TASK_ROW_COUNT

    finally:
        cleanup_staging(connection)
        connection.close()

@pytest.fixture()
def file_setup_teardown():
    ''' Generates and tears down dummy files to test archival'''
    for src, dest in zip(SOURCE_FILE_PATHS, DUMMY_FILE_PATHS):
        copyfile(src, dest)

    try:
        yield
    finally:
        for archive_path in [f for f in os.listdir(config.ARCHIVE_FILE_DIR)
                             if f.endswith('.tar.gz')]:
            os.remove(os.path.join(config.ARCHIVE_FILE_DIR, archive_path))
