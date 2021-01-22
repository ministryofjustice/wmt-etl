#pylint: disable=W0613,W0621,W0611
'''Tests for import top level run module'''
from __future__ import absolute_import
from os.path import join, dirname, abspath
import os
import pytest
import wmt_etl.run as job
import wmt_etl.etl_config as config
import wmt_etl.extract_loader as loader
from wmt_etl.tests.test_extract_loader import cleanup_staging
from wmt_etl.tests.fixtures import clear_archive, copy_source_files

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
        expected_task_count = 1
        expected_ext_count = 5
        job.run()

        for name in config.VALID_SHEET_NAMES:
            select = 'SELECT COUNT(*) FROM {0}.{1}'.format(config.DB_STG_SCHEMA, name)

            results = connection.execute(select)
            for row in results:
                assert row[0] == expected_ext_count, "Expected %r row count" % expected_ext_count

        task_select = 'SELECT COUNT(*) FROM {0}.tasks'.format(config.DB_APP_SCHEMA)
        results = connection.execute(task_select)
        for row in results:
            assert row[0] == 1, "Expected %r task count" % expected_task_count

    finally:
        cleanup_staging(connection)
        connection.close()

# pylint: disable=duplicate-code
@pytest.fixture()
def file_setup_teardown():
    ''' Generates and tears down dummy files to test job execution'''
    copy_source_files(SOURCE_FILE_PATHS, DUMMY_FILE_PATHS)
    try:
        yield
    finally:
        clear_archive()
