#!/usr/bin/env python3
# coding: utf-8

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

# most of the data I began to work with to generate the working test data
# i had to get from the clipboard on websites
# clipDF = pd.read_clipboard()
# csvName = input('What type of account is it?')
# csvName = csvName + '.csv'
# clipDF.to_csv(csvName, index = False)

# print versions
print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
print('PYTHON VERSIONS')
print('-----------------------------------------')
print("python     : ",  platform.python_version())
print("pandas     : ", pd.__version__)
print("matplotlib : ", matplotlib.__version__)
print("squarify   :  0.4.3")
print('-----------------------------------------\n\n')

def read_csv():
    csvName = input('ENTER CSV NAME\n')
    print('-----------------------------------------')
    if csvName.endswith('.csv'):
        return pd.read_csv(csvName)
    else:
        csvName = csvName + '.csv'
        return pd.read_csv(csvName)

def get_sort_by(df):
    pp.pprint(df.head())
    print('------------------------------------------------------------------------------------------------------')
    print('OPTIONS:::')
    print('------------------------------------------------------------------------------------------------------')
    none_in = [print(list(df.columns)[i].upper(), end =" ") for i in range(len(list(df.columns)))]
    sort_col = input(f'\n\nCHOOSE COLUMN TO SORT BY?:: \n').lower()
    sort = ' '.join(str(elem) for elem in [i for i in df.columns if i == sort_col.lower()])
    return sort

def get_categories():
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    # budget_type = input(
        #     f'What type of purchase is this? Choose From :: \n{" - ".join(categories)}\n')
    defaults = ['food', 'fast_food', 'home_maintenance', 'pets', 'restaurants', 'utilities', 'car_maintenance', 'gas', 'medical', 'entertainment', 'family']
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


def add_trans_type(df, i, sort_by=0):
    ####################################################get_sort_by####################################################
    if sort_by:
        purchase_type = df[sort_by][i].split()
        print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
        for index in range(len(purchase_type)):
            key = input(
                f'SORT THIS PURCHASE BY:: {purchase_type[index]}, Y/N\n')
            if 'y' in key:
                print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
                print(
                    f'YOU WILL SORT THIS TRANS BY COLUMN:: {str(sort_by)} DATA::{purchase_type[index]}\n')
                return sort_by, purchase_type[index]
            else:
                print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
                print('CHOOSE AGAIN')
                continue

def make_dict(categories):
    trans_type = {}
    for i in categories:
        trans_type[i] = []
    return trans_type


def add_data(budget_dict, data):
    #print(f'CATEGORIES:: {list(budget_dict.keys())}')
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    location = str(input(
        f'\nCHOOSE CATEGORY FOR::: "{data[1]}"\n------------------------------------------------------\nCATEGORY OPTIONS:: \n\n{" - ".join(list(budget_dict.keys()))}\n------------------------------------------------------\n'))
    if location not in budget_dict.keys():
        add_key = input(f'{location}:: NOT IN BUDGET FILE, WOULD YOU LIKE TO ADD IT? Y/N\n')
        if 'y' in add_key:
            budget_dict[location] = []
    for key, value in budget_dict.items():
        if location == key:
            value.append(data)
            print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
            print('ADDITION SUCCESSFUL')
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
    if type(budget_dict) == type({}):
        categories = budget_dict.keys()
        trans_type = budget_dict
        pp.pprint(df)
        sort_by = get_sort_by(df)

    else:
        ######################################### get_categories ##############################################
        categories = get_categories()
        no_of_dicts = len(categories)
        ############################################## make_dict ##############################################
        trans_type = make_dict(categories)
        sort_by = get_sort_by(df)
        
    #organize_by = str(input('Which column do you want to categorize data by\n'))
    
    cols = input('COLUMNS TO KEEP::\n')
    #cols = cols.split()
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


    for i in range(len(df)):  # range(len(df)):
        ##############################################add_trans_type ###############################################
        get_col = add_trans_type(df, i, sort_by)
        #print(f'GET COl {get_col}')
        organize_by = get_col[0]
        identity = get_col[1]
        data_to_sort = df.iloc[i][organize_by]
        # PRINT TESTING STATMENTS
        # print(f'SORTING BY:: "{sort_by.upper()}" COLUMN')
        # print(f'IDENTIFIER IS:: {identity}')
        # print(f'COL NAME IS:: {organize_by}')
        # print(f'CATEGORIZE DATA:: {data_to_sort}\n')
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

#sample dictionary
# budget_type: [date, identifier, data, amount]
dictionary = {
    'home': [
    ['01/24/21', 'HOME_DEPOT',  -57],
    ['01/12/21', 'LOWES', -100],
    ['02/14/21', 'TRUE_VALUE', -60]],
    'fast_food': [
    ['01/28/21', 'CHICK-FIL-A', -14.99]],
    'food':[
    ['02/21/21', 'HARRIS_TEETER', -250],
    ['03/15/21', 'FARM_FRESH', -150]]
}
# print('TESTING FOR DATA WITHIN DICTIONARY')
# z = search_dict(trans_type, ['01/14/21', 'HOME_DEPOT', -100], 'HOME_DEPOT')


# WORKING< 
# Exception Program is not matching Data within Dictionary and adding without asking
csv = read_csv()
#print(csv.columns)
for i in csv.columns:
    csv = csv.rename(columns={i:i.lower()})
pp.pprint(csv.head())
pp.pprint(split_purchases(csv.head()))
#pp.pprint(split_purchases(ninety_days.head(), dictionary))

if __name__ == "__main__":
    main()