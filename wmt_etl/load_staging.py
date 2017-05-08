'''Functionality to populate staging schema with WMT extracts'''

from sqlalchemy import create_engine
import wmt_etl.etl_config as config

def import_extract(dataframes):
    '''Process all dataframes representing total contents of an extract workbook'''
    for key, value in dataframes.iteritems():
        process_dataframe(key, value)

def process_dataframe(sheet_name, sheet_data):
    '''Process an individual dataframe'''
    database = get_connection()
    schema = config.DB_SCHEMA
    table_name = map_tablename(sheet_name)
    write_to_staging(table_name, sheet_data, database, schema)
    return table_name

def map_tablename(key):
    '''Maps Extract sheet name to staging table'''
    return 'stg_{}'.format(key.lower())

def write_to_staging(table_name, dataframe, database, schema):
    ''' Insert dataframe into the target staging table'''
    dataframe.to_sql(table_name, database, schema=schema, if_exists='append')

def get_connection():
    ''' Get SQLAlchemy DB connection'''
    connection_string = get_connection_string()
    return create_engine(connection_string)

def get_connection_string():
    ''' Get formatted db connection string'''
    return '{0}://{1}:{2}@{3}/{4}'.format(
        config.DB_ENGINE,
        config.DB_USERNAME,
        config.DB_PASSWORD,
        config.DB_SERVER,
        config.DB_NAME)
