'''
Run main ETL application process
'''
import logging
from os import listdir, mkdir
from os.path import isfile, join, exists
import log
import wmt_etl.etl_config as config
import wmt_etl.archive as archive
import wmt_etl.extract_parser as parser
import wmt_etl.extract_loader as loader

def main():
    '''Main application entry point'''
    setup_log_dir()
    log.setup_logging()
    logging.info("Running load to schema %s", config.DB_SCHEMA)
    input_files = get_input_files()
    try:
        if len(input_files) < config.EXPECTED_FILE_COUNT:
            raise ValueError('Not all expected extract files are present')

        process_file(input_files[0], clean_tables=True)
        for workbook_file_name in input_files[1:]:
            process_file(workbook_file_name, clean_tables=False)
    except Exception, ex:
        logging.error(ex.message, exc_info=True)
    finally:
        try:
            archive_name = archive.archive_files(input_files)
            logging.info('Archived input files to %s', archive_name)
        except Exception:
            logging.error('Error archiving extract files', exc_info=True)
        logging.info('Extract process completed')

def process_file(input_file, clean_tables):
    ''' Process a single extract workbook file'''
    workbook = parser.load_workbook(input_file)
    dataframes = parser.parse_workbook(workbook)
    loader.import_extract(dataframes, clean_tables)

def get_input_files():
    '''Return list of files to process'''
    return [join(config.IMPORT_FILE_DIR, f)
            for f in listdir(config.IMPORT_FILE_DIR)
            if isfile(join(config.IMPORT_FILE_DIR, f))
            and f.endswith(config.EXPECTED_FILE_EXTENSIONS)]

def setup_log_dir():
    '''Ensure configured logging directory exists'''
    if not exists(config.LOGGING_DIR):
        try:
            mkdir(config.LOGGING_DIR)
        except:
            logging.error('Could not create logging directory', exc_info=True)
            raise

if __name__ == '__main__':
    main()
