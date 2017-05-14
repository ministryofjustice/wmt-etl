'''Functionality to populate staging schema with WMT extracts'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import wmt_etl.etl_config as config

def import_extract(dataframes, clean=False):
    '''Process all dataframes representing total contents of an extract workbook'''
    db_engine = get_db_engine()
    Session = scoped_session(sessionmaker(bind=db_engine))
    session = Session()
    try:
        for table_name, data in dataframes.iteritems():
            if clean:
                delete = 'DELETE FROM {0}.{1}'.format(config.DB_SCHEMA, table_name)
                session.execute(delete)
            process_dataframe(db_engine, table_name, data)
        session.commit()
    except:
        session.rollback()
        raise

def process_dataframe(db_engine, table_name, data):
    '''Process an individual dataframe'''
    schema = config.DB_SCHEMA
    write_to_staging(table_name, data, db_engine, schema)

def write_to_staging(table_name, dataframe, database, schema):
    ''' Insert dataframe into the target staging table'''
    dataframe.to_sql(table_name, database, schema=schema, if_exists='append', index=False)

def get_db_engine():
    ''' Get SQLAlchemy DB engine with which to open connection'''
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
