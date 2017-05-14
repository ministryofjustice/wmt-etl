'''
Application configuration settings
'''
import os

# WMT Database - target staging schema
DB_ENGINE = os.getenv('WMT_DB_ENGINE', 'postgresql')
DB_SERVER = os.getenv('WMT_DB_SERVER', 'localhost')
DB_NAME = os.getenv('WMT_DB_NAME', 'wmt_db')
DB_SCHEMA = os.getenv('WMT_DB_SCHEMA', 'staging')
DB_USERNAME = os.getenv('WMT_DB_USERNAME', 'wmt_etl')
DB_PASSWORD = os.getenv('WMT_DB_PASSWORD', 'wmt_etl')

# Extract file settings
IMPORT_FILE_DIR = os.getenv('WMT_IMPORT_FILE_PATH', './data/')
ARCHIVE_FILE_DIR = os.getenv('WMT_ARCHIVE_FILE_PATH', './data/archive/')
ARCHIVE_FILE_NAME = os.getenv('WMT_ARCHIVE_FILE_NAME', 'delius-extract')
EXPECTED_FILE_COUNT = 7
EXPECTED_FILE_EXTENSIONS = ('.xlsx', '.xls')

# Extract valid source worksheet tabs
VALID_SHEET_NAMES = [
    'wmt_extract',
    'court_reports',
    'inst_reports',
    'flag_warr_4_n',
    'flag_upw',
    'flag_o_due',
    'flag_priority']
