#!/usr/bin/env python3
# coding: utf-8

# Budget.py takes a given csv, clipboard copy from a table, or excel file and sorts the data
# into a dictionary with a budget category as the key
# it also asks the user what are the necessary columns for their budget
# once the program begins it passes a unique identifier to each row entry
# this unique identifier is also stored at the end of the dictionary of lists
# so that once it is within the dictionary the program will recognize
# all future occurrences of identifier and add it without input
# Why clipboard data?? :: most of the data I began to work with to generate the working test data
# was acquired from the clipboard on websites


## <<<<<<<<WORKING>>>>>>>>>>>
# Clean up import statements
# Think about separating functions into different .py files based on function
# Watch the order!! 

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

# # for importing from excel to pandas
# from pandas import ExcelWriter
# from pandas import ExcelFile
import re
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None
pp = pprint.PrettyPrinter(indent=4)

# graphing

## <<<<<<<<WORKING>>>>>>>>>>>
# Add unit tests and tests dealing with number input inconsistencies, avoids VALUE ERROR, ATTRIBUTE ERROR
# Use Try, Except and Assert

pd.set_option("display.max_rows", None, "display.max_columns", None)

## <<<<<<<<WORKING>>>>>>>>>>>
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


def read_data(file_type): 
    data_file = input(f'ENTER "{file_type.upper()}" LOCATION\\NAME\n')
    if 'csv' in file_type.lower():
        if data_file.endswith('.csv'):
            return pd.read_csv(data_file)
        else:
            return pd.read_csv(data_file + '.csv')
    elif data_file.endswith('.xls') or data_file.endswith('.xlsx'):
        return pd.read_excel(data_file)
    elif 'xls' in file_type.lower() or 'excel' in file_type.lower():
        print('\nERROR::: FILE EXTENSION OMITTED PLEASE RE-ENTER, XLS or XLSX\n')
        e_type = input('ENTER XLS OR XLSX\n')
        if 'xlsx' in e_type:
            return pd.read_excel(data_file + '.xlsx')
        elif 'xls' in e_type.lower():
            return pd.read_excel(data_file + '.xls')
    else: 
        print('INVALID INPUT, EXITING PLEASE TRY AGAIN')
        exit()

def get_data_type():
    import_data = input('DATA IS EXCEL FILE, CSV OR CLIPBOARD INPUT?\n').lower()
    query_format = input('IS DATA PROPERLY FORMATTED WITH COLUMNS? Y/N\n')
    formatted = None

    if ('csv' in import_data.lower() and 'y' in query_format.lower()) or ('csv' in import_data.lower() and 'n' in query_format.lower()):
        # Normalizing the column names to lower
        data = read_data('csv')
        for i in data.columns:
            data = data.rename(columns={i: i.lower()})
        print('------------------------------------------------------------------------------------------------------')
        print('CHECKING COLUMNS')
        import format_data
        check_cols = format_data.get_col_names(data)
        data = check_cols[1]
        print(f'\n"{import_data.upper()}" DATASET, ...IMPORT SUCCESS\n')
        print('DATASET SAMPLE')
        print('------------------------------------------------------------------------------------------------------')
        pp.pprint(data.head())
        print('------------------------------------------------------------------------------------------------------\n\n')
        formatted = 'formatted'

    elif 'clip' in import_data.lower() or 'format' in query_format.lower()  or 'n' in query_format.lower():
        format_q = (f'FORMAT "{import_data.upper()}" DATA? Y/N').lower()
        if 'n' in format_q.lower():
            ## <<<<<<<<WORKING>>>>>>>>>>>
            # Fix Module import statement
            print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
            print('RUNNING FORMAT_DATA PROGRAM')
            import format_data
            if 'clip' in import_data.lower():
                data = import_clip()
                data = format_data.initiate_format(data)
                for i in data.columns:
                    data = data.rename(columns={i: i.lower()})
                print(f'\n"{import_data.upper()}" DATASET...IMPORT SUCCESS\n')
                print('DATASET')
                print('------------------------------------------------------------------------------------------------------')
                pp.pprint(data.head())
                formatted = 'formatted'
                # print('------------------------------------------------------------------------------------------------------')
            elif 'format' in query_format.lower() or 'n' in query_format.lower():
                data = read_data('csv')
                data = format_data.initiate_format(data)
                for i in data.columns:
                    data = data.rename(columns={i: i.lower()})
                print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
                print(f'"{import_data.upper()}" FORMATED DATASET, ...IMPORT SUCCESS\n RETURNING TO CREATE_BUDGET_DICT')
                print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
                print('DATASET')
                print('------------------------------------------------------------------------------------------------------')
                pp.pprint(data.head())
                print('------------------------------------------------------------------------------------------------------\n\n')
                formatted = 'formatted'
            formatted = 'formatted'
        
    elif 'excel' in import_data or 'xls' in import_data:
        data = read_data('excel')
        for i in data.columns:
            data = data.rename(columns={i: i.lower()})
        import format_data
        check_cols = format_data.get_col_names(data)
        data = check_cols[2]
        formatted = 'formatted'
        print(f'\n"{import_data.upper()}" DATASET...IMPORT SUCCESS\n')
        print('DATASET')
        print('------------------------------------------------------------------------------------------------------')
        pp.pprint(data.head())
        print('------------------------------------------------------------------------------------------------------')
    
    else:
        print('INVALID INPUT, PLEASE TRY AGAIN')
        exit()
    return data, formatted


def import_clip():
    clipDF = pd.read_clipboard()
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    csvName = input('WHAT TYPE OF ACCOUNT FOR FILENAME?\n')
    csvName = csvName + '.csv'
    clipDF.to_csv(csvName, index=False)
    return pd.read_csv(csvName)


## <<<<<<<<WORKING>>>>>>>>>>>
##  Redundant, kept if needed to add more than one csv file in the future?
# def import_csv():
#     csvName = input('ENTER CSV LOCATION\\NAME\n')
#     print('------------------------------------------------------------------------------------------------------')
#     if csvName.endswith('.csv'):
#         return pd.read_csv(csvName)
#     else:
#         csvName = csvName + '.csv'
#         return pd.read_csv(csvName)




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
    else:
        print('EXITING')
        #exit()

def import_excel(path):
    sheet_or_file = input('IS YOUR EXCEL FILE ON A SHEET? Y/N\n')
    if 'n' in sheet_or_file.lower():
        df = pd.read_excel(fr'{path}')
    elif 'y' in sheet_or_file.lower() or 'sheet' in sheet_or_file.lower():
        xls_sheet = input('WHAT IS THE SHEETS NAME?\n')
        df = pd.read_excel(fr'{path}', sheet_name=xls_sheet)
    else:
        print('INVALID INPUT EXITING PLEASE TRY AGAIN\n')
        exit()
    return df

# <<<<<<<<WORKING>>>>>>>>>>>
# figure out if these comments are useful
def get_sort_by(df, sort_query):
    print('------------------------------------------------------------------------------------------------------')
    print('DATAFRAME')
    print('------------------------------------------------------------------------------------------------------')
    pp.pprint(df.head())

    print('------------------------------------------------------------------------------------------------------')
    print(f'SORTING BY "{sort_query.upper()}"')
    print('------------------------------------------------------------------------------------------------------')
    if sort_query != 'CATEGORY DATA':
        print(f'OPTIONS::: {" - ".join(list(df.columns))}')
        print('------------------------------------------------------------------------------------------------------')

    sort_col = constrain_input_loop(sort_query, list(df.columns))
    sort = ' '.join(str(elem)
                    for elem in [i for i in df.columns if i == sort_col.lower()])
    return sort


def get_categories(categories = 0):
    # look at jupyter notebook with purchases categorized as essential, non essential, fixed, variable, one-time and reoccuring
    # add these into the make dict with new sub categories
    defaults = sorted(['groceries', 'take_away', 'home', 'pet', 'restaurant', 'utility',
                'transportation', 'gas', 'medical', 'entertainment', 'deposit', 'interest', 'savings', 'debt', 'income'])
    if  categories:
        if type(categories) == type([]):
            if len(categories) < len(defaults + ['0_format']):
                #Trying to skip printing out 0_format, needs better code
                categories_list = " - ".join(sorted(categories)[1:])
                c_len = len(categories_list)
                if '0_format' in categories:
                    print(f'CURRENT CATEGORIES::: {categories_list[:int(c_len/2)]}\n{categories_list[int(c_len/2):]}\n------------------------------------------------------------------------------------------------------')
                else:
                    print(f'CURRENT CATEGORIES::: {categories_list[:int(c_len/2)]}\n{categories_list[int(c_len/2):]}\n------------------------------------------------------------------------------------------------------')
                add_defaults = []
                for i in defaults:
                    if i not in categories:
                        add_defaults.append(i)
                #{" - ".join(categories)}
                d_list = " - ".join([i.lower() for i in add_defaults])
                d_len = len(d_list)
                print(f'DEFAULTS NOT IN CURRENT CATEGORIES:::\n "{d_list[:int(d_len/2)]}\n{d_list[int(d_len/2):]}"\n------------------------------------------------------------------------------------------------------')
                confirm_addition = input('ADD EXTRA DEFAULTS TO CATEGORIES Y/N\n')
                if 'y' in confirm_addition.lower():
                    for i in add_defaults:
                        categories.append(i)
                    categories = sorted(categories)
    else:
        print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
        d_list2 = " - ".join(defaults)
        d_len2 = len(d_list2)
        print(f'DEFAULT CATEGORIES::: \n------------------------------------------------------------------------------------------------------\n{d_list2[:int(d_len2/2)]}\n{d_list2[int(d_len2/2):]}\n------------------------------------------------------------------------------------------------------')
        use_defaults = input('USE DEFAULTS::: Y/N\n')
        if 'y' in use_defaults:
            categories = defaults
        else:
            categories = input(
                'ENTER BUDGET CATEGORIES:::\n')
        cat = ''
        if type(categories) == type('s'):
            #need to add regex to sub a space between words with an underscore but before a comma
            if ',' in categories:
                categories = [i.strip().replace(' ', '_') for i in categories.split(',')]
            else:
                categories = sorted(categories.split())
# <<<<<<<<WORKING>>>>>>>>>>>
# Add a section that if you ask the user to continue and there is any other value than y
# print out the list with index numbers, ask which number is wrong 
# add a loop to make sure you fix all the type errors
    if categories[0].lower() == '0_format':
        print('------------------------------------------------------------------------------------------------------')
        cat_list2 = " - ".join([str(x) for x in [*categories[1:]]])
        c_len2 = len(cat_list2)
        print(f'CATEGORIES ARE::: "{cat_list2[:int(c_len2/2)]}\n{cat_list2[int(c_len2/2):]}"')
        print('------------------------------------------------------------------------------------------------------\n')
        print('//////////////////////////////////////////////////////////////////////////////////////////////////////\n')
    else:
        print('------------------------------------------------------------------------------------------------------')
        cat_list3 = " - ".join([str(x) for x in [*categories]])
        c_len3 = len(cat_list3)
        print(f'CATEGORIES ARE:::\n"{cat_list3[:int(c_len3/2)]}\n{cat_list3[int(c_len3/2):]}"')
        #print(f'CATEGORIES ARE::: "{" - ".join([str(x) for x in [*categories]])}"')
        print('------------------------------------------------------------------------------------------------------\n')
        print('//////////////////////////////////////////////////////////////////////////////////////////////////////\n')
    return categories

# <<<<<<<<WORKING>>>>>>>>>>>
# ADD EXIT QUERY FOR LOOP

def constrain_input_loop(sort_query, list_options):
    if sort_query == 'CATEGORY DATA' and 'transaction' in list_options:
        return 'transaction'
    elif sort_query.lower() == 'date' and 'date' in list_options:
        return 'date'
    elif sort_query.lower() == 'amount' and ('amount' in list_options or 'float amount' in list_options):
        return 'amount'
    else:
        correct = ''
        while 'y' not in correct.lower():
            for index in range(len(list_options)):
                correct = input(
                    f'SORT THIS {sort_query} BY:: "{list_options[index].upper()}", Y/N OR EXIT\n')
                if 'y' in correct.lower():
                    print(
                        '//////////////////////////////////////////////////////////////////////////////////////////////////////')
                    print(
                        f'YOU WILL SORT THIS "{sort_query}" BY::"{list_options[index].upper()}"\n')
                    return list_options[index]
                elif 'n' in correct.lower():
                    print(f'"{correct.upper()}" ENTERED, PLEASE CHOOSE AGAIN')
                    continue
                else:
                    print('YOU MUST ENTER YES OR NO')
                    exit = input('WOULD YOU LIKE TO EXIT THIS PROGRAM? Y/N\n')
                    if 'y' in exit.lower():
                        print("EXITING")
                        exit()
                # <<<<<<<<WORKING>>>>>>>>>>>
                # why is error thrown when exit == 'y' ??


def add_transaction_type(df, i, sort_by=0):
    ####################################################get_sort_by####################################################
    if sort_by:
        purchase_type = df[sort_by][i].replace('*', ' ').split()
        print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
        for index in range(len(purchase_type)):
            print(f'TESTING IDENTIFIER:: "{purchase_type[index]}", Y/N\n')
            print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
            print(f'SORTING TRANSACTION:: "{str(sort_by).upper()}" BY IDENTIFIER::{purchase_type[index].upper()}')
            return sort_by, purchase_type[index].lower()


def add_trans_type_confirm(df, i, sort_by=0):
    ####################################################get_sort_by####################################################
    if sort_by:
        purchase_type = df[sort_by][i].replace('*', ' ').split()
        print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
        key = ''
        while 'y' not in key.lower():
            for index in range(len(purchase_type)):
                key = input(
                    f'SORT THIS PURCHASE BY:: "{purchase_type[index]}", Y/N\n')
                if 'y' in key:
                    print(
                        '//////////////////////////////////////////////////////////////////////////////////////////////////////')
                    print(
                        f'SORTING TRANSACTION:: "{str(sort_by).upper()}" BY IDENTIFIER::{purchase_type[index].upper()}')
                    return sort_by, purchase_type[index].lower()
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


def make_dict(categories, old_dict=0):
    # <<<<<<<<WORKING>>>>>>>>>>>
    # look at jupyter notebook with purchases categorized as essential, non essential, fixed, variable, one-time and reoccuring
    # add these into the make dict with new sub categories
    if type(old_dict) == type({}):
        #print('DICT CONFIRMED')
        if '0_format' not in old_dict.keys():
            #print('0_FORMAT NOT IN DICTIONARY ADDING\n')
            old_dict['0_format'] = ['date', 'transaction', 'float amount', 'identifier']
        for i in categories:
            if i not in old_dict.keys():
                old_dict[i] = []
        trans_type = old_dict

    else:
        trans_type = {'0_format': [
        'date', 'transaction', 'float amount', 'identifier']}
        for i in categories:
            trans_type[i] = []
    return trans_type

# <<<<<<<<WORKING>>>>>>>>>>>
# Need to format location input into a prettier line of code
# def add_data2(budget_dict, data):
#     print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
#     print('RUNNING ADD DATA')
#     print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
#     cat_options2 = " - ".join(sorted(list(budget_dict.keys()))[1:])
#     len_cat = int(len(cat_options2)/2)
#     location = str(input(
#         f'\nCHOOSE CATEGORY FOR::: "{data}"\n------------------------------------------------------------------------------------------------------\nCATEGORY OPTIONS:: {cat_options2[:len_cat]}\n{cat_options2[len_cat:]}\n------------------------------------------------------------------------------------------------------\n'))
#     # Adding a new key if the entered key is not already in the dictionary or part of defaults
#     if location[:3] not in [i[:3] for i in budget_dict.keys()]:
#         add_key = input(
#             f'"{location}":: NOT IN BUDGET FILE, WOULD YOU LIKE TO ADD IT? Y/N\n')
#         if 'y' in add_key:
#             budget_dict[location] = []
#             print(f'ADDITION TO "{location.upper()}" SUCCESSFUL')

    # # Matching the location input for the item to corresponding key
    # for key, value in budget_dict.items():
    #     if location[:3] == key[:3]:
    #         print(f'YOU ENTERED "{location.upper()}" WE ARE MATCHING TO "{key.upper()}"')
    #         if type(data[0]) != type([]):
    #             value.append(data+[key])
    #             print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    #             print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
    #             return budget_dict
    #         elif type(data[0]) == type([]) and len(data) > 1:
    #             for z in data:
    #                 z.append(key)
    #                 value.append(z)
    #             print('//////////////////////////////////////////////////////////////////////////////////////////////////////\n')
    #             print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
    #             return budget_dict
    #         else:
    #             print('ERROR SKIPPING')
    # return budget_dict


# <<<<<<<<WORKING>>>>>>>>>>>
# Need to clean up add_Data and search_dict
def search_dict(budget_dict, data, data_point):  # location is column name
    print(f'SEARCHING DICT FOR {data_point.upper()}')
    for key, value in budget_dict.items():
        # skip keys that are empty
        if value and len(value) > 0:
            for i in value:
                if i and len(i) > 0:
                    for j in i:
                        if re.search(rf'{data_point}', str(j), re.IGNORECASE) != None:
                                print(
                                    '//////////////////////////////////////////////////////////////////////////////////////////////////////')
                                print(f'DATA POINT IDENTIFIED')
                                print(f'ADDING TO CATEGORY "{key.upper()}"')
                                for x in data:
                                    if type(x) == type([]) and len(data) == 1:
                                        return budget_dict, 'identified'
                                    elif type(x) == type([]) and len(data) > 1:
                                        value.append(x + [key])
                                    else:
                                        value.append(data + [key])
                                        return budget_dict, 'identified'
                                return budget_dict, 'identified'
                        else:
                            pass              
    return budget_dict, 'unknown'



# <<<<<<<<WORKING>>>>>>>>>>>
# NEED TO ADD TRY/ACCEPT STATEMENTS for ALL_INPUTS

def confirm_cols(df, formatted_df=0):
    if formatted_df:
        return list(df.columns)
    else:
        keep_cols = input('KEEP COLUMN NAMES? Y/N\n')
        if 'n' in keep_cols:
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
        else:
            cols = df.columns
    return cols


# def search_all(df, row_num, sort_by, trans_split):
#     print('------------------------------------------------------------------------------------------------------')
#     print(f'SEARCHING ALL "{sort_by.upper()}" STRING FOR IDENTIFIERS')
#     print(trans_split)
#     counter = 0
#     while counter < len(purchase_types):
#         counter += 1
#         return purchase_types[counter].lower(), 'searching'
#     return 'match'

# def search_row2(cols, df, row, sort_by, skip_rows, match_status):
#         if match_status == 'searching':
#             row_split = df[sort_by][row].replace('*', ' ').split()
#             counter = 0
#             while counter < len(row_split):
#                 identity = row_split[counter]
#                 mask = df.apply(lambda x: x.str.contains(rf'{identity}', na=False, case=False))
#                 matching_rows = df.loc[mask.any(axis=1)]
#                 skip_rows += matching_rows.index.tolist()

#                 if len(matching_rows) >= 2:
#                     print(f'{len(matching_rows)} ROWS MATCHED IN IMPORTED DATA:::')
#                     data = []
#                     for rows in matching_rows.index.tolist():
#                         data.append(list(df.iloc[rows])+[identity])
#                     counter += 1
#                 else:
#                     data = []
#                     print('NO MATCH IN IMPORTED DATA:::')
#                     counter += 1
#                     continue
#                 #counter += 1
#             match_status = 'not_found'

#         #identity = search_all(df, row, sort_by, row_split)
#         ## get_col used if search_all fails
#         else:
#             get_id = add_transaction_type(df, row, sort_by)
#             identity = get_id[1]
#             mask = df.apply(lambda x: x.str.contains(rf'{identity}', na=False, case=False))
#             matching_rows = df.loc[mask.any(axis=1)]
#             skip_rows += matching_rows.index.tolist()

#             if len(matching_rows) >= 2:
#                 print(f'{len(matching_rows)} ROWS MATCHED IN IMPORTED DATA:::')
#                 data = []
#                 for rows in matching_rows.index.tolist():
#                     data.append(list(df.iloc[rows])+[identity])
#             else:
#                 data = []
#                 print('NO MATCH IN IMPORTED DATA:::')
#                 for col in cols:
#                         data.append(df.iloc[row][col])
#                 data.append(identity)
#         return data, identity, skip_rows  

# def split_purchases2(df, formatted_df=0, budget_dict=0):
#     cols = confirm_cols(df, formatted_df)
#     #pp.pprint(df)
#     print('BEGIN PURCHASE CATEGORIZATION')
#     print('------------------------------------------------------------------------------------------------------')
# # if statement separates data if a correctly formatted dictionary is passed to it
# # else it creates a dictionary
#     if type(budget_dict) == type({}):
#         ######################################### get_categories ##############################################
#         categories = get_categories(list(budget_dict.keys()))
#         ######################################### make_dict ##############################################
#         trans_type = make_dict(categories, budget_dict)
#         ######################################### get_sort_by ##############################################
#         sort_by = get_sort_by(df, 'CATEGORY DATA')
#         print(f'SORT BY "{sort_by.upper()}" WITH DICT')

#     else:
#         ######################################### get_categories ##############################################
#         categories = get_categories()
#         ############################################## make_dict ##############################################
#         trans_type = make_dict(categories)
#         ############################################## get_sort_by ##############################################
#         sort_by = get_sort_by(df, 'CATEGORY DATA')
#         print(f'SORT BY "{sort_by.upper()}" WITHOUT DICT')

#     skip_rows = []
#     for i in range(len(df)):
#         ##############################################add_transaction_type ###############################################
#         if i not in skip_rows:
#             all = search_row(cols, df, i, sort_by, skip_rows, 'searching')
#             data = all[0]
#             identity = all[1]
#             skip_rows = all[2]
#         else:
#             continue
#         pp.pprint(data)
#         print(identity)
#         print(i)
#         searched_dict = search_dict(trans_type, data, identity)
#         new_dict = searched_dict[0]
#         if 'identified' not in searched_dict[1].lower():
#             budget_dict = add_data(new_dict, data)
#     #pp.pprint(budget_dict)
#         # PROBLEM HERE, BOTH new_dict and budget_dict do the same thing,..... 
#         #pp.pprint(new_dict)
#     # print('budget_dict')
#     # print(budget_dict)
#     # print('new_dict')
#     # print(new_dict)
#     #####
#     print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
#     print('PROGRAM COMPLETE')
#     print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
#     return new_dict

# Remember to delete search row, search all and new split purchases if starting over and add_data
# <<<<<<<<WORKING>>>>>>>>>>>
# Need to format location input into a prettier line of code
def add_data(budget_dict, data):
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    print('RUNNING ADD DATA')
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    cat_options2 = " - ".join(sorted(list(budget_dict.keys()))[1:])
    len_cat = int(len(cat_options2)/2)
    location = str(input(
        f'\nCHOOSE CATEGORY FOR::: "{data[1]}"\n------------------------------------------------------------------------------------------------------\nCATEGORY OPTIONS:: {cat_options2[:len_cat]}\n{cat_options2[len_cat:]}\n------------------------------------------------------------------------------------------------------\n'))
    # Adding a new key if the entered key is not already in the dictionary or part of defaults
    if location[:3] not in [i[:3] for i in budget_dict.keys()]:
        add_key = input(
            f'"{location}":: NOT IN BUDGET FILE, WOULD YOU LIKE TO ADD IT? Y/N\n')
        if 'y' in add_key:
            budget_dict[location] = []
            print(f'ADDITION TO "{location.upper()}" SUCCESSFUL')
    # Matching the location input for the item to corresponding key
    for key, value in budget_dict.items():
        if location[:3] == key[:3]:
            print(f'YOU ENTERED "{location.upper()}" WE ARE MATCHING TO "{key.upper()}"')
            if type(data[0]) != type([]):
                value.append(data+[key])
                print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
                print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
                return budget_dict
            elif type(data[0]) == type([]) and len(data) > 1:
                for z in data:
                    z.append(key)
                    value.append(z)
                print('//////////////////////////////////////////////////////////////////////////////////////////////////////\n')
                print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
                return budget_dict
            else:
                print('ERROR SKIPPING')
    return budget_dict

def split_purchases(df, formatted_df=0, budget_dict=0):
    cols = confirm_cols(df, formatted_df)
    #pp.pprint(df)
    print('BEGIN PURCHASE CATEGORIZATION')
    print('------------------------------------------------------------------------------------------------------')
# if statement separates data if a correctly formatted dictionary is passed to it
# else it creates a dictionary
    if type(budget_dict) == type({}):
        ######################################### get_categories ##############################################
        categories = get_categories(list(budget_dict.keys()))
        ######################################### make_dict ##############################################
        trans_type = make_dict(categories, budget_dict)
        ######################################### get_sort_by ##############################################
        sort_by = get_sort_by(df, 'CATEGORY DATA')
        print(f'SORT BY "{sort_by.upper()}" WITH DICT')

    else:
        ######################################### get_categories ##############################################
        categories = get_categories()
        ############################################## make_dict ##############################################
        trans_type = make_dict(categories)
        ############################################## get_sort_by ##############################################
        sort_by = get_sort_by(df, 'CATEGORY DATA')
        print(f'SORT BY "{sort_by.upper()}" WITHOUT DICT')

    skip_rows = []
    for i in range(len(df)):
        ##############################################add_trans_type ###############################################
        if i not in skip_rows:
            get_col = add_transaction_type(df, i, sort_by)
            identity = get_col[1]
            

        # PRINT TESTING STATEMENTS
            # print(f'SORTING BY:: "{sort_by.upper()}" COLUMN')
            # print(f'IDENTIFIER IS:: {identity}')
            # organize_by = get_col[0]
            # print(f'COL NAME IS:: {organize_by}')
            # data_to_sort = df.iloc[i][organize_by]
            # print(f'CATEGORIZE DATA:: {data_to_sort}\n')
            # # trans_type is the entire dictionary
            # print(f'TRANSACTION TYPE IS:: {trans_type}\n')
            # print("DF is :: ")
            #pp.pprint(df)
            ############################################## search_dict ##############################################
            
            #########data grouping search##############
            mask = df.apply(lambda x: x.str.contains(rf'{identity}', na=False, case=False))
            matching_rows = df.loc[mask.any(axis=1)]
            skip_rows += matching_rows.index.tolist()

            if len(matching_rows) >= 2:
                print(f'{len(matching_rows)} ROWS MATCHED IN IMPORTED DATA:::')
                # print('ROWS MATCH\n')
                data = []
                for rows in matching_rows.index.tolist():
                    data.append(list(df.iloc[rows])+[identity])
                #pp.pprint(data)
            else:
                data = []
                print('NO MATCH IN IMPORTED DATA:::')
                for col in cols:
                        data.append(df.iloc[i][col])
                data.append(identity)
                #pp.pprint(data)

        else:
            continue
        searched_dict = search_dict(trans_type, data, identity)
        new_dict = searched_dict[0]
        if 'identified' not in searched_dict[1].lower():
            budget_dict = add_data(new_dict, data)
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    print('PROGRAM COMPLETE')
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    return new_dict

# def split_purchases_original(df, formatted_df=0, budget_dict=0):
#     cols = confirm_cols(df, formatted_df)
#     #pp.pprint(df)
#     print('BEGIN PURCHASE CATEGORIZATION')
#     print('------------------------------------------------------------------------------------------------------')
# # if statement separates data if a correctly formatted dictionary is passed to it
# # else it creates a dictionary
#     if type(budget_dict) == type({}):
#         ######################################### get_categories ##############################################
#         categories = get_categories(list(budget_dict.keys()))
#         ######################################### make_dict ##############################################
#         trans_type = make_dict(categories, budget_dict)
#         ######################################### get_sort_by ##############################################
#         sort_by = get_sort_by(df, 'CATEGORY DATA')
#         print(f'SORT BY "{sort_by.upper()}" WITH DICT')

#     else:
#         ######################################### get_categories ##############################################
#         categories = get_categories()
#         ############################################## make_dict ##############################################
#         trans_type = make_dict(categories)
#         ############################################## get_sort_by ##############################################
#         sort_by = get_sort_by(df, 'CATEGORY DATA')
#         print(f'SORT BY "{sort_by.upper()}" WITHOUT DICT')

#     skip_rows = []
#     for i in range(len(df)):
#         ##############################################add_trans_type ###############################################
#         if i not in skip_rows:
#             get_col = add_trans_type(df, i, sort_by)
#             identity = get_col[1]
            

#         # PRINT TESTING STATEMENTS
#             # print(f'SORTING BY:: "{sort_by.upper()}" COLUMN')
#             # print(f'IDENTIFIER IS:: {identity}')
#             # organize_by = get_col[0]
#             # print(f'COL NAME IS:: {organize_by}')
#             # data_to_sort = df.iloc[i][organize_by]
#             # print(f'CATEGORIZE DATA:: {data_to_sort}\n')
#             # # trans_type is the entire dictionary
#             # print(f'TRANSACTION TYPE IS:: {trans_type}\n')
#             # print("DF is :: ")
#             #pp.pprint(df)
#             ############################################## search_dict ##############################################
            
#             #########data grouping search##############
#             mask = df.apply(lambda x: x.str.contains(rf'{identity}', na=False, case=False))
#             matching_rows = df.loc[mask.any(axis=1)]
#             skip_rows += matching_rows.index.tolist()

#             if len(matching_rows) >= 2:
#                 print(f'{len(matching_rows)} ROWS MATCHED IN IMPORTED DATA:::')
#                 # print('ROWS MATCH\n')
#                 data = []
#                 for rows in matching_rows.index.tolist():
#                     data.append(list(df.iloc[rows])+[identity])
#                 #pp.pprint(data)
#             else:
#                 data = []
#                 print('NO MATCH IN IMPORTED DATA:::')
#                 for col in cols:
#                         data.append(df.iloc[i][col])
#                 data.append(identity)
#                 #pp.pprint(data)

#         else:
#             continue
#         searched_dict = search_dict(trans_type, data, identity)
#         new_dict = searched_dict[0]
#         if 'identified' not in searched_dict[1].lower():
#             budget_dict = add_data(new_dict, data)
#     #pp.pprint(budget_dict)
#         # PROBLEM HERE, BOTH new_dict and budget_dict do the same thing,..... 
#         #pp.pprint(new_dict)
#     # print('budget_dict')
#     # print(budget_dict)
#     # print('new_dict')
#     # print(new_dict)
#     #####
#     print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
#     print('PROGRAM COMPLETE')
#     print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
#     return new_dict


def test_date(df):

    df['date']= pd.to_datetime(df['date'])
    #pp.pprint(df)
    unique_cats = df.category.unique()
    #print(unique_cats)
    test_dict = {}
    key = []
    for i in unique_cats:
        separate_df = df.loc[df['category'] == i]
        key = []
        for j in range(len(separate_df)):
            key.append(separate_df.iloc[j].tolist())
        test_dict[i] = key    
        #key.append(separate_df)
        #test_dict['i'] = separate_df.set_index('category').T.to_dict('list')
    #pp.pprint(test_dict)
    return test_dict


def dict_to_Frame(data_dict):
    print('PROCCESSING DATAFRAME')
    skip_list = []
    rows = []
    for key, value in data_dict.items():
        # Skipping the first entry which is the columns
        if key == '0_format':
            print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
            print('SKIPPING FORMAT ROW')
            continue
        elif len(value) == 0:
            skip_list.append(key)
        else:
            for i in range(len(value)):
                if len(value[i]) == len(data_dict['0_format']):
                    rows.append(value[i])
                else:
                    rows.append(value[i]+[key])
        if 'category' not in data_dict['0_format']:
            cols = data_dict['0_format'] + ['category']
        else:
            cols = data_dict['0_format']      
    # print('********TEST******')
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    ## PLACE TO ADD EXTRA COLUMNS 
    #pp.pprint(rows)
    df = pd.DataFrame(np.array(rows), columns=cols)
    skip_list_p = ", ".join(skip_list)
    len_skip = int(len(skip_list_p)/2)
    print((f'NO AVAILABLE DATA, SKIPPING CATEGORIES IN DATAFRAME:::\n{skip_list_p[:len_skip]}\n{skip_list_p[len_skip:]}'))
    return df

# <<<<<<<<WORKING>>>>>>>>>>>
# Adding PYMONGO DB functionality
# Need to add a print statement, also pymongo install based on the users OS
# For consistent use of program need to add searchability for date and transaction type that the db connection only adds if the data is new

# Notes https://docs.mongodb.com/manual/reference/method/db.collection.find/
# https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/


def conn_mongo(data):
    import pymongo
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.clover
    if db.budgetDB.drop():
        # Make Input statement, add to database y/n or replace database
        print('MAKING NEW DATABASE')
    else:
        print('DB NOT PRESENT')
    db.show
    db.budgetDB.insert_one(data)

    # Hopefully printing the first 5 entries in the db
    # pprint(db.budgetDB.find_one())
    # db.budgetDB.find().pretty()

# regex for "Oct 21, 2014" or "October 21, 2014"
# need more sophisticated validations such as validating the number of days for a specific month
#(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})\s+(\d{4})
# February 2009
#\b(?:Jan(?:uary)?|Feb(?:ruary)?|...|Dec(?:ember)?) (?:19[7-9]\d|2\d{3})(?=\D|$)
# or
#(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})
#yyyy-mm-dd

#(\d+(?:/|\\|-)\d+(?:/|\\|-)\d{4}$)


def main():
    t_start = datetime.now()
    # <<<<<<<<WORKING>>>>>>>>>>>
    # Add import DB from mongo
    # Right now using written in dictionary

    dictionary = {
    '0_format': ['date', 'location data', 'float amount', 'identifier', 'category'],
    'home': [
        ['01/24/21', 'HOME_DEPOT',  -57, 'DEPOT','home'],
        ['01/12/21', 'LOWES', -100, 'LOWES', 'home'],
        ['02/14/21', 'TRUE_VALUE', -60, 'TRUE', 'home']],

    'take_away': [
        ['01/28/21', 'CHICK-FIL-A', -14.99, 'CHICK-FIL-A','take_away'],
        ['03/15/21', 'BOJANGLES 5555 ELIZABETH CITY NY', -12.99, 'BOJANGLES', 'take_away']
        ],

    'groceries': [
        ['01/22/21', 'FOOD LION',  -200, 'FOOD LION', 'groceries'],
        ['02/21/21', 'HARRIS_TEETER', -250, 'HARRIS', 'groceries'],
        ['03/15/21', 'FARM_FRESH', -150, 'FRESH', 'groceries']],
    'gas':[
        ['03/22/21', 'SHELL OIL 2423423423423 LUCY, PA', -28, 'SHELL', 'gas']
    ],
    'utilities':[
        ['03/18/21', 'DENVER SANITATION 489-4698-06456 CO', -80, 'SANITATION', 'utilities']
        ]
}

    #dictionary = None

    print('RUNNING GET DATA TYPE\n')
    formatted_df = None
    data_formatted = get_data_type()
    data = data_formatted[0]
    if data_formatted[1]:
        print(f'CONFIRMED DATA IS {data_formatted[1].upper()}')
        formatted_df = data_formatted[1]
    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    print('RUNNING SPLIT PURCHASES PROGRAM')
    print('------------------------------------------------------------------------------------------------------')
    ### place to limit data use data.head(num)
    if dictionary:
        trans_dict = split_purchases(data, formatted_df, dictionary)
    else:
        trans_dict = split_purchases(data, formatted_df)

    print('SPLIT PURCHASES PROGRAM COMPLETE')
    print('------------------------------------------------------------------------------------------------------')

    print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
    print('ADDING TO DICTIONARY')
    print('------------------------------------------------------------------------------------------------------')
    # <<<<<<<<WORKING>>>>>>>>>>>
    show_dict = input('PRINT OUT DICT Y/N\n')
    if 'y' in show_dict.lower():
        print('DICTIONARY VALUES :::::')
        pp.pprint(trans_dict)
        print('------------------------------------------------------------------------------------------------------')
    converted_DF = dict_to_Frame(trans_dict)
    trans_dict = test_date(converted_DF)
    print('------------------------------------------------------------------------------------------------------')

    # <<<<<<<<WORKING>>>>>>>>>>>
    #Change this to an input statement attached to the loop
    #Formats amounts and dates if not already formatted
    if data_formatted[1]:
        pass
    else:
        print('------------------------------------------------------------------------------------------------------')
        print('PLEASE ENTER THE COLUMN NAME OF THE DATE')
        col_with_dates = 'DATE'
        sort_by = get_sort_by(converted_DF, col_with_dates)
        converted_DF = converted_DF.sort_values(by=sort_by).reset_index(drop=True)
        pp.pprint(converted_DF)
        import format_data
        converted_DF = format_data.convert_date(converted_DF)
        # <<<<<<<<WORKING>>>>>>>>>>>
        #Change this to an input statement attached to the loop
        print('PLEASE ENTER THE COLUMN NAME OF THE AMOUNTS')
        col_with_amounts = 'AMOUNTS'
        sort_by = get_sort_by(converted_DF, col_with_amounts)
        converted_DF = make_num(converted_DF, sort_by)

    pp.pprint(converted_DF)
    create_database = input('ADD TO DATABASE? Y/N \n')
    if 'y' in create_database:
        conn_mongo(trans_dict)
        print('MongoDB Successful')
    save_csv(converted_DF)
    t_end = datetime.now()
    t_execute = t_end - t_start
    print(f'PROGRAM EXECUTION TIME {t_execute.total_seconds()}')
    return data, converted_DF


if __name__ == "__main__":
    main()

