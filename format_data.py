#!/usr/bin/env python3
# coding: utf-8

# format_data.py works to normalize data that is messy, imported from a csv, clipboard or in a
# xls format so that it has proper headings, datetime, and numerical formatting for computation


# WORKING
# ADD DATETIME FORMATTING FOR DATE COLUMN
# export data to MONGO DB


from texthero import preprocessing
import re
import requests
from bs4 import BeautifulSoup as soup
from googlesearch import search
from fastnumbers import fast_float
import random
from random import randint
from random import seed
import plotly.graph_objects as go
import squarify
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import pprint
import os
import platform

# working with dates, month abbrev, and the
#  it takes to run prg
import datetime

# from datetime import datetime
# from datetime import date
from calendar import month_abbr
import time

# for importing from excel to pandas
# from pandas import ExcelWriter
# from pandas import ExcelFile
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

# Test Editing Libraries
# import texthero as hero #pip install texthero==1.0.5 works with newer python versions
# pip install nltk #NLP

# nltk.download("stopwords")
# nltk.download("punkt")

pp = pprint.PrettyPrinter(indent=4)
line_size = os.get_terminal_size()
line = line_size[0]


def p_line():
    line = ''
    for i in range(line_size[0]):
        line += '-'
    print(line)


def p_slash():
    line = ''
    for i in range(line_size[0]):
        line += '/'
    print(line)


# graphing

# for generating random data from original to test and share to github

# Dealing with number input inconsistencies, avoids VALUE ERROR, ATTRIBUTE ERROR

# trying to grab the trans data from google, need another way to do it

pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option("expand_frame_repr", False)

# print versions


def version_assistant():
    # print versions
    p_slash()
    print("PYTHON VERSIONS")
    print("-----------------------------------------")
    print("python     : ", platform.python_version())
    print("pandas     : ", pd.__version__)
    print("matplotlib : ", matplotlib.__version__)
    print("squarify   :  0.4.3")
    print("-----------------------------------------\n\n")


# Getting Data from Clipboard copied from Website DataFrame
# most of the data I began to work with to generate the working test data
# i had to get from the clipboard on websites


def import_clip():
    clipDF = pd.read_clipboard()
    p_slash()
    csvName = input("WHAT TYPE OF ACCOUNT FOR FILENAME?\n")
    csvName = csvName + ".csv"
    clipDF.to_csv(csvName, index=False)
    return pd.read_csv(csvName)


# convert_amount keeps value at positive or negative

def reconcile_column_type(df, dict):
    new_cols = list(df.columns)
    old_cols = dict['0_format']
    test_new = set(new_cols)
    test_old = set(old_cols)
    diff = test_new.difference(test_old)
    col_format = {}
    if not diff:
        print('Column list is the same')
    else:
        print(diff)
        for i in diff:
            if i in new_cols:
                print(i)
            elif i in old_cols:
                print(i)


def convert_amount(entry):
    # there are entries where there is no balance listed
    entry = str(entry).strip()
    if "--" in entry:
        return 0
    # making the float negative
    if "-" in entry:
        return float(entry.translate({ord(i): None for i in "$-,"})) * -1
    else:
        return float(entry.translate({ord(i): None for i in "$-,"}))


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

    clean_list = re.sub(
        r"[,-/.]", " ", date_str
    )  # ,-/ and . are all common separators of a date
    return clean_list


# CONVERT DATE complicated is for more complicated date formats
def convert_date_complicated(df):
    import datetime

    get_date_col = input("DATE COLUMN NAME:: \n").lower()
    date_time = []
    if isinstance(df[get_date_col][0], str):
        date_list = (split_date(df[get_date_col][0])).split()
        print(date_list)
        date_format_part1 = []
        for i in date_list:
            date_format_part1.append(
                (input(f"ENTER MONTH DAY OR YEAR FOR {i}\n")).lower()
            )
        print(date_format_part1)
        date_format = "%m/%d/%y"
        for i in df[get_date_col]:
            break
        for i in df[get_date_col]:
            date_time.append(datetime.datetime.strptime(i, date_format))
    elif isinstance(df[get_date_col[0], datetime.date]):
        return df
    else:
        print("INCORRECT DATE COLUMN")


def convert_date(df):
    import datetime
    list_cols = [i.lower() for i in df.columns.tolist()]
    test_cols = ["date", "day", "time", "occurence"]
    verified_cols = []
    for col in list_cols:
        for test in test_cols:
            if test in col:
                verified_cols.append(col)
    for tested in verified_cols:
        search_dates = df[tested].apply(
            lambda x: 'True' if isinstance(x, datetime.date) else 'False')
        if not search_dates.any():
            p_slash()
            print('ALL DATES ARE IN DATETIME SKIPPING')
            p_slash()
            continue
        elif (df[tested].map(type) == str).all():
            date_time = []
            for j in df[tested]:
                if len(j) == 10:
                    date_time.append(
                        datetime.datetime.strptime(j, "%m/%d/%Y"))
                elif len(j) == 8:
                    date_time.append(
                        datetime.datetime.strptime(j, "%m/%d/%y"))
                else:
                    print("UNKNOWN DATE FORMAT SKIPPING FORMATTING")
                    return df
            df[tested] = date_time
            df = df.sort_values(
                by=[tested]).reset_index(drop=True)
            # Want to use sort_values by tested, however, because its a loop it wont choose the primary date col
            # df = df.sort_values(
            #     by=['date', 'transaction', 'amount']).reset_index(drop=True)
            # (by=['date', 'category', 'identifier', 'amount']
        else:
            print('your dates are a mess, see your programmer')
    return df



def get_sort_by(df, sort_query):
    p_line()
    print("UNSORTED DATAFRAME")
    p_line()
    pp.pprint(df.head())
    print(f"\nSORTING BY {sort_query}")
    p_line()
    print(f'OPTIONS::: {" - ".join(list(df.columns))}')
    p_line()
    # none_in = [print(list(df.columns)[i].upper(), end =" ") for i in range(len(list(df.columns)))]
    try:
        df[sort_query]
        sort = sort_query
    except:
        import budget

        sort_col = budget.constrain_input_loop(sort_query, list(df.columns))
        sort = " ".join(
            str(elem) for elem in [i for i in df.columns if i == sort_col.lower()]
        )
    return sort


# Bringing in Data
def import_csv():
    csvName = input("ENTER CSV NAME\n")
    p_line()
    if csvName.endswith(".csv"):
        return pd.read_csv(csvName)
    else:
        csvName = csvName + ".csv"
        return pd.read_csv(csvName)


def inserting_first(df, columns_list):
    row1 = []
    # grabbing the data in the columns from the df
    for col in df.columns:
        row1.append(col)
    df = rename_cols(df, columns_list)
    # inserting the data into row 0
    df = (insertRow(0, df, row1)).reset_index(drop=True)
    return df


def insertRow(rowNum, df, rowVal):
    df1 = df[0:rowNum]
    df2 = df[rowNum:]
    df1.loc[rowNum] = rowVal
    dfResult = pd.concat([df1, df2])
    return dfResult


def rename_cols(df, columns_list):
    for i in range(len(columns_list)):
        df.rename(columns={df.columns[i]: columns_list[i]}, inplace=True)
    return df


def remove_cols(df):
    p_line()
    pp.pprint(df.head(1))
    p_line()
    remove_query = input("REMOVE COLUMNS? Y/N\n").lower()
    if "y" in remove_query.lower():
        remove_cols = input("COLUMNS TO REMOVE::\n").lower()
        remove = ""
        for k in remove_cols:
            if "," in k:
                remove += k.strip(",")
            else:
                remove += k
        remove = remove.split(" ")
        for c in remove:
            try:
                df[c.lower()]
                df = df.drop(columns=c, axis=1)
            except KeyError:
                print("ERROR, RE-ENTER COLUMN\n")
    return df


def get_col_names(df):
    rename_cols_query = "test"
    while "y" not in rename_cols_query:
        p_line()
        print(f'CURRENT COLUMNS::: {" - ".join(list(df.columns))}')
        p_line()
        rename_cols_query = input("RENAME COLUMNS? Y/N\n").lower()
        suggested_cols = ["Date", "Transaction",
                          "Account", "Amount", "Balance"]
        cols = list(df.columns)
        if "y" in rename_cols_query:
            p_line()
            print(f"PLEASE ENTER {len(df.columns)} COLUMN NAMES")
            print("WARNING COLUMN NAMES MUST BE UNIQUE")
            p_line()
            print(f'SUGGESTED::: {" - ".join(suggested_cols)}')
            p_line()
            print("REQUIRED ::: Date, Transaction, Amount")
            p_line()
            cols = input("ENTER COLUMN NAMES IN ORDER\n").lower()
            cat = ""
            for i in cols:
                if "," in cols:
                    cat += i.strip(",")
                else:
                    cat += i
            cols = cat.split(" ")
            if (len(cols) == len(df.columns)) and (cols != list(df.columns)):
                rename_cols_query = "y"
            else:
                print(
                    f"COLUMNS {len(df.columns) - len(cols)} ENTERED DO NOT MATCH LENGTH OF {len(df.columns)}"
                )
                print(f"THESE ARE NAMES ENTERED PLEASE TRY AGAIN:: {cols}\n")
                rename_cols_query = "test"
        elif "n" in rename_cols_query:
            break
        else:
            print("INVALID INPUT")
            exit_program = input(
                "WOULD YOU LIKE TO EXIT THE PROGRAM, Y/N or Exit\n"
            ).lower()
            if "y" in exit_program or "exit" in exit_program:
                exit()
    p_line()
    return cols, rename_cols_query


#import texthero as hero


def strip_db_space(df):
    remove_white = [preprocessing.fillna                    # , preprocessing.lowercase
                    # , preprocessing.remove_digits
                    # , preprocessing.remove_punctuation
                    # , preprocessing.remove_diacritics
                    # , preprocessing.remove_stopwords
                    , preprocessing.remove_whitespace
                    # , preprocessing.stem
                    ]
    for i in range(len(df.columns)):
        df = hero.clean(df.iloc[:, i], pipeline=remove_white)
    return df


def format_data(df):
    test_cols = get_col_names(df)
    new_cols = test_cols[0]
    # rename_cols_query = test_cols[1]
    insert_first = input(
        "DOES ORIGINAL COLUMN DATA NEED TO BE INSERTED INTO DF? Y/N\n"
    ).lower()
    if "y" in insert_first:
        inserted_first = inserting_first(df, new_cols)
        df = rename_cols(inserted_first, new_cols)
        df = remove_cols(inserted_first)
    else:
        df = rename_cols(df, new_cols)
        df = remove_cols(df)
    # Formatting amount column into floats
    if "amount" in df.columns:
        df = make_num(df, "amount")
    # Formatting date column into datetime obj
    if "date" in df.columns:
        df = convert_date(df)
    return df


def initiate_format(df=0):
    p_line()
    print("FORMATTING CLIPBOARD, EXCEL OR CSV INPUT")
    p_line()
    formatted = format_data(df)
    # Dropping duplicates
    formatted = formatted.drop_duplicates()
    # Sorting cols by date
    # [date_col, 'category', 'identifier', 'amount'])
    date_col = [col for col in list(
        formatted.columns) if "date" in col.lower()]
    # date col is a list won't work in a list requiring a str, need to fix possibly
    formatted = formatted.sort_values(
        by=['date', 'transaction', 'amount']).reset_index(drop=True)
    p_line()
    print("FORMATTED DATAFRAME")
    p_line()
    pp.pprint(formatted.head())
    p_line()
    print("FORMATTING CLIPBOARD OR CSV COMPLETE")
    p_line()
    p_line()
    print('\n\n')
    return formatted


def main():
    t_start = datetime.datetime.now()
    initiate_format()
    t_end = datetime.datetime.now()
    print(f"PROGRAM EXECUTION TIME {t_start-t_end}")


if __name__ == "__main__":
    main()

# data/sample_month.csv
# data/green_may2621_training.csv
# date1, date, transaction, card, amount, balance
# date1, card, balance
