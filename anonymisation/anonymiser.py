import pandas as pd
import anonymiser_config as config
from os.path import isfile, join, exists
from os import listdir, mkdir
import time

def main():
    ''' Load workbook at specified path'''
    input_files = get_input_files()
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    mkdir('./output_files/' + timestamp)
    for workbook_file_name in input_files:
        workbook = pd.ExcelFile(workbook_file_name)

        dataframes = {}
        for sheet in workbook.sheet_names:
            worksheet = workbook.parse(sheet)
            worksheet.columns = transform_names(worksheet.columns)

            spreadsheetColumnsAsSet = set(worksheet.columns.tolist())

            expectedColumnsAsSet = set(config.VALID_COLUMNS[clean_name(sheet)])

            if not spreadsheetColumnsAsSet.issubset(expectedColumnsAsSet):
                unexpectedColumns = spreadsheetColumnsAsSet.difference(expectedColumnsAsSet)
                dataframes[clean_name(sheet)] = worksheet.drop(labels=list(unexpectedColumns), axis=1)
                message = 'Removed the following unexpected columns: ' + str(list(unexpectedColumns)) + ' from the ' + clean_name(sheet) + ' tab in the ' + workbook_file_name + ' file'
                print(message)
            else:
                dataframes[clean_name(sheet)] = worksheet

            if clean_name(sheet) == 'wmt_extract' or clean_name(sheet) == 'court_reports' or clean_name(sheet) == 'omic_teams':
                dataframes[clean_name(sheet)]['om_surname'] = dataframes[clean_name(sheet)]['om_key']
            if clean_name(sheet) == 'wmt_extract_filtered' or clean_name(sheet) == 't2a':
                dataframes[clean_name(sheet)]['om_surname'] = ''
                dataframes[clean_name(sheet)]['om_forename'] = ''
            if clean_name(sheet) == 'inst_reports':
                dataframes[clean_name(sheet)]['om_name'] = ''
            if clean_name(sheet) == 'cms':
                dataframes[clean_name(sheet)]['contact_staff_name'] = ''
                dataframes[clean_name(sheet)]['om_name'] = ''
            if clean_name(sheet) == 'gs':
                dataframes[clean_name(sheet)]['om_name'] = ''
            if clean_name(sheet) == 'arms':
                dataframes[clean_name(sheet)]['assessment_staff_name'] = ''
                dataframes[clean_name(sheet)]['offender_manager_staff_name'] = ''
            if clean_name(sheet) == 't2a_detail':
                dataframes[clean_name(sheet)]['staff_name_order_manager'] = ''
                dataframes[clean_name(sheet)]['staff_name_offender_manager'] = ''
        newFileName = './output_files/' + timestamp + '/' + clean_file_name(workbook_file_name)
       
        print(newFileName)
        with pd.ExcelWriter(newFileName) as writer:
            for table_name, data in dataframes.iteritems():
                data.to_excel(writer, sheet_name=table_name, index=False)


def transform_names(names):
    ''' Map worksheet or column names to db staging table format'''
    return [clean_name(name) for name in names]

def clean_name(name):
    ''' Rules for transforming an extract worksheet or column name to staging table format'''
    illegal_chars = '-'
    return name.strip().replace(illegal_chars, '').lower()

def clean_file_name(name):
    ''' Rules for transforming an extract worksheet or column name to staging table format'''
    illegal_chars = './input_files/'
    return name.strip().replace(illegal_chars, '')

def get_input_files():
    '''Return list of files to process'''
    return [join(config.IMPORT_FILE_DIR, f)
            for f in listdir(config.IMPORT_FILE_DIR)
            if isfile(join(config.IMPORT_FILE_DIR, f))
            and f.endswith(config.EXPECTED_FILE_EXTENSIONS)]

if __name__ == '__main__':
    main()
