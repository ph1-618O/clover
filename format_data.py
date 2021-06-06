#!/usr/bin/env python3
# coding: utf-8

# format_data.py works to normalize data that is messy, imported from a clipboard or in a 
# xls format so that it has proper headings, datetime, and numerical formatting for computation


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
pd.set_option('expand_frame_repr', False)

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
    entry = str(entry).strip()
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
    return df.reset_index(drop=True)

# Another place that if I had the dataset I could use machine learning to figure out
# the actual date format without asking
# Begin coding to ask user if 04 is month or day, 19 is day and 2021 is year
def split_date(date_str):
    import re
    clean_list = re.sub(r"[,-/.]", " ", date_str) #,-/ and . are all common separators of a date
    return clean_list

# print((split_date(df['date'][0])).split())

# CONVERT DATE 2 is for more complicated date formats
def convert_date_complicated(df):
    import datetime
    get_date_col = input('DATE COLUMN NAME:: \n').lower()
    date_time = []
    if isinstance(df[get_date_col][0], str):
        date_list = (split_date(df[get_date_col][0])).split()
        print(date_list)
        date_format_part1 = []
        for i in date_list:
            date_format_part1.append((input(f'ENTER MONTH DAY OR YEAR FOR {i}\n')).lower())
        print(date_format_part1)
        date_format = '%m/%d/%Y'
        for i in df[get_date_col]:
            break   
        for i in df[get_date_col]:
            date_time.append(datetime.datetime.strptime(i, date_format))
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
    return df.reset_index(drop=True)

# def make_date(df, col_name):
#     newCol = []
#     for in in range(len(df)):
#         newCol.append(make_date(df[col_name][i]))
#         df[col_name] = newCol
#     return df


def get_sort_by(df, sort_query):
    print('------------------------------------------------------------------------------------------------------')
    print('UNSORTED DATAFRAME')
    print('------------------------------------------------------------------------------------------------------')
    pp.pprint(df.head())
    print(f'\nSORTING BY {sort_query}')
    print('------------------------------------------------------------------------------------------------------')
    print(f'OPTIONS::: {" - ".join(list(df.columns))}')
    print('------------------------------------------------------------------------------------------------------')
    #none_in = [print(list(df.columns)[i].upper(), end =" ") for i in range(len(list(df.columns)))]
    try:
        df[sort_query]
        sort = sort_query
    except:
        import create_budget_dict
        sort_col = create_budget_dict.constrain_input_loop(sort_query, list(df.columns))
        # sort_col = input(
        #         f'\n\nCHOOSE COLUMN TO SORT {sort_query} BY?:: \n').lower()
        sort = ' '.join(str(elem)
                        for elem in [i for i in df.columns if i == sort_col.lower()])
    return sort




def format_data(df, columns_list=0):
    df = remove_cols(df, columns_list)

    # Formatting amount column into floats
    if 'amount' in df.columns:
        df = make_num(df, 'amount')
    # Formatting date column into datetime obj
    if 'date' in df.columns:
        df = convert_date(df)
    #     sorted_df = df.sort_values(by=['date']).reset_index(drop=True)
    #     sort_test = sorted_df['date']

    #     if sort_test.to_list() != list(df.date):
    #         print('------------------------------------------------------------------------------------------------------') 
    #         print('IT LOOKS LIKE YOUR DATES ARE OUT OF ORDER')
    #         print('------------------------------------------------------------------------------------------------------')
    #         date_col = input(f'CHOOSE COLUMN TO SORT DATE BY?:: \n').lower()
    #         sort_by = get_sort_by(df, date_col)
    # #sort_by = get_sort_by(df, col_with_dates)
    # #sort_which = get_sort_by(df)
    #         df = df.sort_values(sort_by.lower()).reset_index(drop=True)
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


def remove_cols(df, columns_list):
    row1 = []
    for col in df.columns:
        row1.append(col)
    for i in range(len(row1)):
        df.rename(columns={df.columns[i]: columns_list[i]}, inplace=True)
    # inserting the data into row 0
    df = (insertRow(0, df, row1)).reset_index(drop=True)
    # Asking user what columns they want to keep
    print('------------------------------------------------------------------------------------------------------')
    pp.pprint(df.head(1))
    print('------------------------------------------------------------------------------------------------------')
    remove_query = input('REMOVE COLUMNS? Y/N\n')
    if 'y' in remove_query.lower():
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
    return df

def get_col_names(df):
    print('------------------------------------------------------------------------------------------------------')
    print(f'CURRENT COLUMNS::: {" - ".join(list(df.columns))}')
    print('------------------------------------------------------------------------------------------------------')
    format_input = input('RENAME COLUMNS? Y/N\n')
    suggested_cols = ['Name', 'Date', 'Transaction', 'Account', 'Amount', 'Balance']
    if 'y' in format_input:
        print('------------------------------------------------------------------------------------------------------')
        print('WARNING COLUMN NAMES MUST BE UNIQUE')
        print('------------------------------------------------------------------------------------------------------')
        print(f'SUGGESTED::: {" - ".join(suggested_cols)}')
        print('------------------------------------------------------------------------------------------------------')
        cols = input('ENTER COLUMN NAMES IN ORDER\n')
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
    print('FORMATTING CLIPBOARD, EXCEL OR CSV INPUT')
    print('------------------------------------------------------------------------------------------------------')
    # df = read_clip()
    # df = read_csv()
# Asking user if they want to rename the columns
    cols = get_col_names(df)
    if len(cols) == len(df.columns):
        pass
    #possibly running rename cols twice
        # for i in range(len(df.columns)):
        #     df = df.rename(columns = {df.columns[i]:cols[i]})
            #print(cols)
            #pp.pprint(df.head())
            #break   
    # ADD constrain_input loop here
    else:
        print(f'PLEASE ENTER {len(df.columns)} COLUMN NAMES\n')
        verify_cols = input(f'ARE THESE THE CORRECT COLUMN NAMES:: Y OR N {cols}\n')
        if 'n' in verify_cols:
            cols = get_col_names(df)

    formatted_csv = format_data(df, cols)
    print('------------------------------------------------------------------------------------------------------')
    print('FORMATTED DATAFRAME')
    print('------------------------------------------------------------------------------------------------------')
    pp.pprint(formatted_csv.head())
    print('------------------------------------------------------------------------------------------------------')
    print('FORMATTING CLIPBOARD OR CSV COMPLETE')
    print('------------------------------------------------------------------------------------------------------')
    print('------------------------------------------------------------------------------------------------------\n\n')
    time.sleep(2)
    return formatted_csv

def main():
    initiate_format()

if __name__ == "__main__":
    main()


#data/green_may2621_training.csv
#date1, date, transaction, card, amount, balance
#date1, card, balance

