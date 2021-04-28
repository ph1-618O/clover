#!/usr/bin/env python3
# coding: utf-8

## WORKING 
# ADD DATETIME FORMATTING FOR DATE COLUMN
# export data to MONGO DB



import platform

# working with dates, month abbrev, and the 
#  it takes to run prg
from datetime import datetime
from datetime import date
from calendar import month_abbr
import time

# for importing from excel to pandas
#from pandas import ExcelWriter
#from pandas import ExcelFile
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None
import pprint
pp = pprint.PrettyPrinter(indent=4)

# graphing
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
import squarify
import plotly.graph_objects as go

# for generating random data from original to test and share to github
from random import seed
from random import randint
import random

# Dealing with number input inconsistencies, avoids VALUE ERROR, ATTRIBUTE ERROR
from fastnumbers import fast_float

# trying to grab the trans data from google, need another way to do it
from googlesearch import search
from bs4 import BeautifulSoup as soup
import requests
import re

pd.set_option("display.max_rows", None, "display.max_columns", None)

# print versions
def version_assistant():
    # print versions
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    print('PYTHON VERSIONS')
    print('-----------------------------------------')
    print("python     : ",  platform.python_version())
    print("pandas     : ", pd.__version__)
    print("matplotlib : ", matplotlib.__version__)
    print("squarify   :  0.4.3")
    print('-----------------------------------------\n\n')


# Getting Data from Clipboard copied from Website DataFrame
# most of the data I began to work with to generate the working test data
# i had to get from the clipboard on websites


def read_clip():
    clipDF = pd.read_clipboard()
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    csvName = input('WHAT TYPE OF ACCOUNT FOR FILENAME?\n')
    csvName = csvName + '.csv'
    clipDF.to_csv(csvName, index=False)
    return pd.read_csv(csvName)


def insertRow(rowNum, df, rowVal):
    df1 = df[0:rowNum]
    df2 = df[rowNum:]
    df1.loc[rowNum] = rowVal
    dfResult = pd.concat([df1, df2])
    return dfResult

# convert_amount keeps value at positive or negative


def convert_amount(entry):
    # there are entries where there is no balance listed
    entry = str(entry)
    if '--' in entry:
        return 0
    # making the float negative
    if '-' in entry:
        return (float(entry.translate({ord(i): None for i in '$-,'})) * -1)
    else:
        return float(entry.translate({ord(i): None for i in '$-,'}))


def make_num(df, col_name):
    newCol = []
    for i in range(len(df)):
        newCol.append(convert_amount(df[col_name][i]))
    df[col_name] = newCol
    return df


def split_date(date_str):
    import re
    clean_list = re.sub(r"[,-/.]", " ", date_str) #,-/ and . are all common separators of a date
    return clean_list

# Begin coding to ask user if 04 is month or day, 19 is day and 2021 is year
# print((split_date(df['date'][0])).split())

def convert_date2(df):
    import datetime
    get_date_col = input('Enter the name of the date column\n').lower()
    date_time = []
    if isinstance(df[get_date_col][0], str):
        print((split_date(df[get_date_col][0])).split())
        for i in df[get_date_col]:
            break   
        for i in df[get_date_col]:
            date_time.append(datetime.datetime.strptime(i, original_date))
    elif isinstance(df[get_date_col[0], datetime.date]):
        return df
    else:
        print('INCORRECT DATE COLUMN')

def convert_date(df):
    import datetime
    date_time = []
    for i in df['date']:
        date_time.append(datetime.datetime.strptime(i, '%m/%d/%Y'))
    df['date'] = date_time
    return df

# def make_date(df, col_name):
#     newCol = []
#     for in in range(len(df)):
#         newCol.append(make_date(df[col_name][i]))
#         df[col_name] = newCol
#     return df

def get_sort_by(df):
    print('------------------------------------------------------------------------------------------------------')
    print('UNSORTED DATAFRAME')
    pp.pprint(df.head())
    print('------------------------------------------------------------------------------------------------------')
    print('OPTIONS:::')
    print('------------------------------------------------------------------------------------------------------')
    none_in = [print(list(df.columns)[i].upper(), end =" ") for i in range(len(list(df.columns)))]
    print('\n\nIT LOOKS LIKE YOUR DATES ARE OUT OF ORDER\n')
    sort_col = input(f'\nCHOOSE COLUMN TO SORT DATA BY?:: \n').lower()
    print('------------------------------------------------------------------------------------------------------')
    sort = ' '.join(str(elem) for elem in [i for i in df.columns if i == sort_col.lower()])
    return sort


def format_clipCSV(df, columns_list):
    row1 = []
    for col in df.columns:
        row1.append(col)
    for i in range(len(row1)):
        df.rename(columns={df.columns[i]: columns_list[i]}, inplace=True)
    # inserting the data into row 0
    df = (insertRow(0, df, row1)).reset_index(drop=True)
    # Asking user what columns they want to keep
    remove_cols = input('COLUMNS TO REMOVE::\n')
    remove = ''
    for k in remove_cols:
        if ',' in k:
            remove += k.strip(',')
        else:
            remove += k
    remove = remove.split(' ')
    for c in remove:
        try:
            df[c.lower()]
            df = df.drop(columns = c, axis = 1)
        except KeyError:
            print('ERROR, RE-ENTER COLUMN\n')
    # Formatting amount column into floats
    if 'amount' in df.columns:
        make_num(df, 'amount')
    # Formatting date column into datetime obj
    if 'date' in df.columns:
        convert_date(df)
    ## Giving examples of data
    sort_which = get_sort_by(df)
    df = df.sort_values(sort_which.lower()).reset_index(drop=True)
    return df

# Bringing in Data
def read_csv():
    csvName = input('ENTER CSV NAME\n')
    print('-----------------------------------------')
    if csvName.endswith('.csv'):
        return pd.read_csv(csvName)
    else:
        csvName = csvName + '.csv'
        return pd.read_csv(csvName)

def get_column_names(df):
    print(f'\n{" - ".join(list(df.columns))}\n\n')
    format_input = input('RENAME COLUMNS? Y/N\n')
    if 'y' in format_input:
        print('------------------------------------------------------------------------------------------------------')
        print('WARNING COLUMN NAMES MUST BE UNIQUE')
        print('------------------------------------------------------------------------------------------------------')
        cols = input('ENTER COLUMN NAMES\n')
        cat = ''
        for i in cols:
            if ',' in cols:
                cat += i.strip(',')
            else:
                cat += i
        cols = cat.split(' ')
        return cols
    else:
        return list(df.columns)

def initiate_format(df = 0):
    print('FORMATTING CLIPBOARD OR CSV INPUT')
    print('------------------------------------------------------------------------------------------------------')
    # df = read_clip()
    df = read_csv()
# Asking user if they want to rename the columns
    cols = get_column_names(df)
    if len(cols) == len(df.columns):
        for i in range(len(df.columns)):
            df.rename(columns = {df.columns[i]:cols[i]})
    else:
        print(f'PLEASE ENTER {len(df.columns)} COLUMN NAMES\n')
        verify_cols = input(f'ARE THESE THE CORRECT COLUMN NAMES:: Y OR N {cols}\n')
        if 'n' in verify_cols:
            cols = get_column_names(df)

    formatted_csv = format_clipCSV(df, cols)
    print('------------------------------------------------------------------------------------------------------')
    print('FORMATTED DATAFRAME')
    print('------------------------------------------------------------------------------------------------------')
    pp.pprint(formatted_csv.head())
    print('------------------------------------------------------------------------------------------------------')
    print('FORMATTING CLIPBOARD OR CSV COMPLETE')
    print('------------------------------------------------------------------------------------------------------')
    print('------------------------------------------------------------------------------------------------------\n\n\n')
    return formatted_csv

def main():
    initiate_format()

if __name__ == "__main__":
    main()



