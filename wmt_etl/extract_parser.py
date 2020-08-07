'''Functionality for process WMT extract worksheets'''
import pandas as pd
import wmt_etl.etl_config as config
import logging

def load_workbook(file_path):
    ''' Load workbook at specified path'''
    workbook = pd.ExcelFile(file_path)
    if not validate_workbook_format(workbook.sheet_names):
        raise ValueError('Workbook does not contain the expected worksheets')
    return workbook

def parse_workbook(workbook, input_file):
    ''' Parse an individual workbook'''
    dataframes = {}
    for sheet in workbook.sheet_names:
        if clean_name(sheet) in config.VALID_SHEET_NAMES:
            worksheet = workbook.parse(sheet)
            worksheet.columns = transform_names(worksheet.columns)

            spreadsheetColumnsAsSet = set(worksheet.columns.tolist())
            expectedColumnsAsSet = set(config.VALID_COLUMNS[clean_name(sheet)])

            if not spreadsheetColumnsAsSet.issubset(expectedColumnsAsSet):
                unexpectedColumns = spreadsheetColumnsAsSet.difference(expectedColumnsAsSet)
                dataframes[clean_name(sheet)] = worksheet.drop(columns=list(unexpectedColumns))
                message = 'Removed the following unexpected columns: ' + str(list(unexpectedColumns)) + ' from the ' + clean_name(sheet) + ' tab in the ' + input_file + ' file'
                logging.info(message)
            else:
                dataframes[clean_name(sheet)] = worksheet

    return dataframes

def transform_names(names):
    ''' Map worksheet or column names to db staging table format'''
    return [clean_name(name) for name in names]

def clean_name(name):
    ''' Rules for transforming an extract worksheet or column name to staging table format'''
    illegal_chars = '-'
    return name.strip().replace(illegal_chars, '').lower()

def validate_workbook_format(sheet_names):
    '''XLSX file should be in the expected format - i.e. at min contains all valid sheet names'''
    return set(config.VALID_SHEET_NAMES).issubset(set(transform_names(sheet_names)))
