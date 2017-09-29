''' Tests for WMT extract file parser'''
import os
import pytest
from xlrd import XLRDError
import wmt_etl.extract_parser as parser

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_FILE_PATH = os.path.join(THIS_DIR, 'data/WMT_Extract_sample.xlsx')
INVALID_DATA_FILE_PATH = os.path.join(THIS_DIR, 'data/Invalid_WMT_Extract_sample.xlsx')
INVALID_FILE_TYPE_PATH = os.path.join(THIS_DIR, 'data/invalid.txt')

def test_column_unchanged():
    '''Already clean column names should remain unchanged'''
    name = 'staff_grade'
    clean = parser.clean_name(name)
    assert clean == name

def test_clean_names():
    '''Column names should be cleaned of illegal characters, case and trailing whitespace'''
    name = ' My-Staff_Grade '
    clean = parser.clean_name(name)
    assert clean == 'mystaff_grade'

def test_transform_cols():
    '''Set of column headers should be mapped to staging compatible format'''
    cols = ['OM_Key', 'Team_Code', 'LicIn1st16Weeks', 'V-CRN_Count']
    clean_cols = parser.transform_names(cols)
    assert clean_cols[0] == 'om_key'
    assert clean_cols[1] == 'team_code'
    assert clean_cols[2] == 'licin1st16weeks'
    assert clean_cols[3] == 'vcrn_count'

def test_validate_sheet_names():
    '''Test validation of extract workbook format'''
    sheet_names = [
        'Wmt_Extract',
        'Court_Reports',
        'Inst_Reports',
        'Flag_Warr_4_n',
        'Flag_Upw',
        'Flag_O_Due',
        'Flag_Priority',
        'Requirements',
        'CMS',
        'GS',
        'T2A']
    assert parser.validate_workbook_format(sheet_names)

def test_invalid_sheet_names():
    '''Test validation fails if extract format not as expected'''
    sheet_names = ['wmt_extract', 'court_reports', 'dummy_value']
    assert not parser.validate_workbook_format(sheet_names)

def test_load_workbook():
    '''Test that a workbook in XLSX format can be successfully loaded'''
    workbook = parser.load_workbook(TEST_DATA_FILE_PATH)
    assert len(workbook.sheet_names) == 10
    assert workbook.sheet_names[0] == 'WMT_Extract'
    assert workbook.sheet_names[1] == 'Court_Reports'
    assert workbook.sheet_names[len(workbook.sheet_names)-1] == 'T2A'

def test_parse_workbook():
    '''Test that a workbook can be parsed correctly'''
    workbook = parser.load_workbook(TEST_DATA_FILE_PATH)
    dataframes = parser.parse_workbook(workbook)
    assert len(dataframes) == 10
    assert not dataframes['wmt_extract'].empty
    assert len(dataframes['wmt_extract'].columns) == 41
    assert len(dataframes['wmt_extract'].index) == 2
    assert len(dataframes['court_reports'].columns) == 9
    assert len(dataframes['court_reports'].index) == 2
    assert dataframes['wmt_extract'].columns[3] == 'ldu_desc'
    assert dataframes['court_reports'].columns[7] == 'sdr_conv_last_30'

def test_load_workbook_missing_file():
    '''Loading a missing workbook file should raise an error'''
    with pytest.raises(IOError) as error:
        parser.load_workbook('./data/missing.xlsx')
    assert 'No such file or directory' in str(error.value)

def test_load_workbook_invalid():
    '''Loading a workbook with invalid format should raise an error'''
    with pytest.raises(ValueError) as error:
        parser.load_workbook(INVALID_DATA_FILE_PATH)
    assert 'Workbook does not contain the expected worksheets' in str(error.value)

def test_invalid_file_type():
    '''Loading any file other than a valid workbook will raise an error'''
    with pytest.raises(XLRDError) as error:
        parser.load_workbook(INVALID_FILE_TYPE_PATH)
    assert 'Unsupported format, or corrupt file' in str(error.value)
