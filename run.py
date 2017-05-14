'''
Run main ETL application process
'''
import logging
from os import listdir
from os.path import isfile, join
import wmt_etl.etl_config as config
import wmt_etl.archive as archive
import wmt_etl.extract_parser as parser
import wmt_etl.extract_loader as loader

def main():
    '''Main application entry point'''
    print "Running load to {}".format(config.DB_SCHEMA)
    input_files = get_input_files()
    try:
        if len(input_files) < config.EXPECTED_FILE_COUNT:
            raise ValueError('Not all expected extract files are present')

        process_file(input_files[0], clean_tables=True)
        for workbook_file_name in input_files[1:]:
            process_file(workbook_file_name, clean_tables=False)
    finally:
        try:
            archive.archive_files(input_files)
        except Exception as ex:
            logging.exception(ex)

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

if __name__ == '__main__':
    main()
