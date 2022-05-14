#!/usr/bin/env python3
# coding: utf-8

import os
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
pio.renderers.default = 'jpg'

# Orca must be installed?
# conda install -c plotly plotly-orca
# Kaleido is for exporting images from plotly
# pip install -U kaleido

if not os.path.exists('images'):
    os.mkdir('images')


# Colors
rainbow_colors = ['#F94144', '#f3722c', '#F9844A', '#f8961e','#F9C74F', '#90BE6D', '#43AA8B', '#4D908E', '#277DA1', '#577590']
ainbow_colors = ['#F94144', '#f3722c', '#F9844A', '#f8961e','#F9C74F', '#90BE6D', '#43AA8B', '#4D908E', '#277DA1', '#577590']
print(len(rainbow_colors))

red_orange = ['#F94144', '#F94A40', '#F9543C', '#F95D37','#F96733', '#F8702F', '#F87A2B', '#F88326', '#F88D22', '#F8961E']
orange_yellow = ['#F89B23', '#F8A129', '#F8A62E', '#F8AC34', '#F9B139', '#F9B73F', '#F9BC44', '#F9C24A', '#F9C74F']
yellow_green = ['#EDC652', '#E2C556', '#D6C459', '#CAC35C',
                '#BFC260', '#B3C163', '#A7C066', '#9CBF6A', '#90BE6D', ]
green_cyan = ['#88BC70', '#87BC70', '#7FBA74', '#76B777','#6EB57A', '#65B37E', '#55B082', '#54AE84', '#4CAC88']
cyan_deepcyan = ['#43AA8B', '#44A78B', '#45A48C', '#479E8C','#499C8D', '#4A998D', '#4B968D', '#4C968D', '#4D908E']
deepcyan_blue = ['#498E90', '#458C92', '#408A94', '#3C8896','#388599', '#34839B', '#2F819D', '#2B7F9F', '#277DA1']
blue_darkblue = ['#2C7C9F', '#327B9D', '#377A9B', '#3C7999','#427998', '#477896', '#4C7794', '#527692', '#577590']

gradient = red_orange + orange_yellow + yellow_green + \
    green_cyan + cyan_deepcyan + deepcyan_blue + blue_darkblue
# Stacked Bar Graph


def make_stacked_bar_graph(data_df, cat_order, pos_amount):
    #month_categories is a df grouped
    # pos_amount is a list of the positive dollars spent
    # cat_order is an ordered dataframe by month and category
    month_categories = (data_df.groupby(['month', 'category', 'long_month'])[
                        'amount'].sum()).to_frame(name='month_sum').reset_index()
    import plotly.express as px
    fig = px.bar(month_categories,
                x=cat_order['long_month'], y=pos_amount,
                color=cat_order['category'],
                color_discrete_sequence=gradient[:len(
                    cat_order['category'])][::-1],
                labels={
                    "x": "Month",
                    "color": 'Category',
                    "y": "Amount",
                },
                title="Total Spending by Category by Month")
    fig.update_layout(
        bargap=0.15)
    fig.show()
