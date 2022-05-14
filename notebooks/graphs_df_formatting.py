#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import os
import datetime
from colour import Color
from colr import color
import pprint
pp = pprint.PrettyPrinter(indent=4)

#Graphs have to have datetime dates
def convert_date(df):
    import datetime
    list_cols = [i.lower() for i in df.columns.tolist()]
    test_cols = ["date", "day", "time", "occurrence"]
    verified_cols = []
    for col in list_cols:
        for test in test_cols:
            if test in col:
                verified_cols.append(col)
    for tested in verified_cols:
        search_dates = df[tested].apply(
            lambda x: 'True' if isinstance(x, datetime.date) else 'False')
        if not search_dates.any():
            #p_slash()
            print('ALL DATES ARE IN DATETIME SKIPPING')
            #p_slash()
            continue
        elif (df[tested].map(type) == str).all():
            date_time = []
            for j in df[tested]:
                if len(j) == 10 and '/' in j:
                    date_time.append(
                        datetime.datetime.strptime(j, "%m/%d/%Y"))
                elif len(j) == 8 and '/' in j:
                    date_time.append(
                        datetime.datetime.strptime(j, "%m/%d/%y"))
                elif len(j) == 10 and '-' in j:
                    date_time.append(
                        datetime.datetime.strptime(j, "%Y-%m-%d"))
                else:
                    print("UNKNOWN DATE FORMAT SKIPPING FORMATTING")
                    return df
            df[tested] = date_time
            df[tested] = pd.to_datetime(df[tested]).apply(lambda x: x.date())
            df = df.sort_values(
                by=[tested]).reset_index(drop=True)
            # Want to use sort_values by tested, however, because its a loop it wont choose the primary date col
            # df = df.sort_values(
            #     by=['date', 'transaction', 'amount']).reset_index(drop=True)
            # (by=['date', 'category', 'identifier', 'amount']
        else:
            print('your dates are a mess, see your programmer')
    return df


def graph_data_formatting(data_df):
    #format dates to datetime
    data_df = convert_date(data_df)
    
    # Adding a numerical day for data, and a word value for day of week
    data_df['day'] = pd.DatetimeIndex(data_df['date']).day
    data_df['long_day'] = list(map(lambda x: datetime.datetime.strptime(
        str(x), "%d").strftime("%A"), data_df['day']))

    # Adding a numerical value col for month and a word value for mo
    data_df['month'] = pd.DatetimeIndex(data_df['date']).month
    data_df['long_month'] = list(map(lambda x: datetime.datetime.strptime(
        str(x), "%m").strftime("%B"), data_df['month']))

    # Fixing order
    reorder = data_df[['month', 'day']].copy(deep=True)
    data_df = data_df.drop(columns=['month', 'day'])
    data_df['month'] = reorder['month']
    data_df['day'] = reorder['day']
    
    #remove payment and interest as categories
    #these will go somewhere else
    if 'category' in data_df.columns or 'Category' in data_df.columns:
        if 'payment' in data_df['category']:
            data_df = data_df.loc[data_df['category'] != 'payment']
        if 'interest' in data_df['category']:
            data_df = data_df.loc[data_df['category'] != 'interest']
    
    #Getting whole month total for spending all categories
    if 'category' in data_df.columns:
        month_sum = (data_df.groupby(['month', 'long_month'])['amount'].sum()).to_frame(name='month_sum').reset_index()
        month_categories = (data_df.groupby(['month', 'category', 'long_month'])[
                            'amount'].sum()).to_frame(name='month_sum').reset_index()
    else:
        month_sum = (data_df.groupby(['month', 'long_month'])['amount'].sum()).to_frame(name='month_sum').reset_index()
        month_categories = (data_df.groupby(['month', 'long_month'])[
                            'amount'].sum()).to_frame(name='month_sum').reset_index()
    
    #Getting whole month spending by category
    month_categories = month_categories.sort_values(
        by=['month', 'month_sum']).reset_index(drop=True)
    
    cat_order = month_categories.sort_values(
        by=['month', 'category']).reset_index(drop=True)

    pos_amount = [i*-1 for i in cat_order['month_sum']]

    return data_df, cat_order, pos_amount
