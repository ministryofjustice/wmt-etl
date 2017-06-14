'''Functionality to populate staging schema with WMT extracts'''
from sqlalchemy import create_engine
import wmt_etl.etl_config as config

PROCESS_IMPORT_TASK_TYPE = 'PROCESS-IMPORT'
SUBMITTING_AGENT = 'DATA-IMPORT'
TASK_STATUS_PENDING = 'PENDING'
TASK_TABLE = 'tasks'

def import_extract(dataframes, clean=False, complete=False):
    '''Process all dataframes representing total contents of an extract workbook'''
    db_engine = get_db_engine()
    with db_engine.connect() as connection, connection.begin():
        for table_name, data in dataframes.iteritems():
            if clean:
                delete = 'DELETE FROM {0}.{1}'.format(config.DB_STG_SCHEMA, table_name)
                connection.execute(delete)
            process_dataframe(connection, table_name, data)

        if complete:
            create_import_task(connection)

def create_import_task(connection):
    '''Create a new Task which indicates import process completion to Worker'''
    insert = """INSERT INTO {0}.{1} (submitting_agent, type, status)
                VALUES ('{2}', '{3}', '{4}')""".format(
                    config.DB_APP_SCHEMA,
                    TASK_TABLE,
                    SUBMITTING_AGENT,
                    PROCESS_IMPORT_TASK_TYPE,
                    TASK_STATUS_PENDING)
    connection.execute(insert)

def process_dataframe(connection, table_name, data):
    '''Process an individual dataframe'''
    schema = config.DB_STG_SCHEMA
    write_to_staging(table_name, data, connection, schema)

def write_to_staging(table_name, dataframe, connection, schema):
    ''' Insert dataframe into the target staging table'''
    dataframe.to_sql(table_name, connection, schema=schema, if_exists='append', index=False)

def get_db_engine():
    ''' Get SQLAlchemy DB engine with which to open connection'''
    connection_string = get_connection_string()
    return create_engine(connection_string)

def get_connection_string():
    ''' Get formatted db connection string'''
    return '{0}://{1}@{3}:{2}@{3}/{4}'.format(
        config.DB_ENGINE,
        config.DB_USERNAME,
        config.DB_PASSWORD,
        config.DB_SERVER,
        config.DB_NAME)
