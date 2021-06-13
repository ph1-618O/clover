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


# <<<<<<<<WORKING>>>>>>>>>>>
# Clean up import statements
# Think about separating functions into different .py files based on function
# Watch the order!!

import texthero as hero  # pip install texthero==1.0.5 works with newer python versions
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from fastnumbers import fast_float
import pprint
import plotly.graph_objects as go
import squarify
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib
import platform

# working with dates, month abbrev, and the
#  it takes to run prg
import datetime

# from datetime import datetime
# from datetime import date
from calendar import month_abbr
import time

# # for importing from excel to pandas
# from pandas import ExcelWriter
# from pandas import ExcelFile
import re
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

# Text Editing
pp = pprint.PrettyPrinter(indent=4)
# pip install nltk #NLP

# nltk.download("stopwords")
# nltk.download("punkt")


# graphing

# <<<<<<<<WORKING>>>>>>>>>>>
# Add unit tests and tests dealing with number input inconsistencies, avoids VALUE ERROR, ATTRIBUTE ERROR
# Use Try, Except and Assert

pd.set_option("display.max_rows", None, "display.max_columns", None)

# <<<<<<<<WORKING>>>>>>>>>>>
# Need to add in portion from other notebook that asked user if they want to install these dependencies if they are not included


def version_assistant():
    # print versions
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print("PYTHON VERSIONS")
    print("-----------------------------------------")
    print("python     : ", platform.python_version())
    print("pandas     : ", pd.__version__)
    print("matplotlib : ", matplotlib.__version__)
    print("squarify   :  0.4.3")
    print("-----------------------------------------\n\n")


def read_data(file_type):
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    data_file = input(f'ENTER "{file_type.upper()}" LOCATION\\NAME\n')
    if "csv" in file_type.lower():
        if data_file.endswith(".csv"):
            return pd.read_csv(data_file)
        else:
            return pd.read_csv(data_file + ".csv")
    elif data_file.endswith(".xls") or data_file.endswith(".xlsx"):
        return pd.read_excel(data_file)
    elif "xls" in file_type.lower() or "excel" in file_type.lower():
        print("\nERROR::: FILE EXTENSION OMITTED PLEASE RE-ENTER, XLS or XLSX\n")
        e_type = input("ENTER XLS OR XLSX\n")
        if "xlsx" in e_type:
            return pd.read_excel(data_file + ".xlsx")
        elif "xls" in e_type.lower():
            return pd.read_excel(data_file + ".xls")
    else:
        print("INVALID INPUT, EXITING PLEASE TRY AGAIN")
        exit()


def get_data_type():
    import_data = input(
        "DATA IS EXCEL FILE, CSV OR CLIPBOARD INPUT?\n").lower()
    query_format = input("IS DATA PROPERLY FORMATTED WITH COLUMNS? Y/N\n")
    formatted = None

    if ("csv" in import_data.lower() and "y" in query_format.lower()) or (
        "csv" in import_data.lower() and "n" in query_format.lower()
    ):
        # Normalizing the column names to lower
        data = read_data("csv")
        for i in data.columns:
            data = data.rename(columns={i: i.lower()})
        print(
            "------------------------------------------------------------------------------------------------------"
        )
        print("CHECKING COLUMNS")
        import format_data

        check_cols = format_data.get_col_names(data)
        data = check_cols[1]
        print(f'\n"{import_data.upper()}" DATASET, ...IMPORT SUCCESS\n')
        print("DATASET SAMPLE")
        print(
            "------------------------------------------------------------------------------------------------------"
        )
        pp.pprint(data.head())
        print(
            "------------------------------------------------------------------------------------------------------\n\n"
        )
        formatted = "formatted"

    elif (
        "clip" in import_data.lower()
        or "format" in query_format.lower()
        or "n" in query_format.lower()
    ):
        format_q = (f'FORMAT "{import_data.upper()}" DATA? Y/N').lower()
        if "n" in format_q.lower():
            # <<<<<<<<WORKING>>>>>>>>>>>
            # Fix Module import statement
            print(
                "//////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            print("RUNNING FORMAT_DATA PROGRAM")
            import format_data

            if "clip" in import_data.lower():
                data = import_clip()
                data = format_data.initiate_format(data)
                for i in data.columns:
                    data = data.rename(columns={i: i.lower()})
                print(f'\n"{import_data.upper()}" DATASET...IMPORT SUCCESS\n')
                print("DATASET")
                print(
                    "------------------------------------------------------------------------------------------------------"
                )
                pp.pprint(data.head())
                formatted = "formatted"
                # print('------------------------------------------------------------------------------------------------------')
            elif "format" in query_format.lower() or "n" in query_format.lower():
                data = read_data("csv")
                data = format_data.initiate_format(data)
                for i in data.columns:
                    data = data.rename(columns={i: i.lower()})
                print(
                    "//////////////////////////////////////////////////////////////////////////////////////////////////////"
                )
                print(
                    f'"{import_data.upper()}" FORMATED DATASET, ...IMPORT SUCCESS\n RETURNING TO CREATE_BUDGET_DICT'
                )
                print(
                    "//////////////////////////////////////////////////////////////////////////////////////////////////////"
                )
                print("DATASET")
                print(
                    "------------------------------------------------------------------------------------------------------"
                )
                pp.pprint(data.head())
                print(
                    "------------------------------------------------------------------------------------------------------\n\n"
                )
                formatted = "formatted"
            formatted = "formatted"

    elif "excel" in import_data or "xls" in import_data:
        data = read_data("excel")
        for i in data.columns:
            data = data.rename(columns={i: i.lower()})
        import format_data

        check_cols = format_data.get_col_names(data)
        data = check_cols[2]
        formatted = "formatted"
        print(f'\n"{import_data.upper()}" DATASET...IMPORT SUCCESS\n')
        print("DATASET")
        print(
            "------------------------------------------------------------------------------------------------------"
        )
        pp.pprint(data.head())
        print(
            "------------------------------------------------------------------------------------------------------"
        )

    else:
        print("INVALID INPUT, PLEASE TRY AGAIN")
        exit()
    return data, formatted


def import_clip():
    clipDF = pd.read_clipboard()
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    csvName = input("WHAT TYPE OF ACCOUNT FOR FILENAME?\n")
    csvName = csvName + ".csv"
    clipDF.to_csv(csvName, index=False)
    return pd.read_csv(csvName)


# <<<<<<<<WORKING>>>>>>>>>>>
# Redundant, kept if needed to add more than one csv file in the future?
# def import_csv():
#     csvName = input('ENTER CSV LOCATION\\NAME\n')
#     print('------------------------------------------------------------------------------------------------------')
#     if csvName.endswith('.csv'):
#         return pd.read_csv(csvName)
#     else:
#         csvName = csvName + '.csv'
#         return pd.read_csv(csvName)


def save_csv(df):
    save_csv = input("SAVE NEW DATAFRAME TO CSV? Y/N\n")
    if "y" in save_csv.lower():
        csvName = input("ENTER NEW CSV LOCATION\\NAME\n")
        accept_name = input(
            f"IS THIS THE CORRECT LOCATION\\FILENAME {csvName} Y\\N\n")
        while "y" not in accept_name.lower():
            if csvName[:-4] == ".csv":
                accept_name = input(
                    f"IS THIS THE CORRECT LOCATION\\FILENAME {csvName} Y\\N\n"
                )
            else:
                accept_name = input(
                    f'IS THIS THE CORRECT LOCATION\\FILENAME {csvName + ".csv"} Y\\N\n'
                )
                csvName = csvName + ".csv"
            accept_name = input(
                "WOULD YOU LIKE TO EXIT THE PROGRAM? Y\\N").lower()
        df.to_csv(csvName, index=False)
        print("DATA SUCCESSFULLY STORED TO CSV\n")
    else:
        print("EXITING")
        # exit()


def import_excel(path):
    sheet_or_file = input("IS YOUR EXCEL FILE ON A SHEET? Y/N\n")
    if "n" in sheet_or_file.lower():
        df = pd.read_excel(fr"{path}")
    elif "y" in sheet_or_file.lower() or "sheet" in sheet_or_file.lower():
        xls_sheet = input("WHAT IS THE SHEETS NAME?\n")
        df = pd.read_excel(fr"{path}", sheet_name=xls_sheet)
    else:
        print("INVALID INPUT EXITING PLEASE TRY AGAIN\n")
        exit()
    return df


# <<<<<<<<WORKING>>>>>>>>>>>
# figure out if these comments are useful
def get_sort_by(df, sort_query):
    print(
        "------------------------------------------------------------------------------------------------------"
    )
    print("DATAFRAME")
    print(
        "------------------------------------------------------------------------------------------------------"
    )
    pp.pprint(df.head())

    print(
        "------------------------------------------------------------------------------------------------------"
    )
    print(f'SORTING BY "{sort_query.upper()}"')
    print(
        "------------------------------------------------------------------------------------------------------"
    )
    if sort_query != "CATEGORY DATA":
        print(f'OPTIONS::: {" - ".join(list(df.columns))}')
        print(
            "------------------------------------------------------------------------------------------------------"
        )

    sort_col = constrain_input_loop(sort_query, list(df.columns))
    sort = " ".join(
        str(elem) for elem in [i for i in df.columns if i == sort_col.lower()]
    )
    return sort


def get_categories(categories=0):
    # look at jupyter notebook with purchases categorized as essential, non essential, fixed, variable, one-time and reoccuring
    # add these into the make dict with new sub categories
    defaults = sorted(
        [
            "groceries",
            "take_away",
            "home",
            "pet",
            "restaurant",
            "utility",
            "transportation",
            "gas",
            "medical",
            "entertainment",
            "deposit",
            "interest",
            "savings",
            "debt",
            "income",
            "work",
            "online",
            "other",
        ]
    )
    if categories:
        if type(categories) == type([]):
            if len(categories) < len(defaults + ["0_format"]):
                # Trying to skip printing out 0_format, needs better code
                categories_list = " - ".join(sorted(categories)[1:])
                c_len = len(categories_list)
                if "0_format" in categories:
                    print(
                        f"CURRENT CATEGORIES::: {categories_list[:int(c_len/2)]}\n{categories_list[int(c_len/2):]}\n------------------------------------------------------------------------------------------------------"
                    )
                else:
                    print(
                        f"CURRENT CATEGORIES::: {categories_list[:int(c_len/2)]}\n{categories_list[int(c_len/2):]}\n------------------------------------------------------------------------------------------------------"
                    )
                add_defaults = []
                for i in defaults:
                    if i not in categories:
                        add_defaults.append(i)
                for i in add_defaults:
                    categories.append(i)
                categories = sorted(categories)
                # CODE BELOW ASKS USER IF THEY WANT TO KEEP CATS
                # COMMENTED OUT BECAUSE THEY WILL BE REMOVED ANYWAY IF EMPTY
                # d_list = " - ".join([i.lower() for i in add_defaults])
                # d_len = len(d_list)
                # print(f'DEFAULTS NOT IN CURRENT CATEGORIES:::\n "{d_list[:int(d_len/2)]}\n{d_list[int(d_len/2):]}"\n------------------------------------------------------------------------------------------------------')
                # confirm_addition = input('ADD EXTRA DEFAULTS TO CATEGORIES Y/N\n')
                # if 'y' in confirm_addition.lower():
                #     for i in add_defaults:
                #         categories.append(i)
                #     categories = sorted(categories)
    else:
        categories = defaults
        # print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
        # d_list2 = " - ".join(defaults)
        # d_len2 = len(d_list2)
        # print(f'DEFAULT CATEGORIES::: \n------------------------------------------------------------------------------------------------------\n{d_list2[:int(d_len2/2)]}\n{d_list2[int(d_len2/2):]}\n------------------------------------------------------------------------------------------------------')
        # use_defaults = input('USE DEFAULTS::: Y/N\n')
        # if 'y' in use_defaults:
        #     categories = defaults
        # else:
        #     categories = input(
        #         'ENTER BUDGET CATEGORIES:::\n')
        # cat = ''
        # if type(categories) == type('s'):
        #     #need to add regex to sub a space between words with an underscore but before a comma
        #     if ',' in categories:
        #         categories = [i.strip().replace(' ', '_') for i in categories.split(',')]
        #     else:
        #         categories = sorted(categories.split())

    # <<<<<<<<WORKING>>>>>>>>>>>
    # Add a section that if you ask the user to continue and there is any other value than y
    # print out the list with index numbers, ask which number is wrong
    # add a loop to make sure you fix all the type errors
    if categories[0].lower() == "0_format":
        print(
            "------------------------------------------------------------------------------------------------------"
        )
        cat_list2 = " - ".join([str(x) for x in [*categories[1:]]])
        c_len2 = len(cat_list2)
        print(
            f'CATEGORIES ARE::: "{cat_list2[:int(c_len2/2)]}\n{cat_list2[int(c_len2/2):]}"'
        )
        print(
            "------------------------------------------------------------------------------------------------------\n"
        )
        print(
            "//////////////////////////////////////////////////////////////////////////////////////////////////////\n"
        )
    else:
        print(
            "------------------------------------------------------------------------------------------------------"
        )
        cat_list3 = " - ".join([str(x) for x in [*categories]])
        c_len3 = len(cat_list3)
        print(
            f'CATEGORIES ARE:::\n"{cat_list3[:int(c_len3/2)]}\n{cat_list3[int(c_len3/2):]}"'
        )
        # print(f'CATEGORIES ARE::: "{" - ".join([str(x) for x in [*categories]])}"')
        print(
            "------------------------------------------------------------------------------------------------------\n"
        )
        print(
            "//////////////////////////////////////////////////////////////////////////////////////////////////////\n"
        )
    return categories


# <<<<<<<<WORKING>>>>>>>>>>>
# ADD EXIT QUERY FOR LOOP


def constrain_input_loop(sort_query, list_options):
    if sort_query == "CATEGORY DATA" and "transaction" in list_options:
        return "transaction"
    elif sort_query.lower() == "date" and "date" in list_options:
        return "date"
    elif sort_query.lower() == "amount" and (
        "amount" in list_options or "float_amount" in list_options
    ):
        return "amount"
    else:
        correct = ""
        while "y" not in correct.lower():
            for index in range(len(list_options)):
                correct = input(
                    f'SORT THIS {sort_query} BY:: "{list_options[index].upper()}", Y/N OR EXIT\n'
                )
                if "y" in correct.lower():
                    print(
                        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
                    )
                    print(
                        f'YOU WILL SORT THIS "{sort_query}" BY::"{list_options[index].upper()}"\n'
                    )
                    return list_options[index]
                elif "n" in correct.lower():
                    print(f'"{correct.upper()}" ENTERED, PLEASE CHOOSE AGAIN')
                    continue
                else:
                    print("YOU MUST ENTER YES OR NO")
                    exit = input("WOULD YOU LIKE TO EXIT THIS PROGRAM? Y/N\n")
                    if "y" in exit.lower():
                        print("EXITING")
                        exit()
                # <<<<<<<<WORKING>>>>>>>>>>>
                # why is error thrown when exit == 'y' ??


# Removing stop words dependencies
# pip install nltk
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

nltk.download("stopwords")
nltk.download("punkt")

# Removes most common words


def remove_stop_words(transaction_word_list):
    text_token = word_tokenize(transaction_word_list)
    stop_words = set(stopwords.words("english"))
    tokens_without_sw = [
        word for word in text_token if word.casefold() not in stop_words
    ]
    # print(tokens_without_sw)
    # print(text_token)
    return tokens_without_sw


# original regex
# / ^[A-Za-z0-9]{3, }/
# new
# (?i)(?!\bTST\b | WWW | USA)( ^ [A-Za-z0-9]{3, })

def add_transaction_type(df, i, sort_by=0):
    ####################################################get_sort_by  '[^A-Za-z0-9]+'  ####################################################
    if sort_by:
        # Using re.sub to remove everyting but numbers and words
        purchase_type = remove_stop_words(
            re.sub("/^[A-Za-z0-9]{3,}/", " ", df[sort_by][i])
        )
        print(
            "//////////////////////////////////////////////////////////////////////////////////////////////////////"
        )
        for index in range(len(purchase_type)):
            if len(purchase_type[index]) < 3:
                sort_by = 'transaction' #was None to limit the id to > 3 letters but that didn't work
                pass
            else:
                if purchase_type[index].lower() == 'tst' or purchase_type[index].lower() == 'usa' or purchase_type[index].lower() == 'www' or purchase_type[index].lower() == 'afc':
                    continue
                else:
                    print(f'TESTING IDENTIFIER:: "{purchase_type[index]}"')
                    print(
                        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
                    )
                    print(
                        f'SORTING TRANSACTION:: "{str(sort_by).upper()}" BY IDENTIFIER::"{purchase_type[index].upper()}"'
                    )
                    return sort_by, purchase_type[index].lower()


# def add_transaction_type_confirm(df, i, sort_by=0):
#     ####################################################get_sort_by####################################################
#     if sort_by:
#         purchase_type = df[sort_by][i].replace('*', ' ').split()
#         print('//////////////////////////////////////////////////////////////////////////////////////////////////////')
#         key = ''
#         while 'y' not in key.lower():
#             for index in range(len(purchase_type)):
#                 key = input(
#                     f'SORT THIS PURCHASE BY:: "{purchase_type[index]}", Y/N\n')
#                 if 'y' in key:
#                     print(
#                         '//////////////////////////////////////////////////////////////////////////////////////////////////////')
#                     print(
#                         f'SORTING TRANSACTION:: "{str(sort_by).upper()}" BY IDENTIFIER::{purchase_type[index].upper()}')
#                     return sort_by, purchase_type[index].lower()
#                 else:
#                     print(
#                         '//////////////////////////////////////////////////////////////////////////////////////////////////////')
#                     print('YOU MUST ENTER YES OR NO')
#                     print('CHOOSE AGAIN')
#                     continue
#             key = input('WOULD YOU LIKE TO EXIT THIS PROGRAM? Y/N\n')


def convert_amount(entry):
    # there are entries where there is no balance listed
    entry = str(entry)
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
    return df


def make_dict(categories, old_dict=0):
    # <<<<<<<<WORKING>>>>>>>>>>>
    # look at jupyter notebook with purchases categorized as essential, non essential, fixed, variable, one-time and reoccuring
    # add these into the make dict with new sub categories
    if type(old_dict) == type({}):
        # print('DICT CONFIRMED')
        if "0_format" not in old_dict.keys():
            # print('0_FORMAT NOT IN DICTIONARY ADDING\n')
            old_dict["0_format"] = [
                "date",
                "transaction",
                "amount",
                "identifier",
                "category"
            ]
        for i in categories:
            if i not in old_dict.keys():
                old_dict[i] = []
        trans_type = old_dict

    else:
        trans_type = {"0_format": [
            "date", "transaction", "amount", "identifier", "category"]}
        for i in categories:
            trans_type[i] = []
    return trans_type


# <<<<<<<<WORKING>>>>>>>>>>>
# Need to clean up add_Data and search_dict
def search_dict(budget_dict, data, data_point):  # location is column name
    print(f"SEARCHING DICT FOR {data_point.upper()}")
    if data_point.lower() == "the":
        pass
    else:
        for key, value in budget_dict.items():
            # skip keys that are empty
            if value and len(value) > 0:
                for i in value:
                    if i and len(i) > 0:
                        for j in i:
                            if (
                                re.search(rf"{data_point}", str(
                                    j), re.IGNORECASE) != None
                            ):
                                print(
                                    "//////////////////////////////////////////////////////////////////////////////////////////////////////"
                                )
                                print(f"DATA POINT IDENTIFIED")
                                print(f'ADDING TO CATEGORY "{key.upper()}"')
                                for x in data:
                                    if type(x) == type([]) and len(data) == 1:
                                        return budget_dict, "identified"
                                    elif type(x) == type([]) and len(data) > 1:
                                        value.append(x + [key])
                                    else:
                                        value.append(data + [key])
                                        return budget_dict, "identified"
                                return budget_dict, "identified"
                            else:
                                continue  # pass
    return budget_dict, "unknown"


# <<<<<<<<WORKING>>>>>>>>>>>
# NEED TO ADD TRY/ACCEPT STATEMENTS for ALL_INPUTS


def confirm_cols(df, formatted_df=0):
    if formatted_df:
        return list(df.columns)
    else:
        keep_cols = input("KEEP COLUMN NAMES? Y/N\n")
        if "n" in keep_cols:
            cols = input("COLUMNS TO KEEP::\n")
            cat = ""
            for k in cols:
                if "," in cols:
                    cat += k.strip(",")
                else:
                    cat += k
            cols = cat.split(" ")
            for c in cols:
                try:
                    df[c.lower()]
                except KeyError:
                    print("ERROR, RE-ENTER COLUMN\n")
        else:
            cols = df.columns
    return cols


# <<<<<<<<WORKING>>>>>>>>>>>
# Need to format location input into a prettier line of code
def add_data(budget_dict, data):
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print("RUNNING ADD DATA")
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    cat_options2 = " - ".join(sorted(list(budget_dict.keys()))[1:])
    len_cat = int(len(cat_options2) / 2)
    # formatting print statement to only print transaction data
    if len(data[1]) == 4:
        print_trans = data[1][1]
    else:
        print_trans = data[1]
    location = str(
        input(
            f"\n{print_trans} CHOOSE CATEGORY::: \n------------------------------------------------------------------------------------------------------\nCATEGORY OPTIONS:: {cat_options2[:len_cat]}\n{cat_options2[len_cat:]}\n------------------------------------------------------------------------------------------------------\n"
        )
    )
    sub_keys = {
        'food': 'groceries',
        'foo': 'groceries',
        'fast food': 'take away',
        'fast': 'take away',
        'travel': 'holiday',
        'trav': 'holiday'
        }
    
    for sub_key, sub_value in sub_keys.items():
        if location.lower() == sub_key:
            print(f'SWITCHING {location.upper()} WITH {sub_value.upper()}, {location.upper()} IS A DOUBLE MATCH')
            location = sub_value
            
    # Adding a new key if the entered key is not already in the dictionary or part of defaults
    if location[:3] not in [i[:3] for i in budget_dict.keys()] and (
        location != "0_format"
    ):
        add_key = input(
            f'"{location}":: NOT IN BUDGET FILE, WOULD YOU LIKE TO ADD IT? Y/N\n'
        )
        if "y" in add_key:
            print(f'ADDITION TO "{location.upper()}" SUCCESSFUL')        
            budget_dict[location] = []
        else:
            location = 'other'
            budget_dict[location] = []
            print(f'ADDING TO"{location.upper()}" SUCCESSFUL')
    # Matching the location input for the item to corresponding key
    for key, value in budget_dict.items():
        # find a better way to do this with a dictionary {'fast_food:'take_away', 'food':'groceries, 'travel':'holiday'} etc
        # if location.lower() == 'travel':
        #     key = 'holiday'
        #     if type(data[0]) != type([]):
        #         value.append(data + [key])
        #         print(
        #             "//////////////////////////////////////////////////////////////////////////////////////////////////////"
        #         )
        #         print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
        #         return budget_dict
        #     elif type(data[0]) == type([]) and len(data) > 1:
        #         for z in data:
        #             z.append(key)
        #             value.append(z)
        #         print(
        #             "//////////////////////////////////////////////////////////////////////////////////////////////////////\n"
        #         )
        #         print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
        #         return budget_dict
        #     else:
        #         print("ERROR SKIPPING")
        # elif location.lower() == 'food':
        #     key = 'grocery'
        #     if type(data[0]) != type([]):
        #         value.append(data + [key])
        #         print(
        #             "//////////////////////////////////////////////////////////////////////////////////////////////////////"
        #         )
        #         print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
        #         return budget_dict
        #     elif type(data[0]) == type([]) and len(data) > 1:
        #         for z in data:
        #             z.append(key)
        #             value.append(z)
        #         print(
        #             "//////////////////////////////////////////////////////////////////////////////////////////////////////\n"
        #         )
        #         print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
        #         return budget_dict
        #     else:
        #         print("ERROR SKIPPING")
        
        # elif location.lower() == 'fast food' or location == 'fast_food':
        #     key = 'take_away'
        #     if type(data[0]) != type([]):
        #         value.append(data + [key])
        #         print(
        #             "//////////////////////////////////////////////////////////////////////////////////////////////////////"
        #         )
        #         print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
        #         return budget_dict
        #     elif type(data[0]) == type([]) and len(data) > 1:
        #         for z in data:
        #             z.append(key)
        #             value.append(z)
        #         print(
        #             "//////////////////////////////////////////////////////////////////////////////////////////////////////\n"
        #         )
        #         print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
        #         return budget_dict
        #     else:
        #         print("ERROR SKIPPING")
        if location[:3] == key[:3]:
            print(
                f'YOU ENTERED "{location.upper()}" WE ARE MATCHING TO "{key.upper()}"'
            )
            if type(data[0]) != type([]):
                value.append(data + [key])
                print(
                    "//////////////////////////////////////////////////////////////////////////////////////////////////////"
                )
                print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
                return budget_dict
            elif type(data[0]) == type([]) and len(data) > 1:
                for z in data:
                    z.append(key)
                    value.append(z)
                print(
                    "//////////////////////////////////////////////////////////////////////////////////////////////////////\n"
                )
                print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
                return budget_dict
            else:
                print("ERROR SKIPPING")
    return budget_dict


def split_purchases(df, formatted_df=0, budget_dict=0):
    cols = confirm_cols(df, formatted_df)
    # pp.pprint(df)
    print("BEGIN PURCHASE CATEGORIZATION")
    print(
        "------------------------------------------------------------------------------------------------------"
    )
    # if statement separates data if a correctly formatted dictionary is passed to it
    # else it creates a dictionary
    if type(budget_dict) == type({}):
        ######################################### get_categories ##############################################
        categories = get_categories(list(budget_dict.keys()))
        ######################################### make_dict ##############################################
        trans_type = make_dict(categories, budget_dict)
        ######################################### get_sort_by ##############################################
        sort_by = get_sort_by(df, "CATEGORY DATA")
        print(f'SORT BY "{sort_by.upper()}" WITH DICT')

    else:
        ######################################### get_categories ##############################################
        categories = get_categories()
        ############################################## make_dict ##############################################
        trans_type = make_dict(categories)
        ############################################## get_sort_by ##############################################
        sort_by = get_sort_by(df, "CATEGORY DATA")
        print(f'SORT BY "{sort_by.upper()}" WITHOUT DICT')

    skip_rows = []
    for i in range(len(df)):
        ##############################################add_trans_type ###############################################
        if i not in skip_rows:
            get_col = add_transaction_type(df, i, sort_by)
            # print(get_col)
            identity = get_col[1]
            #########data grouping search##############
            # NEED TO ADD A TYPE TEST BEFORE THIS
            # print(identity)
            mask = df.select_dtypes(
                include=["object"], exclude=["float64", "int64", "datetime"]
            ).apply(lambda x: x.str.contains(rf"{identity}", na=False, case=False))
            # mask = df.apply(lambda x: x.str.contains(rf'{identity}', na=False, case=False))
            matching_rows = df.loc[mask.any(axis=1)]
            skip_rows += matching_rows.index.tolist()

            # print(matching_rows)
            if len(matching_rows) >= 2:
                print(f"{len(matching_rows)} ROWS MATCHED IN IMPORTED DATA:::")
                # print('ROWS MATCH\n')
                data = []
                for rows in matching_rows.index.tolist():
                    data.append(list(df.iloc[rows]) + [identity])
                # pp.pprint(data)
            else:
                data = []
                print("NO MATCH IN IMPORTED DATA:::")
                for col in cols:
                    data.append(df.iloc[i][col])
                data.append(identity)
                # pp.pprint(data)

        else:
            continue
        # print(identity)
        searched_dict = search_dict(trans_type, data, identity)
        new_dict = searched_dict[0]
        if "identified" not in searched_dict[1].lower():
            budget_dict = add_data(new_dict, data)
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print("PROGRAM COMPLETE")
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    return new_dict

    # PRINT TESTING STATEMENTS for SPLIT PURCHASES
    # print(f'SORTING BY:: "{sort_by.upper()}" COLUMN')
    # print(f'IDENTIFIER IS:: {identity}')
    # organize_by = get_col[0]
    # print(f'COL NAME IS:: {organize_by}')
    # data_to_sort = df.iloc[i][organize_by]
    # print(f'CATEGORIZE DATA:: {data_to_sort}\n')
    # # trans_type is the entire dictionary
    # print(f'TRANSACTION TYPE IS:: {trans_type}\n')
    # print("DF is :: ")
    # pp.pprint(df)
    ############################################## search_dict ##############################################


def make_test_dict(df):
    unique_cats = df.category.unique()
    # print(unique_cats)
    test_dict = {}
    key = []
    for i in unique_cats:
        separate_df = df.loc[df["category"] == i]
        key = []
        for j in range(len(separate_df)):
            key.append(separate_df.iloc[j].tolist())
        test_dict[i] = key
        # key.append(separate_df)
        # test_dict['i'] = separate_df.set_index('category').T.to_dict('list')
    # pp.pprint(test_dict)
    return test_dict


def test_date(df):
    # testing all columns with the word date
    # if test in list col num and list_cols comprehension are redundant too tired to fix
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print('TESTING DATES')
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    list_cols = [i.lower() for i in df.columns.tolist()]
    test_cols = ["date", "pending", "posted"]
    verified_cols = []
    for col in list_cols:
        for test in test_cols:
            if test in col:
                verified_cols.append(col)
    # print(verified_cols)
    for tested in verified_cols:
        if all(df[tested].map(type) != type(datetime.datetime.now())):
            # add second conditional here that tests the col for floats, ints and strings
            print("CONVERTING DATAFRAME DATES TO DATETIME")
            print(
                "//////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            df[tested] = pd.to_datetime(df[tested])
    # pp.pprint(df)
    return df


def test_amounts(df):
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print('TESTING AMOUNTS')
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    converted_col = []
    list_cols = [i.lower() for i in df.columns.tolist()]
    test_cols = ["amount", "value", "balance"]
    verified_cols = []
    for col in list_cols:
        for test in test_cols:
            if test in col:
                verified_cols.append(col)
    # print(verified_cols)
    for tested in verified_cols:
        search_floats = df[tested].apply(
            lambda x: 'True' if type(x) == type(0.1) else 'False')
        #floats_test = [True for i in range(len(df[tested])) if type(df[tested][i]) == type(0.1)]
        if search_floats.all():
            print('COLUMNS ARE FLOATS SKIPPING')
            continue
        elif (df[tested].map(type) == str).all():
            # add second conditional here that tests the col for floats, ints and strings
            print(
                "//////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            print("NORMALIZING AMOUNTS")
            print(
                "//////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            for row_num in range(len(df)):
                converted_col.append(convert_amount(
                    df[tested][row_num]))
            df[tested] = converted_col
        else:
            print('your amount columns are all a mess, see your programmer')
    return df


# trying to find the difference between the two dataframes
# there must be a strip function buried in there and some spaces or special characters that i cant find
# so that the rows do not match
def match_dataframes(new_DF, old_DF):
    list_match = ["date", "transaction", "amount"]
    for i in list_match:
        if i in list(new_DF.columns) and i in list(old_DF.columns):
            test_merge_old = old_DF.loc[:, list_match].convert_dtypes()
            test_merge_new = new_DF.loc[:, list_match].convert_dtypes()
    #print(test_merge_new.head())
    #print(test_merge_old.head())
    
    
    # this came back with 12ish rows?  should be 0 with identical data
    match_not_in_new = test_merge_old[~test_merge_old.index.isin(test_merge_new.index)]
    print('OLD NOT IN NEW')
    print(len(match_not_in_new))
    print(match_not_in_new)
    
    
    # This came back empty
    match_not_in_old = test_merge_new[~test_merge_new.index.isin(test_merge_old.index)]
    print('OLD NOT IN NEW')
    print(len(match_not_in_old))
    print(match_not_in_old)
    
    
    # tests if the dataframes are exact equals
    equal = test_merge_old.equals(test_merge_new)
    print('EQUAL?')
    print(equal)
    
    test_concat = pd.concat([test_merge_old, test_merge_new]).drop_duplicates().reset_index(drop=True)
    print('CONCAT W/ DROP')
    print(len(test_concat))
    print(test_concat.head())
    
    
    
    # print(new_DF.iloc[214:226])
    # print(old_DF.iloc[214:226])

    exit()


# Omit old data removes the chance of making copies of data already within db or dict
def omit_old_data(old_data_dict, new_data_dict):
    new_data = {
        k: new_data_dict[k]
        for k in new_data_dict
        if k in old_data_dict and new_data_dict[k] == old_data_dict[k]
    }
    if len(new_data) == 0:
        return None
    else:
        return new_data


# def dict_to_Frame(data_dict, dictionary = 0):
#     if dictionary:
#         df = dict_to_Frame_with_data(data_dict)
#     else:
#         df = dict_to_Frame_no_data(data_dict)
#     return df


def dict_to_Frame(data_dict):
    import format_data as format
    print("PROCCESSING DATAFRAME")
    skip_list = []
    rows = []

    if "category" not in data_dict["0_format"]:
        data_dict["0_format"] = data_dict["0_format"] + ["category"]
    else:
        pass
    cols = data_dict["0_format"]
    for key, value in data_dict.items():
        # Skipping the first entry which is the columns
        if key == "0_format":
            print(
                "//////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            print("SKIPPING FORMAT ROW")
            continue
        elif len(value) == 0:
            skip_list.append(key)
            continue
        else:
            for i in range(len(value)):
                if len(value[i]) == len(data_dict["0_format"]):
                    rows.append(value[i])
                else:
                    rows.append(value[i] + [key])
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    # PLACE TO ADD EXTRA COLUMNS
    # pp.pprint(rows)
    df = pd.DataFrame(np.array(rows), columns=cols).drop_duplicates().reset_index(drop=True)
    skip_list_p = ", ".join(skip_list)
    len_skip = int(len(skip_list_p) / 2)
    print(
        (
            f"NO AVAILABLE DATA, SKIPPING CATEGORIES IN DATAFRAME:::\n{skip_list_p[:len_skip]}\n{skip_list_p[len_skip:]}"
        )
    )
    # place to add convert date from format_data to make all rows datetime objs
    #df = format.convert_date(df)
    return df


def dict_to_Frame_with_data(data_dict):
    import format_data as format
    print("PROCCESSING DATAFRAME")
    skip_list = []
    rows = []
    # print(data_dict['0_format'])
    # print(type(data_dict['0_format']))

    # print(data_dict['0_format'][0])
    # print(type(data_dict['0_format'][0]))

    if "category" not in data_dict["0_format"] and type(data_dict["0_format"]) != type(['list']):
        data_dict["0_format"] = data_dict["0_format"] + ["category"]
    elif "category" not in data_dict["0_format"][0] and type(data_dict["0_format"][0]) != type('str'):
        data_dict["0_format"] = data_dict["0_format"][0] + "category"
    else:
        pass
    cols = data_dict["0_format"]
    for key, value in data_dict.items():
        # Skipping the first entry which is the columns
        if key == "0_format":
            print(
                "//////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            print("SKIPPING FORMAT ROW")
            continue
        elif len(value) == 0:
            skip_list.append(key)
            continue
        else:
            for i in range(len(value)):
                if len(value[i]) == len(data_dict["0_format"]):
                    rows.append(value[i])
                else:
                    rows.append(value[i] + [key])
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    # PLACE TO ADD EXTRA COLUMNS
    # pp.pprint(rows)
    df = pd.DataFrame(np.array(rows), columns=cols).drop_duplicates().reset_index(drop=True)
    skip_list_p = ", ".join(skip_list)
    len_skip = int(len(skip_list_p) / 2)
    print(
        (
            f"NO AVAILABLE DATA, SKIPPING CATEGORIES IN DATAFRAME:::\n{skip_list_p[:len_skip]}\n{skip_list_p[len_skip:]}"
        )
    )
    # place to add convert date from format_data to make all rows datetime objs
    #df = format.convert_date(df)
    return df


# <<<<<<<<WORKING>>>>>>>>>>>
# Adding PYMONGO DB functionality
# Need to add a print statement, also pymongo install based on the users OS
# For consistent use of program need to add searchability for date and transaction type that the db connection only adds if the data is new

# Notes https://docs.mongodb.com/manual/reference/method/db.collection.find/
# https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/


def conn_mongo(data):
    import pymongo

    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    db = client.clover
    if db.budgetDB.drop():
        # Make Input statement, add to database y/n or replace database
        print("MAKING NEW DATABASE")
    else:
        print("DB NOT PRESENT")
    pprint.pprint(db.show_collections)
    # Maybe needs to be
    # for i in data:
    #     db.budgetDB.insert_one(i)
    db.budgetDB.insert_one(data)

    # Hopefully printing the first 5 entries in the db
    pprint.pprint(db.budgetDB.find())
    # db.budgetDB.find().pretty()

def import_test_data():
    # Comparing a dataframe of new_data with old data
    # dropping duplicates
    # dictionary_DF = (
    #     dict_to_Frame(dictionary).sort_values(
    #         by="date").drop_duplicates().reset_index(drop=True)
    # )

    # print(dictionary_DF.head())

    #### Start

    # saving csv out before matching
    data = test_date(data)
    data = data.drop_duplicates().sort_values(
        by=['date', 'transaction', 'amount']).reset_index(drop=True)
    save_csv(data)

    #by=['date', 'category', 'identifier', 'amount']).drop_duplicates().reset_index(drop=True)

    import format_data
    import json
    with open('data/test/dictionary.json') as import_dict:
        imported_dict = json.load(import_dict)
    dictionary_DF = (
        dict_to_Frame(imported_dict).drop_duplicates().sort_values(
            by=['date', 'transaction', 'amount']).reset_index(drop=True)
    )
    dictionary_DF = test_date(dictionary_DF)
    save_csv(dictionary_DF)
    #print(dictionary_DF.head())
    #pp.pprint(dictionary_DF.head())
    #print(data.head())
    testing_frames = match_dataframes(data, dictionary_DF)

    #place to limit data use data.head(num)
    if imported_dict and testing_frames:
        trans_dict = split_purchases(data, formatted_df, imported_dict)
    else:
        trans_dict = split_purchases(data, formatted_df)

    # Test to see if any data is overlapping, omitting if it is
    new_data = omit_old_data(imported_dict, trans_dict)
    if new_data:
        from itertools import chain

        merged_dict = {}
        for k, v in chain(imported_dict.items(), trans_dict.items()):
            merged_dict.setdefault(k, []).extend(v)
    else:
        print("THERE IS NO NEW DATA, EXITING")
        exit()

    trans_dict = omit_old_data(trans_dict, imported_dict)
    print("SPLIT PURCHASES PROGRAM COMPLETE")
    print(
        "------------------------------------------------------------------------------------------------------"
    )

    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print("ADDING TO DICTIONARY")
    print(
        "------------------------------------------------------------------------------------------------------"
    )
    # <<<<<<<<WORKING>>>>>>>>>>>
    show_dict = input("PRINT OUT DICT Y/N\n")
    if "y" in show_dict.lower():
        print("DICTIONARY VALUES :::::")
        pp.pprint(merged_dict)
        print(
            "------------------------------------------------------------------------------------------------------"
        )
    converted_DF = dict_to_Frame(merged_dict)
    new_DF = test_amounts(converted_DF)
    new_DF = test_date(new_DF)
    print(
        "------------------------------------------------------------------------------------------------------"
    )

    # <<<<<<<<WORKING>>>>>>>>>>>
    # Change this to an input statement attached to the loop
    # Formats amounts and dates if not already formatted
    if data_formatted[1]:
        pass
    else:
        print(
            "------------------------------------------------------------------------------------------------------"
        )
        print("PLEASE ENTER THE COLUMN NAME OF THE DATE")
        col_with_dates = "DATE"
        sort_by = get_sort_by(new_DF, col_with_dates)
        new_DF = new_DF.sort_values(by=sort_by).reset_index(drop=True)
        pp.pprint(new_DF)
        import format_data

        new_DF = format_data.convert_date(new_DF)
        # <<<<<<<<WORKING>>>>>>>>>>>
        # Change this to an input statement attached to the loop
        print("PLEASE ENTER THE COLUMN NAME OF THE AMOUNTS")
        col_with_amounts = "AMOUNTS"
        sort_by = get_sort_by(new_DF, col_with_amounts)
        new_DF = make_num(new_DF, sort_by)

    pp.pprint(new_DF.head())
    create_database = input("ADD TO DATABASE? Y/N \n")
    if "y" in create_database:
        conn_mongo(merged_dict)
        print("MongoDB Successful")
    save_csv(new_DF)
    t_end = datetime.datetime.now()
    t_execute = t_end - t_start
    print(f"PROGRAM EXECUTION TIME {t_execute.total_seconds()/60}")
    return data, new_DF
    

def main():
    t_start = datetime.datetime.now()

    # <<<<<<<<WORKING>>>>>>>>>>>
    # Add import DB from mongo
    # Right now using written in dictionary

    #     dictionary = {
    #     '0_format': ['date', 'location data', 'float amount', 'identifier', 'category'],
    #     'home': [
    #         ['01/24/21', 'HOME_DEPOT',  -57, 'DEPOT','home'],
    #         ['01/12/21', 'LOWES', -100, 'LOWES', 'home'],
    #         ['02/14/21', 'TRUE_VALUE', -60, 'TRUE', 'home']],

    #     'take_away': [
    #         ['01/28/21', 'CHICK-FIL-A', -14.99, 'CHICK-FIL-A','take_away'],
    #         ['03/15/21', 'BOJANGLES 5555 ELIZABETH CITY NY', -12.99, 'BOJANGLES', 'take_away']
    #         ],

    #     'groceries': [
    #         ['01/22/21', 'FOOD LION',  -200, 'FOOD LION', 'groceries'],
    #         ['02/21/21', 'HARRIS_TEETER', -250, 'HARRIS', 'groceries'],
    #         ['03/15/21', 'FARM_FRESH', -150, 'FRESH', 'groceries']],
    #     'gas':[
    #         ['03/22/21', 'SHELL OIL 2423423423423 LUCY, PA', -28, 'SHELL', 'gas']
    #     ],
    #     'utilities':[
    #         ['03/18/21', 'DENVER SANITATION 489-4698-06456 CO', -80, 'SANITATION', 'utilities']
    #         ]
    # }

    dictionary = None

    print("RUNNING GET DATA TYPE\n")
    formatted_df = None
    data_formatted = get_data_type()
    data = data_formatted[0]
    if data_formatted[1]:
        print(f"CONFIRMED DATA IS {data_formatted[1].upper()}")
        formatted_df = data_formatted[1]
    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print("RUNNING SPLIT PURCHASES PROGRAM")
    print(
        "------------------------------------------------------------------------------------------------------"
    )

    # OLD STUFF THAT WORKS
    if dictionary:
        trans_dict = split_purchases(data, formatted_df, dictionary)
    else:
        trans_dict = split_purchases(data, formatted_df)

    print("SPLIT PURCHASES PROGRAM COMPLETE")
    print(
        "------------------------------------------------------------------------------------------------------"
    )

    print(
        "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print("ADDING TO DICTIONARY")
    print(
        "------------------------------------------------------------------------------------------------------"
    )
    # <<<<<<<<WORKING>>>>>>>>>>>
    show_dict = input("PRINT OUT DICT Y/N\n")
    if "y" in show_dict.lower():
        # this saves the newly made dict to json to compare later
        import json
        with open('data/test/dictionary.json', 'w') as save_dict:
            save_dict.write(json.dumps(trans_dict))
        print("DICTIONARY VALUES :::::")
        pp.pprint(trans_dict)
        # exit()
        print(
            "------------------------------------------------------------------------------------------------------"
        )
    converted_DF = dict_to_Frame(trans_dict)
    # if dictionary:
    #     converted_DF = dict_to_Frame(trans_dict, 'dictionary')
    # else:
    #     converted_DF = dict_to_Frame(trans_dict)
    new_DF = test_amounts(converted_DF)
    new_DF = test_date(new_DF)
    print(
        "------------------------------------------------------------------------------------------------------"
    )

    # <<<<<<<<WORKING>>>>>>>>>>>
    # Change this to an input statement attached to the loop
    # Formats amounts and dates if not already formatted
    if data_formatted[1]:
        pass
    else:
        print(
            "------------------------------------------------------------------------------------------------------"
        )
        print("PLEASE ENTER THE COLUMN NAME OF THE DATE")
        col_with_dates = "DATE"
        sort_by = get_sort_by(new_DF, col_with_dates)
        new_DF = new_DF.sort_values(by=sort_by).reset_index(drop=True)
        pp.pprint(new_DF)
        import format_data
        new_DF = format_data.convert_date(new_DF)
        # <<<<<<<<WORKING>>>>>>>>>>>
        # Change this to an input statement attached to the loop
        print("PLEASE ENTER THE COLUMN NAME OF THE AMOUNTS")
        col_with_amounts = "AMOUNTS"
        sort_by = get_sort_by(new_DF, col_with_amounts)
        new_DF = make_num(new_DF, sort_by)

    pp.pprint(new_DF.head())
    create_database = input("ADD TO DATABASE? Y/N \n")
    if "y" in create_database:
        conn_mongo(merged_dict)
        print("MongoDB Successful")
    save_csv(new_DF)
    t_end = datetime.datetime.now()
    t_execute = t_end - t_start
    print(f"PROGRAM EXECUTION TIME {t_execute.total_seconds()/60}")
    return data, new_DF

    #### NEW STUFF aka import_test_data():
    # Comparing a dataframe of new_data with old data
    # dropping duplicates
    # dictionary_DF = (
    #     dict_to_Frame(dictionary).sort_values(
    #         by="date").drop_duplicates().reset_index(drop=True)
    # )

    # print(dictionary_DF.head())
    
    #### Start
    
    
    # saving csv out before matching
    # data = test_date(data)
    # data = data.drop_duplicates().sort_values(
    #     by=['date', 'transaction','amount']).reset_index(drop=True)
    # save_csv(data)
    
    # #by=['date', 'category', 'identifier', 'amount']).drop_duplicates().reset_index(drop=True)
    
    # import format_data
    # import json
    # with open('data/test/dictionary.json') as import_dict:
    #     imported_dict = json.load(import_dict)
    # dictionary_DF = (
    #     dict_to_Frame(imported_dict).drop_duplicates().sort_values(
    #         by=['date', 'transaction', 'amount']).reset_index(drop=True)
    # )
    # dictionary_DF = test_date(dictionary_DF)
    # save_csv(dictionary_DF)
    # #print(dictionary_DF.head())
    # #pp.pprint(dictionary_DF.head())
    # #print(data.head())
    # testing_frames = match_dataframes(data, dictionary_DF)

    # #place to limit data use data.head(num)
    # if imported_dict and testing_frames:
    #     trans_dict = split_purchases(data, formatted_df, imported_dict)
    # else:
    #     trans_dict = split_purchases(data, formatted_df)

    # # Test to see if any data is overlapping, omitting if it is
    # new_data = omit_old_data(imported_dict, trans_dict)
    # if new_data:
    #     from itertools import chain

    #     merged_dict = {}
    #     for k, v in chain(imported_dict.items(), trans_dict.items()):
    #         merged_dict.setdefault(k, []).extend(v)
    # else:
    #     print("THERE IS NO NEW DATA, EXITING")
    #     exit()

    # trans_dict = omit_old_data(trans_dict, imported_dict)
    # print("SPLIT PURCHASES PROGRAM COMPLETE")
    # print(
    #     "------------------------------------------------------------------------------------------------------"
    # )

    # print(
    #     "//////////////////////////////////////////////////////////////////////////////////////////////////////"
    # )
    # print("ADDING TO DICTIONARY")
    # print(
    #     "------------------------------------------------------------------------------------------------------"
    # )
    # # <<<<<<<<WORKING>>>>>>>>>>>
    # show_dict = input("PRINT OUT DICT Y/N\n")
    # if "y" in show_dict.lower():
    #     print("DICTIONARY VALUES :::::")
    #     pp.pprint(merged_dict)
    #     print(
    #         "------------------------------------------------------------------------------------------------------"
    #     )
    # converted_DF = dict_to_Frame(merged_dict)
    # new_DF = test_amounts(converted_DF)
    # new_DF = test_date(new_DF)
    # print(
    #     "------------------------------------------------------------------------------------------------------"
    # )

    # # <<<<<<<<WORKING>>>>>>>>>>>
    # # Change this to an input statement attached to the loop
    # # Formats amounts and dates if not already formatted
    # if data_formatted[1]:
    #     pass
    # else:
    #     print(
    #         "------------------------------------------------------------------------------------------------------"
    #     )
    #     print("PLEASE ENTER THE COLUMN NAME OF THE DATE")
    #     col_with_dates = "DATE"
    #     sort_by = get_sort_by(new_DF, col_with_dates)
    #     new_DF = new_DF.sort_values(by=sort_by).reset_index(drop=True)
    #     pp.pprint(new_DF)
    #     import format_data

    #     new_DF = format_data.convert_date(new_DF)
    #     # <<<<<<<<WORKING>>>>>>>>>>>
    #     # Change this to an input statement attached to the loop
    #     print("PLEASE ENTER THE COLUMN NAME OF THE AMOUNTS")
    #     col_with_amounts = "AMOUNTS"
    #     sort_by = get_sort_by(new_DF, col_with_amounts)
    #     new_DF = make_num(new_DF, sort_by)

    # pp.pprint(new_DF.head())
    # create_database = input("ADD TO DATABASE? Y/N \n")
    # if "y" in create_database:
    #     conn_mongo(merged_dict)
    #     print("MongoDB Successful")
    # save_csv(new_DF)
    # t_end = datetime.datetime.now()
    # t_execute = t_end - t_start
    # print(f"PROGRAM EXECUTION TIME {t_execute.total_seconds()/60}")
    # return data, new_DF


if __name__ == "__main__":
    main()
