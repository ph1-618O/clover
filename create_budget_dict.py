#!/usr/bin/env python3
# coding: utf-8

# Create budget dict. py takes a given csv and sorts the data from the csv
# into a dictionary with a budget category as the key
# it also asks the user what are the necessary columns for their budget
# once the program begins it passes a unique identifier to each row entry
# this unique identifier is also stored at the end of the dictionary of lists
# so that once it is within the dictionary the program will recognize
# all future occurrences of identifier and add it without input

from fastnumbers import fast_float
import plotly.graph_objects as go
import squarify
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib
import pprint
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
pp = pprint.PrettyPrinter(indent=4)

# graphing

# Dealing with number input inconsistencies, avoids VALUE ERROR, ATTRIBUTE ERROR

pd.set_option("display.max_rows", None, "display.max_columns", None)


# Need to add in portion from other notebook that asked user if they want to install these dependencies if they are not included
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

# most of the data I began to work with to generate the working test data
# i had to get from the clipboard on websites


def read_clip():
    clipDF = pd.read_clipboard()
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    csvName = input('WHAT TYPE OF ACCOUNT FOR FILENAME?\n')
    csvName = csvName + '.csv'
    clipDF.to_csv(csvName, index=False)
    return pd.read_csv(csvName)


def reading_clipboard():
    clipDF = pd.read_clipboard()
    csvName = input('What type of account is it?')
    csvName = csvName + '.csv'
    clipDF.to_csv(csvName, index=False)


def read_csv():
    csvName = input('ENTER CSV LOCATION\\NAME\n')
    print('-----------------------------------------')
    if csvName.endswith('.csv'):
        return pd.read_csv(csvName)
    else:
        csvName = csvName + '.csv'
        return pd.read_csv(csvName)


def save_csv(df):
    save_csv = input('SAVE NEW DATAFRAME TO CSV? Y/N\n')
    if 'y' in save_csv.lower():
        csvName = input('ENTER NEW CSV LOCATION\\NAME\n')
        accept_name = input(
                        f'IS THIS THE CORRECT LOCATION\\FILENAME {csvName} Y\\N\n')
        while 'y' not in accept_name.lower(): 
            if csvName[:-4] == '.csv':
                accept_name = input(
                        f'IS THIS THE CORRECT LOCATION\\FILENAME {csvName} Y\\N\n')
            else:
                accept_name = input(
                        f'IS THIS THE CORRECT LOCATION\\FILENAME {csvName + ".csv"} Y\\N\n')       
                csvName = csvName + '.csv'
            accept_name = input('WOULD YOU LIKE TO EXIT THE PROGRAM? Y\\N').lower()
    df.to_csv(csvName, index=False)
    print('DATA SUCCESSFULLY STORED TO CSV\n')

# OLD
# def save_csv(df):
#     save_csv = input('SAVE NEW DATAFRAME TO CSV? Y/N\n')
#     if 'y' in save_csv.lower():
#         csvName = input('ENTER NEW CSV NAME\n')
#         csvName = csvName + '.csv'
#         df.to_csv(csvName, index=False)
#         print('DATA SUCCESSFULLY STORED TO CSV\n')


def get_sort_by(df, sort_query):
    pp.pprint(df.head())
    print('------------------------------------------------------------------------------------------------------')
    print('OPTIONS:::')
    print('------------------------------------------------------------------------------------------------------')
    #none_in = [print(list(df.columns)[i].upper(), end =" ") for i in range(len(list(df.columns)))]
    sort_col = input(
        f'\n\nCHOOSE COLUMN TO SORT {sort_query} BY?:: \n').lower()
    sort = ' '.join(str(elem)
                    for elem in [i for i in df.columns if i == sort_col.lower()])
    return sort


def get_categories():
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    defaults = ['food', 'fast_food', 'home', 'pets', 'restaurants', 'utilities',
                'car', 'gas', 'medical', 'fun', 'family', 'deposits', 'interest']
    print(f'\nDEFAULT CATEGORIES::: \n{" - ".join(defaults)}\n')
    use_defaults = input('USE DEFAULTS::: Y/N\n')
    if 'y' in use_defaults:
        categories = defaults
    else:
        categories = input(
            'ENTER BUDGET CATEGORIES? USE UNDERSCORES:::\n')
    cat = ''
    if type(categories) == type('s'):
        for i in categories:
            if ',' in categories:
                cat += i.strip(',')
            else:
                cat += i
        categories = cat.split(' ')
    return categories

# ADD EXIT QUERY FOR LOOP


def add_trans_type(df, i, sort_by=0):
    ####################################################get_sort_by####################################################
    if sort_by:
        purchase_type = df[sort_by][i].split()
        print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
        key = ''
        while 'y' not in key.lower():
            for index in range(len(purchase_type)):
                key = input(
                    f'SORT THIS PURCHASE BY:: {purchase_type[index]}, Y/N\n')
                if 'y' in key:
                    print(
                        '//////////////////////////////////////////////////////////////////////////////////////////////////////')
                    print(
                        f'YOU WILL SORT THIS TRANS BY COLUMN:: {str(sort_by)} DATA::{purchase_type[index]}\n')
                    return sort_by, purchase_type[index]
                else:
                    print(
                        '//////////////////////////////////////////////////////////////////////////////////////////////////////')
                    print('YOU MUST ENTER YES OR NO')
                    print('CHOOSE AGAIN')
                    continue
            key = input('WOULD YOU LIKE TO EXIT THIS PROGRAM? Y/N\n')


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


def make_dict(categories):
    trans_type = {'0_format': [
        'date', 'transaction', 'amount', 'identifier']}
    for i in categories:
        trans_type[i] = []
    return trans_type


# Need to format location input into a prettier line of code
def add_data(budget_dict, data):
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    location = str(input(
        f'\nCHOOSE CATEGORY FOR::: "{data[1]}"\n------------------------------------------------------\nCATEGORY OPTIONS:: \n\n{" - ".join(list(budget_dict.keys()))}\n------------------------------------------------------\n'))

    # Adding a new key if the entered key is not already in the dictionary or part of defaults
    # budget_dict.keys():
    #print([i[:3] for i in budget_dict.keys()])
    if location[:3] not in [i[:3] for i in budget_dict.keys()]:
        add_key = input(
            f'"{location}":: NOT IN BUDGET FILE, WOULD YOU LIKE TO ADD IT? Y/N\n')
        if 'y' in add_key:
            budget_dict[location] = []
            print(f'ADDITION TO "{location.upper()}" SUCCESSFUL\n')

    # Matching the location input for the item to corresponding key
    for key, value in budget_dict.items():
        if location[:3] == key[:3]:
            value.append(data)
            print('//////////////////////////////////////////////////////////////////////////////////////////////////////\n')
            print(f'YOU ENTERED "{location}" WE ARE MATCHING TO "{key.upper()}"')
            print(f'ADDITION TO "{key.upper()}" SUCCESSFUL\n')
            time.sleep(2)
    return budget_dict


# WORKING
# Need to clean up add_Data and search_dict

def search_dict(budget_dict, data):  # location is column name
    data_point = data[-1]
    for key, value in budget_dict.items():
        for i in value:
            if data_point in i:
                print(
                    '//////////////////////////////////////////////////////////////////////////////////////////////////////')
                print(f'DATA POINT IDENTIFIED')
                print(f'ADDING TO CATEGORY "{key}"')
                value.append(data)
                time.sleep(1)
                return budget_dict
            else:
                pass
    ######################################### add_data ##########################################################
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    print('RUNNING ADD DATA')
    time.sleep(1)
    budget_dict = add_data(budget_dict, data)
    return budget_dict


# NEED TO ADD TRY/ACCEPT STATEMENTS for ALL_INPUTS

# pull out each location of purchase and split into keys based on user input
# Home, Food, Fast_Food, Clothing, Car, Utilities, Entertainment


def split_purchases(df, budget_dict=0):
    print('BEGIN PURCHASE CATEGORIZATION')
    print('------------------------------------------------------------------------------------------------------')
    print('------------------------------------------------------------------------------------------------------')
# if statement separates data if a correctly formatted dictionary is passed to it
# else it creates a dictionary
    if type(budget_dict) == type({}):
        categories = budget_dict.keys()
        trans_type = budget_dict
        pp.pprint(df)
        sort_by = get_sort_by(df, 'CATEGORY DATA')

    else:
        ######################################### get_categories ##############################################
        categories = get_categories()
        ############################################## make_dict ##############################################
        trans_type = make_dict(categories)
        ############################################## get_sort_by ##############################################
        sort_by = get_sort_by(df, 'CATEGORY DATA')


# this block asks the reader what columns to keep within the list of data
# Need to add functionality that allows for spaces, and the word and and splits on spaces
# Add a loop that asks again and again until user enters the correct input or asks to exit
# This block is already in format_data.py, maybe add an if statement or run this portion if the chosen
# option is CSV instead of clipboard data(bc clipboard data gets run thru format_data.py)
    cols = input('COLUMNS TO KEEP::\n')
    cat = ''
    for k in cols:
        if ',' in cols:
            cat += k.strip(',')
        else:
            cat += k
    cols = cat.split(' ')
    for c in cols:
        try:
            df[c.lower()]
        except KeyError:
            print('ERROR, RE-ENTER COLUMN\n')

    for i in range(len(df)):
        ##############################################add_trans_type ###############################################
        get_col = add_trans_type(df, i, sort_by)
        organize_by = get_col[0]
        identity = get_col[1]
        data_to_sort = df.iloc[i][organize_by]
    # PRINT TESTING STATEMENTS
        print(f'SORTING BY:: "{sort_by.upper()}" COLUMN')
        print(f'IDENTIFIER IS:: {identity}')
        print(f'COL NAME IS:: {organize_by}')
        print(f'CATEGORIZE DATA:: {data_to_sort}\n')
        ############################################## search_dict ##############################################
        data = []
        for col in cols:
            data.append(df.iloc[i][col])
        data.append(identity)
        new_dict = search_dict(trans_type, data)
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    print('PROGRAM COMPLETE')
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    return new_dict


def dict_to_Frame(data_dict):
    skip_list = []
    li = []
    for key, value in data_dict.items():
        # Skipping the first entry which is the columns
        if key == '0_format':
            continue
        elif len(value) == 0:
            skip_list.append(key)
        else:
            # print(f'{value}')
            db = pd.DataFrame()
            for i in range(len(value)):
                li.append(value[i]+[key])
    cols = data_dict['0_format'] + ['category']
    df = pd.DataFrame(np.array(li), columns=cols)
    print((f'{skip_list} = NO AVAILABLE DATA, SKIPPING'))
    return df

# Adding PYMONGO DB functionality
# Need to add a print statement, also pymongo install based on the users OS
# For consistent use of program need to add searchability that the db connection only adds if the data is new

# Notes https://docs.mongodb.com/manual/reference/method/db.collection.find/
# https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/


def conn_mongo(data):
    import pymongo
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.clover
    if db.budgetDB.drop():
        print('MAKING NEW DATABASE')
    else:
        print('DB NOT PRESENT')
    db.show
    db.budgetDB.insert_one(data)

    # Hopefully printing the first 5 entries in the db
    # pprint(db.budgetDB.find_one())
    # db.budgetDB.find().pretty()


def main():
    # WORKING<
    # change csv variable to data
    # add loop that continues until a yes or no is given or an exit request

    csv_or_clip = input('DATA IS CSV OR CLIPBOARD INPUT?\n').lower()
    if 'csv' in csv_or_clip:
        # Normalizing the column names to lower
        data = read_csv()
        for i in data.columns:
            data = data.rename(columns={i: i.lower()})
        print('IMPORTED DATASET\n')
        print('------------------------------------------------------------------------------------------------------')
        pp.pprint(data.head())
        print('------------------------------------------------------------------------------------------------------')

    elif 'clip' in csv_or_clip:
        format_q = ('FORMAT CLIP BOARD DATA? Y/N').lower()
        if 'y' in format_q.lower():
            # Fix Module import statement
            print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
            print('RUNNING FORMAT_DATA PROGRAM')
            import format_data
            data = read_clip()
            data = format_data.initiate_format(data)
            for i in data.columns:
                data = data.rename(columns={i: i.lower()})
            print('IMPORTED DATASET\n')
            print('------------------------------------------------------------------------------------------------------')
            pp.pprint(data.head())
            # pp.pprint(data.head())
            # print('------------------------------------------------------------------------------------------------------')
    else:
        print('INVALID INPUT, PLEASE TRY AGAIN')
        exit()
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    print('RUNNING SPLIT PURCHASES PROGRAM')
    print('------------------------------------------------------------------------------------------------------')
    trans_dict = split_purchases(data)

    # Need to add dictionary to DB functionality, right now won't work because there are empty categories, and unequal values in columns
    converted_DF = dict_to_Frame(trans_dict)
    print('Please enter the row that has the date\n')
    pp.pprint(trans_dict)
    print('------------------------------------------------------------------------------------------------------')
    sort_by = get_sort_by(converted_DF, 'DATE')
    converted_DF = converted_DF.sort_values(by=sort_by)
    print('Please enter the row that has the amounts\n')
    sort_by = get_sort_by(converted_DF, 'AMOUNTS')
    converted_DF = make_num(converted_DF, sort_by)
    pp.pprint(converted_DF)
    create_database = input('ADD TO DATABASE? Y/N \n')
    if 'y' in create_database:
        conn_mongo(trans_dict)
        print('MongoDB Successful')
    save_csv(converted_DF)
    return data, converted_DF

    #pp.pprint(pd.DataFrame.from_dict(data, orient='index', columns = data.keys()))


if __name__ == "__main__":
    main()

# Create test case.py that uses this dictionary and the sample dataframe
#  sample dictionary for testing
# budget_type: [date, data, amount, identifier]
dictionary = {
    'format': ['date', 'location data', 'float amount', 'identifier'],
    'home': [
        ['01/24/21', 'HOME_DEPOT',  -57, 'HOME'],
        ['01/12/21', 'LOWES', -100, 'LOWES'],
        ['02/14/21', 'TRUE_VALUE', -60, 'TRUE']],

    'fast_food': [
        ['01/28/21', 'CHICK-FIL-A', -14.99, 'CHICK-FIL-A']],

    'food': [
        ['01/22/21', 'FOOD LION',  -200, 'FOOD LION'],
        ['02/21/21', 'HARRIS_TEETER', -250, 'HARRIS'],
        ['03/15/21', 'FARM_FRESH', -150, 'FRESH']]
}
