#!/usr/bin/env python3su
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

# pip install texthero==1.0.5 works with newer python versions
import numpy as np
import pandas as pd
import re
import time
from calendar import month_abbr
import datetime
#import texthero as hero
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from fastnumbers import fast_float
import pprint
import plotly.graph_objects as go
#import squarify
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib
import platform


import os
# Formatting for output on terminal
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


# working with dates, month abbrev, and the
#  it takes to run prg

# from datetime import datetime
# from datetime import date

# # for importing from excel to pandas
# from pandas import ExcelWriter
# from pandas import ExcelFile

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
    p_slash()
    print("PYTHON VERSIONS")
    print("-----------------------------------------")
    print("python     : ", platform.python_version())
    print("pandas     : ", pd.__version__)
    print("matplotlib : ", matplotlib.__version__)
    print("squarify   :  0.4.3")
    print("-----------------------------------------\n\n")


def getting_terminal_size():
    import os
    size = os.get_terminal_size()
    print(size)


def read_data(file_type):
    p_slash()
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
        if "csv" in import_data.lower() and "y" in query_format.lower():
            # Normalizing the column names to lower
            data = read_data("csv")
            for i in data.columns:
                data = data.rename(columns={i: i.lower()})
            p_line()
            print("CHECKING COLUMNS")
            import format_data
            check_cols = format_data.get_col_names(data)
            data.columns = check_cols[0]
            print(f'\n"{import_data.upper()}" DATASET, ...IMPORT SUCCESS\n')
            print("DATASET SAMPLE")
            p_line()
            pp.pprint(data.head())
            p_line()
            print('\n\n')
            formatted = "formatted"
            
        elif "csv" in import_data.lower() and "n" in query_format.lower():
                # Normalizing the column names to lower
            data = read_data("csv")
            for i in data.columns:
                data = data.rename(columns={i: i.lower()})
            p_line()
            print("CHECKING COLUMNS")
            import format_data
            check_cols = format_data.get_col_names(data)
            data.columns = check_cols[0]
            for i in data.columns:
                data = data.rename(columns={i: i.lower()})
            print(f'\n"{import_data.upper()}" DATASET, ...IMPORT SUCCESS\n')
            print("DATASET SAMPLE")
            p_line()
            pp.pprint(data.head())
            p_line()
            print('\n\n')
            formatted = "formatted"

    elif (
        "clip" in import_data.lower()
        or "format" in query_format.lower()
        or "n" in query_format.lower()
    ):
        format_q = (f'FORMAT "{import_data.upper()}" DATA? Y/N').lower()
        if "n" in format_q.lower():
            p_slash()
            print("RUNNING FORMAT_DATA PROGRAM")
            import format_data

            if "clip" in import_data.lower():
                data = import_clip()
                data = format_data.initiate_format(data)
                for i in data.columns:
                    data = data.rename(columns={i: i.lower()})
                formatted = "formatted"
                print(f'\n"{import_data.upper()}" DATASET...IMPORT SUCCESS\n')
                print("DATASET")
                p_line()
                pp.pprint(data.head())
                formatted = "formatted"

            elif "format" in query_format.lower() or "n" in query_format.lower():
                data = read_data("csv")
                data = format_data.initiate_format(data)
                for i in data.columns:
                    data = data.rename(columns={i: i.lower()})
                formatted = "formatted"
                p_line()
                print(f'"{import_data.upper()}" FORMATED DATASET, ...IMPORT SUCCESS')
                p_line()
                print('RETURNING TO BUDGET PROGRAM')
                p_slash()
                print("DATASET SAMPLE")
                p_line()
                print(data)
                pp.pprint(data.head())
                p_line()
        

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
        p_line()
        pp.pprint(data.head())
        p_line()

    else:
        print("INVALID INPUT, PLEASE TRY AGAIN")
        exit()
    return data, formatted


def import_clip():
    clipDF = pd.read_clipboard()
    p_slash()
    csvName = input("WHAT TYPE OF ACCOUNT FOR FILENAME?\n")
    csvName = csvName + ".csv"
    clipDF.to_csv(csvName, index=False)
    return pd.read_csv(csvName)


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
        
def save_json(dictionary):
    import json
    with open("data_local/test/dictionary.json", "w") as outfile:
        json_string = json.dumps(
            dictionary, default = str, sort_keys=True, indent=2)
        #dictionary, default = lambda o: o.__dict__, sort_keys=True, indent=2)
        outfile.write(json_string)
        #json.dumps(dictionary, outfile)
        
def json_dt_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


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
    p_line()
    print("DATAFRAME")
    p_line()
    pp.pprint(df.head())
    p_line()
    print(f'SORTING BY "{sort_query.upper()}"')
    p_line()
    if sort_query != "CATEGORY DATA":
        print(f'OPTIONS::: {" - ".join(list(df.columns))}')
        p_line()

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
            "conveyance",
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
        # p_slash()
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
    if categories[0].lower() == "0_format" and categories[1].lower == '1_seed':
        p_line()
        cat_list2 = " - ".join([str(x) for x in [*categories[2:]]])
        c_len2 = len(cat_list2)
        print(
            f'CATEGORIES ARE::: "{cat_list2[2:int(c_len2/2)]}\n{cat_list2[int(c_len2/2):]}"'
        )
        p_line()
        p_slash()
    elif categories[0].lower() == "0_format":
        p_line()
        cat_list2 = " - ".join([str(x) for x in [*categories[1:]]])
        c_len2 = len(cat_list2)
        print(
            f'CATEGORIES ARE::: "{cat_list2[:int(c_len2/2)]}\n{cat_list2[int(c_len2/2):]}"'
        )
        p_line()
        p_slash()
    else:
        p_line()
        cat_list3 = " - ".join([str(x) for x in [*categories]])
        c_len3 = len(cat_list3)
        print(
            f'CATEGORIES ARE:::\n"{cat_list3[:int(c_len3/2)]}\n{cat_list3[int(c_len3/2):]}"'
        )
        # print(f'CATEGORIES ARE::: "{" - ".join([str(x) for x in [*categories]])}"')
        p_line()
        p_slash()
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
                    p_slash()
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


#lobal_state = []
global_entry_count_processed = 0
global_entry_count_remaining = 0


def remove_city_state(global_state, tokens_removed):
    import location
    import json
    with open('data/stateAbbrv.json') as state:
        state_dict = json.load(state)
        # print_json = json.dumps(state_dict, indent=4)
    # Removing long form state names
    for i in range(len(tokens_removed)):
        for key, value in state_dict['State'].items():
            if value.lower() == tokens_removed[i].lower():
                tokens_removed[i] = tokens_removed[i].replace(
                    tokens_removed[i], '')

    test_str = ' '.join(tokens_removed)
    # print(f'test_str after both abbv and long state search {test_str}')
    # This searches for City State
    # reg_pattern = r'\b([A-Za-z]+(?: [A-Za-z]+)*) ? ([A-Za-z]{2})\b'
    # removing spaces
    reg_pattern = r'(\b[A-Za-z]+(?:[A-Za-z]+)*) ? ([A-Za-z]{2})\b'
    city_state = re.findall(reg_pattern, test_str,
                            re.IGNORECASE | re.MULTILINE)

    # city_state = re.findall(r"\b([A-Za-z]+(?:[A-Za-z]+)*) ? ([A-Za-z]{2})\b", str2,
    #                       re.IGNORECASE | re.MULTILINE)

    # print(f'{city_state} city_state')
    if len(city_state):
        remove_matches = city_state
        # Testing two letter strings against state db
            # print(print_json)
        test_cs = []
        for i in city_state:
            test_cs.append(list(i))
        for i in range(len(city_state)):
            for key, value in state_dict['Code'].items():
                if value in test_cs[i]:
                    # print(value)
                    # print('search for state loop')
                    # print(test_cs[i])
                    city_state = test_cs[i]
                    # print(city_state)
                    break
                else:
                    # print(city_state[i])
                    # print('not in there')
                    continue
        # print(f'city_state after abbv search {city_state}')
        # print(f'City_state {city_state}')

        # Problem here, its iterating over the word A R L I N G T O N, and V A instead of ARLINGTON, and VA
        remove_city_state = 0
        if len(city_state) >= 2 and type(city_state[0]) == type('s'):
            search_location = location.find_location(
                ' '.join(city_state))
            if search_location:
                remove_city_state = city_state
                count = 0
                match_index = {}
                for match in re.finditer(reg_pattern, test_str):
                    count += 1
                    # print('match', count, match.group(), 'start', match.start(), 'end', match.end())
                    match_index[match.group()] = [
                        match.start(), match.end()]

        elif len(city_state) >= 2 and type(city_state[0]) != type('s'):
            for i in range(len(city_state)):
                search_location = location.find_location(
                    ' '.join(city_state[i]))
                if search_location:
                    remove_city_state = city_state[i]
                    count = 0
                    match_index = {}
                    for match in re.finditer(reg_pattern, test_str):
                        count += 1
                        # print('match', count, match.group(), 'start',match.start(), 'end', match.end())
                        match_index[match.group()] = [
                            match.start(), match.end()]
        else:
            print('something else went wrong')

        if remove_city_state:
            for i in remove_city_state:
                if i.lower() not in global_state:
                    global_state.append(i.lower())
                    # print(f'remove matches {remove_matches}')
                    # print(f'Search_location {search_location}')
                    # print(f'Remove city state {remove_city_state}')
                    # print(match_index)

                    for key, value in match_index.items():
                        if key == ' '.join(remove_city_state):
                            tokens = test_str.replace(
                                test_str[value[0]:value[1]], '')
                    # print(tokens)

                    for key in match_index.keys():
                        for i in key.split():
                            if i in remove_city_state and i != ' ':
                                tokens = tokens.replace(i, '')
                    # print(f'Returning tokens {tokens}')
                    return tokens
                else:
                    test_str = test_str.replace(i, '')
                    # print(f'Replaced {i} in {test_str}')
                    continue
            # print(f'Loop done, returning test_str{test_str}')
            return test_str
        else:
            # print('No city or state1')
            # print(f'Tokens removed1 {test_str}')
            return test_str
    else:
        # print('No city or state2')
        # print(f'Tokens removed2 {test_str}')
        return test_str

# Removing stop words dependencies
# pip install nltk
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

# nltk.download("stopwords")
# nltk.download("punkt")
# Removes most common words


def remove_stop_words(transaction_word_list):
    # if type(transaction_word_list) == type('[]'):
        # transaction_word_list = ' '.join(transaction_word_list)
    # print(f'WORD LIST {transaction_word_list}')
    # removing words like 'the, a, and'
    text_token = word_tokenize(transaction_word_list)
    stop_words = set(stopwords.words("english"))
    # print(f'Text token {text_token}')
    # testing string for address
    tokens_without_sw = [
        word for word in text_token if word.casefold() not in stop_words
    ]
    # print(f'tokens without sw{tokens_without_sw}')
    return tokens_without_sw

# Matches all words anywhere no numbers, no special chars except www, com, sq, tst, bill
# flags are /gmi
# \b([A-Za-z]{3, }+(?: [A-Za-z]+)*)(?<!WWW | COM | SQ | TST | bill)


def add_transaction_type(df, i, global_state, sort_by=0):
    if sort_by:
        # Using re.sub to remove everyting but numbers and words
        # print(f'Sending to Remove Stop Words {df[sort_by][i]}')
        regex_no_state = r"(?!WWW|COM|SQ|TST|bill)\b([A-Za-z]{3,}(?:[A-Za-z]+)*)"
        # print('test1 remove state')
        # print(re.findall(regex_no_state, df[sort_by][i], re.IGNORECASE | re.MULTILINE))

        # Keeps city and state
        # print('test2 remove 3 char words')
        # print(re.sub("/^[A-Za-z0-9]{3,}/", " ", df[sort_by][i]))

        no_city_state = remove_city_state(global_state, df[sort_by][i].split())
        # no_city_state = remove_city_state(
        #     re.sub("/^[A-Za-z0-9]{3,}/", " ", df[sort_by][i]).split())

        if no_city_state:
            if type(no_city_state) == type([]):
                # print('list')
                # print(f'NO city state {no_city_state}, {type(no_city_state)}')
                # print(f" No city state sent to remove stop {remove_stop_words(''.join(no_city_state))}")
                purchase_type = remove_stop_words(' '.join(re.findall(
                    regex_no_state, ' '.join(no_city_state), re.IGNORECASE | re.MULTILINE)))
            elif type(no_city_state) == type('s'):
                # print('string')
                purchase_type = remove_stop_words(' '.join(re.findall(
                    regex_no_state, no_city_state, re.IGNORECASE | re.MULTILINE)))
            else:
                print('SOME KIND OF ERROR IN TYPE')
            # print(f'Purchase type after regex {purchase_type}')

        else:
            # print(f'NO city state {no_city_state}, {type(no_city_state)}')
            purchase_type = remove_stop_words(re.findall(
                regex_no_state, df[sort_by][i], re.IGNORECASE | re.MULTILINE))

        # purchase_type = remove_stop_words(
        #     re.sub("/^[A-Za-z0-9]{3,}/", " ", df[sort_by][i])
        # )
        # p_slash()
        print(f'Purchase type after filters {purchase_type}')
        for index in range(len(purchase_type)):
            if len(purchase_type[index]) < 3:
                sort_by = 'transaction'  # was None to limit the id to > 3 letters but that didn't work
                pass
            else:
                # grabbing the edge cases that the regex fails?
                if purchase_type[index].lower() == 'tst' or purchase_type[index].lower() == 'usa' or purchase_type[index].lower() == 'www' or purchase_type[index].lower() == 'afc':
                    continue
                # NEW STUFF NOT WORKING
                # elif isinstance(purchase_type, str) and purchase_type.lower() in global_state:
                #     purchase_type = df[sort_by][i]
                #     p_slash()
                #     print(
                #         f'TESTING IDENTIFIER:: "{purchase_type}"')
                #     p_slash()
                #     print(
                #         f'SORTING TRANSACTION:: "{str(sort_by).upper()}" BY IDENTIFIER::"{(purchase_type).upper()}"'
                #     )
                #     return sort_by, purchase_type
                # elif (purchase_type[0].isalpha() and purchase_type[1].isalpha()) or (purchase_type[0] in global_state) or (purchase_type[1] in global_state):
                #     p_slash()
                #     print(f'TESTING IDENTIFIER:: "{purchase_type[0] + purchase_type[1]}"')
                #     p_slash()
                #     print(
                #         f'SORTING TRANSACTION:: "{str(sort_by).upper()}" BY IDENTIFIER::"{(purchase_type[0] + purchase_type[1]).upper()}"'
                #     )
                #     first_two = purchase_type[0] + purchase_type[1]
                #     return sort_by, first_two.lower()
                elif purchase_type[index].lower() in global_state:
                    continue
                else:
                    p_slash()
                    print(f'TESTING IDENTIFIER:: "{purchase_type[index]}"')
                    p_slash()
                    print(
                        f'SORTING TRANSACTION:: "{str(sort_by).upper()}" BY IDENTIFIER::"{purchase_type[index].upper()}"'
                    )
                    return sort_by, purchase_type[index].lower()


# def add_transaction_type_confirm(df, i, sort_by=0):
#     if sort_by:
#         purchase_type = df[sort_by][i].replace('*', ' ').split()
#         p_slash()
#         key = ''
#         while 'y' not in key.lower():
#             for index in range(len(purchase_type)):
#                 key = input(
#                     f'SORT THIS PURCHASE BY:: "{purchase_type[index]}", Y/N\n')
#                 if 'y' in key:
#                     p_slash()
#                     print(
#                         f'SORTING TRANSACTION:: "{str(sort_by).upper()}" BY IDENTIFIER::{purchase_type[index].upper()}')
#                     return sort_by, purchase_type[index].lower()
#                 else:
#                     p_slash()
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


def make_dict(categories, cols, old_dict=0):
    # <<<<<<<<WORKING>>>>>>>>>>>
    # look at jupyter notebook with purchases categorized as essential, non essential, fixed, variable, one-time and reoccuring
    # add these into the make dict with new sub categories
    if 'identifier' not in cols:
            cols = cols + ['identifier']
    if 'category' not in cols:
            cols = cols + ['category']
    if type(old_dict) == type({}):
        print('DICT CONFIRMED')
        if "0_format" not in old_dict.keys():
            old_dict["0_format"] = cols
        else:
            if 'identifier' not in old_dict['0_format'] and 'category' not in old_dict['0_format']:
                print('WORKING ON THIS')
                old_dict['0_format'].append('identifier')
                old_dict['0_format'].append('category')
        # Adding new keys to old dictionary
        for i in categories:
            if i not in old_dict.keys():
                old_dict[i] = []
        trans_type = old_dict

    else:
        # Wondering if this is ok because it is the first run, do i need to add identifier and category here?
        trans_type = {"0_format": cols}
        for i in categories:
            trans_type[i] = []
    return trans_type


# <<<<<<<<WORKING>>>>>>>>>>>
# Need to clean up add_Data and search_dict
def search_dict(global_state, budget_dict, data, data_point):  # location is column name
    print(f"SEARCHING DICT FOR {data_point.upper()}")
    if data_point.lower() == "the" or data_point.lower() in global_state:
        pass
    # first searching 1_seed for identifier
    elif '1_seed' in budget_dict.keys():
        for key, value in budget_dict.items():
            if key == '0_format' or key == '1_seed':
                continue
            else:
                for category, identifier in budget_dict['1_seed'].items():
                    for id in identifier:
                        if data_point in id and category == key:
                            p_slash()
                            print(f"DATA POINT IDENTIFIED FROM SEED DATA")
                            print(f'ADDING TO CATEGORY "{key.upper()}"')
                            for x in data:
                                if type(x) == type([]) and len(data) == 1:
                                    return budget_dict, "identified"
                                elif type(x) == type([]) and len(data) > 1:
                                    value.append(x + [key])
                                else:
                                    value.append(data + [key])
                                    return budget_dict, "identified"            
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
                                p_slash()
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

def mostly_alpha(string):
    counter = 0
    length = len(string)
    for i in string:
        if i.isnumeric():
            # print(counter)
            # print(i)
            counter += 1
    percent_nums = round(counter/length * 100)
    return percent_nums


# <<<<<<<<WORKING>>>>>>>>>>>
# Need to format location input into a prettier line of code
def add_data(budget_dict, data):
    p_slash()
    print("RUNNING ADD DATA")
    p_slash()
    cat_options2 = " - ".join(sorted(list(budget_dict.keys()))[1:])
    len_cat = int(len(cat_options2) / 2)
    # formatting print statement to only print transaction data
    # print(f'printing trans {data}')
    # print(type(data[0]))
    # Assuming that the transaction info is the longest str
    # Additional removing the strs with timestamp and mostly numbers
    if isinstance(data, list) and isinstance(data[0], list):
        print_trans = max([str(i) for i in data[0] if ('Timestamp' not in str(i)) and (mostly_alpha(str(i)) < 65)], key=len)
    elif isinstance(data, list):
        print_trans = max([str(i) for i in data if (
            'Timestamp' not in str(i)) and (mostly_alpha(str(i)) < 65)], key=len)
    else:
        print_trans = max([str(i) for i in data if (mostly_alpha(str(i)) < 65)], key=len)
    print(
        f"\n{print_trans} CHOOSE CATEGORY::: \n------------------------------------------------------------------------------------------------------\nCATEGORY OPTIONS:: {cat_options2[:len_cat]}\n{cat_options2[len_cat:]}\n------------------------------------------------------------------------------------------------------\n")
    location = str(
        input("CHOICE? \n"))
    sub_keys = {
        'food': 'groceries',
        'foo': 'groceries',
        'fast food': 'take away',
        'fast': 'take away',
        'travel': 'holiday',
        'trav': 'holiday',
        'transportation': 'conveyance'
    }

    for sub_key, sub_value in sub_keys.items():
        if location.lower() == sub_key:
            print(
                f'SWITCHING {location.upper()} WITH {sub_value.upper()}, {location.upper()} IS A DOUBLE MATCH')
            location = sub_value

    # Adding a new key if the entered key is not already in the dictionary or part of defaults
    if location[:3] not in [i[:3] for i in budget_dict.keys()] and (location != "0_format") and (location != '1_seed'):
            add_key = input(
                f'"{location}":: NOT IN BUDGET FILE, WOULD YOU LIKE TO ADD IT? Y/N\n'
            )
            if "y" in add_key:
                print(f'ADDITION TO "{location.upper()}" SUCCESSFUL')
                budget_dict[location] = []
            else:
                location = 'other'
                budget_dict[location] = []
                print(f'ADDING TO "{location.upper()}" SUCCESSFUL')
    #Matching the location input for the item to corresponding key
    for key, value in budget_dict.items():
        if location[:3] == key[:3]:
            print(
                f'YOU ENTERED "{location.upper()}" WE ARE MATCHING TO "{key.upper()}"'
            )
            if type(data[0]) != type([]):
                value.append(data + [key])
                p_slash()
                print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
                return budget_dict
            elif type(data[0]) == type([]) and len(data) > 1:
                for z in data:
                    z.append(key)
                    value.append(z)
                p_slash()
                print(f'ADDITION TO "{key.upper()}" SUCCESSFUL')
                return budget_dict
            else:
                print("ERROR SKIPPING")
    return budget_dict


def split_purchases(df, global_state, formatted_df=0, budget_dict=0):
    global_entry_count_remaining = len(df)
    global_entry_count_processed = 0
    # cols = confirm_cols(df, formatted_df)
    # pp.pprint(df)
    print("BEGIN PURCHASE CATEGORIZATION")
    p_line()
    # if statement separates data if a correctly formatted dictionary is passed to it
    # else it creates a dictionary
    if type(budget_dict) == type({}):
        cols = confirm_cols(df, formatted_df)
        categories = get_categories(list(budget_dict.keys()))
        trans_type = make_dict(categories, cols, budget_dict)
        sort_by = get_sort_by(df, "CATEGORY DATA")
        print(f'SORT BY "{sort_by.upper()}" WITH DICT')
        p_line()

    else:
        cols = confirm_cols(df, formatted_df)
        categories = get_categories()
        trans_type = make_dict(categories, cols)
        sort_by = get_sort_by(df, "CATEGORY DATA")
        print(f'SORT BY "{sort_by.upper()}" WITHOUT DICT')
        p_line()

    skip_rows = []
    for i in range(len(df)):
        if i not in skip_rows:
            p_line()
            print(
                f'{global_entry_count_remaining - len(skip_rows)} ROWS REMAINING TO IDENTIFY OUT OF {len(df)}')
            p_line()
            #print(df.iloc[[i]])
            #print(sort_by)
            get_col = add_transaction_type(df, i, global_state, sort_by)
            # The regex is not perfect, adding to grab just the first word grouping as the key if add_trans doesn't work
            if get_col == None:
                identity = df['transaction'][i].split()[0]
            else:
                identity = get_col[1]
            # NEED TO ADD A TYPE TEST BEFORE THIS
            # print(identity)
            # print(df.select_dtypes(
            #     include=["object"], exclude=["float64", "int64", "datetime"]
            # ))
            mask = df.select_dtypes(
                include=["object"], exclude=["float64", "int64", "datetime"]
            ).apply(lambda x: x.astype(str).str.contains(rf"{identity}", na=False, case=False))
            # mask = df.apply(lambda x: x.str.contains(rf'{identity}', na=False, case=False))
            matching_rows = df.loc[mask.any(axis=1)]
            skip_rows += matching_rows.index.tolist()

            # print(matching_rows)
            if len(matching_rows) >= 2:
                #global_entry_count_processed += global_entry_count_remaining - len(matching_rows)
                print(f"{len(matching_rows)} ROWS MATCHED IN IMPORTED DATA:::")
                # print('ROWS MATCH\n')
                data = []
                for rows in matching_rows.index.tolist():
                    data.append(list(df.iloc[rows]) + [identity])
                # pp.pprint(data)
            else:
                data = []
                print("NO MATCH IN IMPORTED DATA:::")
                #global_entry_count_processed += global_entry_count_remaining - \len(matching_rows)
                for col in cols:
                    data.append(df.iloc[i][col])
                data.append(identity)
                # pp.pprint(data)

        else:
            continue
        # print(identity)
        searched_dict = search_dict(global_state, trans_type, data, identity)
        new_dict = searched_dict[0]
        if "identified" not in searched_dict[1].lower():
            budget_dict = add_data(new_dict, data)
    p_slash()
    print("PROGRAM COMPLETE")
    p_slash()
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


def test_date(df, test_dict=0):
    # testing all columns with the word date
    # if test in list col num and list_cols comprehension are redundant too tired to fix
    p_slash()
    print('TESTING DATES')
    p_slash()
    if isinstance(test_dict, dict):
        print('CHECKING DICTIONARY VALUES FOR DATES')
        p_slash()
        list_cols = test_dict['0_format']
        test_cols = ["date", "pending", "posted"]
        date_indici = []
        #print(list_cols)
        
        for col_indici in range(len(list_cols)):
            for test in test_cols:
                #print(f'SORTING OUT COLS WITH DATE INFO {test.upper()}')
                #Somehow skipping out of the loop here to next if statement
                #print(test)
                #print(col_indici)
                if test in list_cols[col_indici]:
                    #print(list_cols[col_indici])
                    date_indici.append(col_indici)
                else:
                    #print(f'SKIPPING {list_cols[col_indici]}')
                    continue
        #print(date_indici)         
        for key, value in test_dict.items():
            if key == '0_format' or key == '1_seed':
                #print('SKIPPING FORMATTING DATA')
                continue
            elif len(value) == 0:
                #print(f'{key} IS EMPTY SKIPPING')
                continue
            else:
                for data in value:
                    for indici in date_indici:
                        #print('CONVERTING DICTIONARY DATES TO DATETIME')
                        #print(data)
                        #print(indici)
                        try:
                            #print(data[indici])
                            data[indici] = datetime.datetime.strptime(data[indici], '%Y-%m-%d %H:%M:%S')
                        except TypeError:
                            #print('DATA IS ALREADY IN DATETIME')
                            continue
                        #print(data)
        #pp.pprint(test_dict)
        return test_dict       
    if isinstance(df, pd.DataFrame):
        #print('CHECKING DATAFRAME VALUES')
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
                #print("CONVERTING DATAFRAME DATES TO DATETIME")
                #p_slash()
                try:
                    df[tested] = pd.to_datetime(df[tested])
                #     df[tested] = pd.to_datetime(
                #         df[tested], format='%Y-%m-%d %H:%M:%S')
                # df[tested].map(datetime.strptime())
                except ValueError:
                    print('Some kind of error')
                #     df[tested] = pd.to_datetime(
                #         df[tested], format='%m/%d/%Y %H:%M:%S')
        # pp.pprint(df)
        return df




# def test_date(df):
#     # testing all columns with the word date
#     # if test in list col num and list_cols comprehension are redundant too tired to fix
#     p_slash()
#     print('TESTING DATES')
#     p_slash()
#     list_cols = [i.lower() for i in df.columns.tolist()]
#     test_cols = ["date", "pending", "posted"]
#     verified_cols = []
#     for col in list_cols:
#         for test in test_cols:
#             if test in col:
#                 verified_cols.append(col)
#     # print(verified_cols)
#     for tested in verified_cols:
#         if all(df[tested].map(type) != type(datetime.datetime.now())):
#             # add second conditional here that tests the col for floats, ints and strings
#             print("CONVERTING DATAFRAME DATES TO DATETIME")
#             p_slash()
#             df[tested] = pd.to_datetime(df[tested])
#     # pp.pprint(df)
#     return df


def test_amounts(df):
    p_line()
    p_slash()
    print('TESTING AMOUNTS')
    p_slash()
    # converted_col = []
    list_cols = [i.lower() for i in df.columns.tolist()]
    test_cols = ["amount", "value", "balance", "price", "cost", "dollars", "total"]
    verified_cols = []
    for col in list_cols:
        for test in test_cols:
            if test in col:
                verified_cols.append(col)
    # print(verified_cols)
    for tested in verified_cols:
        search_floats = df[tested].apply(
            lambda x: 'True' if isinstance(x, float) else 'False')
        if not search_floats.any():
            #print('COLUMNS ARE FLOATS SKIPPING')
            continue
        elif (df[tested].map(type) == str).all():
            # add second conditional here that tests the col for floats, ints and strings
            print("NORMALIZING AMOUNTS")
            p_slash()
            converted_col = []
            for row_num in range(len(df)):
                converted_col.append(convert_amount(
                    df[tested][row_num]))
            df[tested] = converted_col
        elif search_floats.all():
            continue
            #print('COLUMNS ARE ALL FLOATS SKIPPING')
        else:
            print(f'your {tested} columns are all a mess, see your programmer')
    return df


# trying to find the difference between the two dataframes
# there must be a strip function buried in there and some spaces or special characters that i cant find
# so that the rows do not match
def match_dataframes(new_DF, old_DF):
    
    # Cutting off all other columns old dataframe will have categories, new will not at this point
    list_match = ["date", "transaction", "amount"]
    for i in list_match:
        if i in list(new_DF.columns) and i in list(old_DF.columns):
            test_merge_old = old_DF.loc[:, list_match].convert_dtypes()
            test_merge_new = new_DF.loc[:, list_match].convert_dtypes()
    # print(test_merge_new.head())
    # print(test_merge_old.head())

    # this came back with 12ish rows?  should be 0 with identical data
    match_not_in_new = test_merge_old[~test_merge_old.index.isin(
        test_merge_new.index)].reset_index(drop=True)
    # print('OLD NOT IN NEW')
    # print(len(match_not_in_new))
    # print(match_not_in_new)

    # This came back empty
    match_not_in_old = test_merge_new[~test_merge_new.index.isin(
        test_merge_old.index)].reset_index(drop=True)
    # print('NEW NOT IN OLD')
    # print(len(match_not_in_old))
    # print(match_not_in_old)

    # tests if the dataframes are exact equals
    equal = test_merge_old.equals(test_merge_new)
    p_line()
    print(f'DUPLICATED DATA? {str(equal).upper()}')
    p_line()
    #ie are they equal

    test_concat = pd.concat(
        [test_merge_old, test_merge_new]).drop_duplicates().reset_index(drop=True)
    #print('CONCAT W/ DROP')
    # print(len(test_concat))
    #print(test_concat.head())
    data_dups = len(test_concat)
    duplicate_rows = [g for _, g in test_concat.groupby(
        list(test_concat.columns)) if len(g) > 1]
    if duplicate_rows:
        duplicates = pd.concat(g for _, g in test_concat.groupby(
            list(test_concat.columns)) if len(g) > 1)
        print(f' There are {len(duplicates)/2} duplicated rows, Removing')
        data = test_concat.drop_duplicates().sort_values(
            by=['date', 'transaction', 'amount']).reset_index(drop=True)
        print(f'Removed {len(data) - data_dups} from original dataframe')
    # If equal is true, dataframes are the same passing false to exit split purchases
    # If equal is false, new_DF has new data, passing to split purchases
    if equal:
        return True, old_DF
    else:
        return False, new_DF


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


def dict_to_Frame(data_dict):
    #pp.pprint(data_dict)
    import format_data as format
    print("PROCESSING DATAFRAME")
    skip_list = []
    rows = []
    # print(data_dict['0_format'])
    if "category" not in data_dict["0_format"]:
        data_dict["0_format"] = data_dict["0_format"] + ["category"]
    else:
        pass
    cols = data_dict["0_format"]
    for key, value in data_dict.items():
        # Skipping the first entry which is the columns
        if key == "0_format" or key == '1_seed':
            #p_slash()
            #print("SKIPPING FORMATTING ROWS")
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
    # PLACE TO ADD EXTRA COLUMNS
    # pp.pprint(rows)
    # print(cols)
    # pp.pprint(data_dict)
    df = pd.DataFrame(
        np.array(rows), columns=cols).drop_duplicates().reset_index(drop=True)
    skip_list_p = ", ".join(skip_list)
    len_skip = int(len(skip_list_p) / 2)
    p_line()
    print(
        (
            f"NO AVAILABLE DATA, SKIPPING CATEGORIES IN DATAFRAME:::\n{skip_list_p[:len_skip]}\n{skip_list_p[len_skip:]}"
        )
    )
    # place to add convert date from format_data to make all rows datetime objs
    # df = format.convert_date(df)
    return df


def dict_to_Frame_with_data(data_dict):

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
        if key == "0_format" or key=='1_seed':
            p_slash()
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
    p_slash()
    # PLACE TO ADD EXTRA COLUMNS
    # pp.pprint(rows)
    df = pd.DataFrame(
        np.array(rows), columns=cols).drop_duplicates().reset_index(drop=True)
    skip_list_p = ", ".join(skip_list)
    len_skip = int(len(skip_list_p) / 2)
    p_line()
    print(
        (
            f"NO AVAILABLE DATA, SKIPPING CATEGORIES IN DATAFRAME:::\n{skip_list_p[:len_skip]}\n{skip_list_p[len_skip:]}"
        )
    )
    # place to add convert date from format_data to make all rows datetime objs
    # import format_data as format
    # df = format_data.convert_date(df)
    return df


# <<<<<<<<WORKING>>>>>>>>>>>
# Adding PYMONGO DB functionality
# Need to add a print statement, also pymongo install based on the users OS
# For consistent use of program need to add searchability for date and transaction type that the db connection only adds if the data is new

# Notes https://docs.mongodb.com/manual/reference/method/db.collection.find/
# https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/

def make_seed_data(df):
    # Add this in after each run of data
    # making seed data
    seed_data = {}
    for index, row in df.iterrows():
        if row['category'] not in seed_data.keys():
            seed_data[row['category']] = []  # [row['identifier']]
        if row['identifier'] not in seed_data[row['category']]:
            seed_data[row['category']].append(row['identifier'])
    return seed_data


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

def get_surrounding_locals():
    import location
    p_slash()
    print("LOCATION QUERY")
    p_slash()
    p_line()
    address = input('WHAT IS YOUR ADDRESS\n')
    p_line()
    p_slash()
    print('UPDATING LOCATION IN PROGRESS........PLEASE WAIT THIS CAN TAKE UP TO A MINUTE')
    p_slash()
    global_state = location.remove_location(address)
    return global_state

def main():
    global_entry_count_remaining = 0
    #-----------------------------------------------------------------------------------------------------------
    # Starting the timer
    #-----------------------------------------------------------------------------------------------------------
    t_start = datetime.datetime.now()
    #-----------------------------------------------------------------------------------------------------------
    # Asking for address to create the list of city, states to remove from transaction
    #-----------------------------------------------------------------------------------------------------------
    timer_s = datetime.datetime.now()
    global_state = get_surrounding_locals()
    timer_end = datetime.datetime.now()
    print(f"PROGRAM EXECUTION TIME {(timer_end - timer_s).total_seconds()/60}")
    #print(global_state)
    #-----------------------------------------------------------------------------------------------------------
    # # Getting new data, initiating the program
    #-----------------------------------------------------------------------------------------------------------
    p_slash()
    print("RUNNING GET DATA TYPE")
    p_slash()
    formatted_df = None
    data_formatted = get_data_type()
    data = data_formatted[0]
    if data_formatted[1]:
        p_slash()
        print(f"CONFIRMED DATA IS {data_formatted[1].upper()}")
        formatted_df = data_formatted[1]
        
    #-----------------------------------------------------------------------------------------------------------
    # Checking Amount and Date Columns from New Data
    #-----------------------------------------------------------------------------------------------------------
    no_dict = 0
    data = test_date(data, no_dict)
    data = test_amounts(data)
    data_dups = len(data)
    
    #-----------------------------------------------------------------------------------------------------------
    # Testing for Duplicate Rows from New Data
    #-----------------------------------------------------------------------------------------------------------
    duplicate_rows = [g for _, g in data.groupby(
        list(data.columns)) if len(g) > 1]
    if duplicate_rows:
        duplicates = pd.concat(g for _, g in data.groupby(
            list(data.columns)) if len(g) > 1)
        print(f' There are {len(duplicates)/2} duplicated rows, Removing')
        data = data.drop_duplicates().sort_values(
            by=['date', 'transaction', 'amount']).reset_index(drop=True)
        print(f'Removed {len(data) - data_dups} from original dataframe')
    
    #-----------------------------------------------------------------------------------------------------------
    # Bringing in Database Data as Dictionary --- Pulling in Dictionary as JSON, sub for importing from mongoDB when ready
    #-----------------------------------------------------------------------------------------------------------
    imported_dict = None
    import format_data
    import json
    try:
        with open('data_local/test/dictionary.json') as import_dict:
            raw_dict = json.load(import_dict)
    except:
        p_line()
        p_slash()
        print('FILE DOES NOT EXIST')
        p_slash()
        import_dict = None
        dictionary_DF = None
        raw_dict = None
        
    if raw_dict:
        #pp.pprint(raw_dict)
        p_line()
        p_slash()
        print('IMPORTING JSON DICT CONVERTING TO DF')
        empty_df = 0
        imported_dict = test_date(empty_df, raw_dict)
        #pp.pprint(imported_dict)
        dictionary_DF = (
            dict_to_Frame(imported_dict).drop_duplicates().sort_values(
                by=['date', 'transaction', 'amount']).reset_index(drop=True)
        )
        no_dict = 0
        #dictionary_DF = test_date(dictionary_DF, no_dict)
        dictionary_DF = test_amounts(dictionary_DF)
        

    #-----------------------------------------------------------------------------------------------------------
    # Comparing DataFrames from DB and new Data
    #-----------------------------------------------------------------------------------------------------------
    # Default for testing frames is False or None because the default is no old data
    testing_frames = False
    if dictionary_DF is not None:
        testing_frames = match_dataframes(data, dictionary_DF)

    #-----------------------------------------------------------------------------------------------------------
    # Sending new dataframe to split purchases
    #-----------------------------------------------------------------------------------------------------------
    # place to limit data use data.head(num)
    #pp.pprint(imported_dict)
    #print(testing_frames[1].head(5))
    # If there is both a Database file, and a True Value 
    p_line()
    global_entry_count_remaining = len(data)
    print(f'EVALUATING {global_entry_count_remaining} LINES OF DATA')
    p_line()
    if imported_dict and (testing_frames[0] == False):
        p_slash()
        print("RUNNING SPLIT PURCHASES PROGRAM 1")
        p_line()
        trans_dict = split_purchases(data.head(), global_state, formatted_df, imported_dict)
        
    elif imported_dict and (testing_frames[0] == True):
        p_slash()
        print("THERE IS NO NEW DATA, EXITING")
        p_slash()
        exit()
        
    else:
        print('FIRST RUN')
        p_slash()
        print("RUNNING SPLIT PURCHASES PROGRAM 2")
        p_line()
        trans_dict = split_purchases(data.head(), global_state, formatted_df)
    final_dict = trans_dict
    
    
    #-----------------------------------------------------------------------------------------------------------
    # This is not working, a little too complicated when considering there will be different columns, and it does not omit duplicated data
    #-----------------------------------------------------------------------------------------------------------
    
    # Test to see if any data is overlapping, omitting if it is
    if imported_dict:
        print('TESTING IMPORTED DATA FOR DUPLICATES\n')
        new_data = omit_old_data(imported_dict, trans_dict)
        # print('\n\n\n')
        # pp.pprint(new_data)
        # print('\n\n\n')
        # pp.pprint(imported_dict)
        # print('\n\n\n')
        # pp.pprint(trans_dict)
        # if new_data:
        #     from itertools import chain
        #     merged_dict = {}
        #     for k, v in chain(imported_dict.items(), trans_dict.items()):
        #         merged_dict.setdefault(k, []).extend(v)
        # else:
        #     print("THERE IS NO NEW DATA, EXITING")
        #     exit()
        # trans_dict = omit_old_data(trans_dict, imported_dict)
        # print('TRANS DICT')
        # pp.pprint(trans_dict)
        # print('MERGED DICT')
        # pp.pprint(merged_dict)
        # final_dict = merged_dict
        
    print("SPLIT PURCHASES PROGRAM COMPLETE")
    p_line()

    p_slash()
    print("ADDING TO DICTIONARY")
    p_line()
    # <<<<<<<<WORKING>>>>>>>>>>>
    
    converted_DF = dict_to_Frame(final_dict)
    new_DF = test_amounts(converted_DF)
    no_dict = 0
    new_DF = test_date(new_DF, no_dict)
    seed_categories = make_seed_data(converted_DF)
    final_dict['1_seed'] = seed_categories
    show_dict = input("PRINT OUT DICT Y/N\n")
    if "y" in show_dict.lower():
        print("DICTIONARY VALUES :::::")
        pp.pprint(final_dict)
        p_line()
    p_line()
    save_dict = input("SAVE DICT TO JSON Y/N\n")
    if "y" in save_dict.lower():
        save_json(final_dict)
        p_line()
    p_line()

    # <<<<<<<<WORKING>>>>>>>>>>>
    # Change this to an input statement attached to the loop
    # Formats amounts and dates if not already formatted
    if data_formatted[1]:
        pass
    else:
        p_line()
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
        conn_mongo(final_dict)
        print("MongoDB Successful")
    save_csv(new_DF)
    t_end = datetime.datetime.now()
    t_execute = t_end - t_start
    print(f"PROGRAM EXECUTION TIME {t_execute.total_seconds()/60}")
    return data, new_DF


if __name__ == "__main__":
    main()
    

