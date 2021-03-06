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
        'Wmt_Extract_Filtered',
        'Court_Reports',
        'Inst_Reports',
        'Flag_Warr_4_n',
        'Flag_Upw',
        'Flag_O_Due',
        'Flag_Priority',
        'CMS',
        'GS',
        'ARMS',
        'T2A',
        'WMT_Extract_SA',
        'Suspended_Lifers',
        'T2a_Detail',
        'Omic_Teams']
    assert parser.validate_workbook_format(sheet_names)

def test_invalid_sheet_names():
    '''Test validation fails if extract format not as expected'''
    sheet_names = ['wmt_extract', 'court_reports', 'dummy_value']
    assert not parser.validate_workbook_format(sheet_names)

def test_load_workbook():
    '''Test that a workbook in XLSX format can be successfully loaded'''
    workbook = parser.load_workbook(TEST_DATA_FILE_PATH)
    assert len(workbook.sheet_names) == 16
    assert workbook.sheet_names[0] == 'WMT_Extract'
    assert workbook.sheet_names[1] == 'WMT_Extract_Filtered'
    assert workbook.sheet_names[2] == 'Court_Reports'
    assert workbook.sheet_names[13] == 'Suspended_Lifers'
    assert workbook.sheet_names[14] == 'T2A_Detail'
    assert workbook.sheet_names[15] == 'OMIC_Teams'

def test_parse_workbook():
    '''Test that a workbook can be parsed correctly'''
    workbook = parser.load_workbook(TEST_DATA_FILE_PATH)
    dataframes = parser.parse_workbook(workbook)
    print len(dataframes)
    assert len(dataframes) == 16
    assert not dataframes['wmt_extract'].empty
    assert len(dataframes['wmt_extract'].columns) == 41
    assert len(dataframes['wmt_extract'].index) == 2
    assert len(dataframes['court_reports'].columns) == 17
    assert len(dataframes['court_reports'].index) == 2
    assert dataframes['wmt_extract'].columns[3] == 'ldu_desc'
    assert dataframes['court_reports'].columns[7] == 'om_surname'

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
