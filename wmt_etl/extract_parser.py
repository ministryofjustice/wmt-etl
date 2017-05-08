'''Functionality for process WMT extract worksheets'''
import pandas as pd

def load_workbook(file_path):
    ''' Load workbook at specified path'''
    workbook = pd.ExcelFile(file_path)
    return workbook

def parse_workbook(workbook):
    ''' Parse an individual workbook'''
    dataframes = {}
    for sheet in workbook.sheet_names:
        dataframes[sheet] = workbook.parse(sheet)

    return dataframes
