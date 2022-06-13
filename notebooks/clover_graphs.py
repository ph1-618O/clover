#!/usr/bin/env python3
# coding: utf-8

from colr import color
from colour import Color
import os
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'jpg'

# Orca must be installed?
# conda install -c plotly plotly-orca
# Kaleido is for exporting images from plotly
# pip install -U kaleido

if not os.path.exists('images'):
    os.mkdir('images')


# Colors
red = 'tomato'
coral = 'FF8360'
pastel_pink = 'DA9598'
rajah = 'FFAA5A'
light_red = 'ED6A5A'
soft_colors = [light_red, 'lightsalmon', rajah, 'gold',
            'lightgreen', 'mediumturquoise', 'lightblue', 'lightgray', 'white']
contrast_colors = colors = ['tomato', 'lightsalmon', 'darkorange', 'gold',
                            'lightgreen', 'mediumturquoise', 'lightblue', 'lightgray', 'white']
rainbow_colors = ['#F94144', '#f3722c', '#F9844A', '#f8961e',
                '#F9C74F', '#90BE6D', '#43AA8B', '#4D908E', '#277DA1', '#577590']
rainbow_colors = ['#F94144', '#f3722c', '#F9844A', '#f8961e',
                '#F9C74F', '#90BE6D', '#43AA8B', '#4D908E', '#277DA1', '#577590']
print(len(rainbow_colors))

red_orange = ['#F94144', '#F94A40', '#F9543C', '#F95D37',
            '#F96733', '#F8702F', '#F87A2B', '#F88326', '#F88D22', '#F8961E']
orange_yellow = ['#F89B23', '#F8A129', '#F8A62E', '#F8AC34',
                '#F9B139', '#F9B73F', '#F9BC44', '#F9C24A', '#F9C74F']
yellow_green = ['#EDC652', '#E2C556', '#D6C459', '#CAC35C',
                '#BFC260', '#B3C163', '#A7C066', '#9CBF6A', '#90BE6D', ]
green_cyan = ['#88BC70', '#87BC70', '#7FBA74', '#76B777',
            '#6EB57A', '#65B37E', '#55B082', '#54AE84', '#4CAC88']
cyan_deepcyan = ['#43AA8B', '#44A78B', '#45A48C', '#479E8C',
                '#499C8D', '#4A998D', '#4B968D', '#4C968D', '#4D908E']
deepcyan_blue = ['#498E90', '#458C92', '#408A94', '#3C8896',
                '#388599', '#34839B', '#2F819D', '#2B7F9F', '#277DA1']
blue_darkblue = ['#2C7C9F', '#327B9D', '#377A9B', '#3C7999',
                '#427998', '#477896', '#4C7794', '#527692', '#577590']

gradient = red_orange + orange_yellow + yellow_green + \
    green_cyan + cyan_deepcyan + deepcyan_blue + blue_darkblue

def test_color():
    start = Color("#F94144")
    colors = list(start.range_to(Color("#CAC35C"), 20))
    str(colors[1])


    color_list = []
    for i in range(len(colors)):
        color_list.append(str(colors[i]))

    print(color('test', fore='F94144', back='000'))

    for i in gradient:
        print(color('■', fore=i, back='000'), end='')

    for i in gradient:
        print(color(f'{i}', fore=i, back='000'), end='')

    #help('colour')

    for i in colors:
        print(color('■', fore=str(i), back='000'), end='')

    rainbow_colors = ['#F94144', '#f3722c', '#F9844A', '#f8961e',
        '#F9C74F', '#90BE6D', '#43AA8B', '#4D908E', '#277DA1', '#577590']
    # color= rainbow_colors[:len(cat_order['category'])+1]
# Stacked Bar Graph

# Category types
fixed = {
    'debt': ['car loan', 'student loan/tution'],
    'housing': ['home owners insurance', 'renters insurance', 'rent', 'mortgage', 'property taxes'],
    'utilities': ['cable', 'internet', 'garbage'],
    'medical': ['health insurance'],
    'childcare': ['daycare', 'child support'],
    'entertainment': ['streaming services']
}

variable = {
    'utilities': ['water', 'electricity', 'gas', 'phone']
}

essentials = {
    'savings': ['life insurance', 'emergency fund', 'ROTH IRA', '401(k)', 'college fund', 'mad money'],
    'debt': ['credit card', 'car loan', 'student loan', 'tuition', 'pay day loan', 'other'],
    'domicile': ['home', 'renters insurance', 'home insurance', 'rent', 'mortgage', 'repair', 'maitenance', 'furnishings', 'property taxes', 'yard', 'cleaning supply', 'kitchen ware', 'tools'],
    'transportation': ['car insurance', 'maintenance', 'gas' 'bus', 'subway', 'train', 'ferry fare'],
    'food': ['groceries'],
    # oil, wood
    'utilities': ['phone', 'cable', 'internet', 'water', 'gas', 'electricity', 'garbage', 'utility'],
    # types of doctors, optometrist, dentist, etc
    'medical': ['health insurance', 'doctor', 'prescriptions', 'first aid supply', 'appointment'],
    'education': ['supplies', 'fees', 'books'],
    'childcare': ['daycare', 'camps', 'babysitter', 'child support'],
    'personal': ['clothing', 'toiletries', 'grooming'],
    'work': ['office supply', 'work phone', 'computer repair', 'software', 'hardware']
}

non_essentials = {
    'cravings': ['dining out', 'fast food', 'delivery', 'alcohol', 'restaurants', 'coffee'],
    'gifts': ['birthday', 'anniversary', 'holiday', 'other'],
    'giving': ['tithing', 'charitable', 'other'],
    'pets': ['food', 'supplies', 'vet', 'prescriptions', 'appointment'],
    'entertainment': ['streaming services', 'games', 'movies', 'hobbies', 'vacation', 'books'],
    'personal': ['salon', 'gym', 'dry cleaning']}
# 'online':['unknown']}
# 'domicile' : {'home': ['home insurance', 'mortgage', 'mortgage payment', 'home maitenance', 'home repair', 'property taxes', 'yard'],
#                'rental':['renters insurance', 'rent', 'rent payment', 'rental repair'],
#                 'furnishings':['furnishings', 'cleaning supply', 'kitchen ware','tools']},

# Stacked Bar graph
def make_stacked_bar_graph(data_df, cat_order, pos_amount):
    # month_categories is a df grouped
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
    fig.write_image(f'images/fig_stacked_bar.svg')
    fig.show()

# Sunburst
def make_sunburst(data_df):
    # Essentials variable pulled from above category types
    priority = []
    for i in data_df.category:
        if i in essentials.keys() or i in essentials.values():
            priority.append('Essential')
        elif i == 'online':
            priority.append('Unknown')
        else:
            priority.append('Non-Essential')
    data_df['priority'] = priority
    data_df['percentage'] = [(i/data_df.amount.sum()*100) for i in data_df.amount]
    essential_value = sum(
        data_df.loc[data_df['priority'] == 'Essential'].percentage)
    nonessential_value = sum(
        data_df.loc[data_df['priority'] == 'Non-Essential'].percentage)
    unknown = sum(data_df.loc[data_df['priority'] == 'Unknown'].percentage)
    non = sum(data_df.loc[data_df['priority'] == 'Non-Essential'].amount)
    # small_perc = (data_df.loc[data_df['priority'] ==
    #             'Non-Essential'].amount/non)*100
    sum_non = sum(data_df.loc[data_df['priority'] == 'Non-Essential'].amount)
    sum_ess = sum(data_df.loc[data_df['priority'] == 'Essential'].amount)
    sum_unk = sum(data_df.loc[data_df['priority'] == 'Unknown'].amount)
    percent_of_priority = []
    for index, row in data_df.iterrows():
        if row['priority'] == 'Essential':
            val = row['amount']/sum_ess*100
            #val = row['percentage']/essential_value*100
            percent_of_priority.append(val)
            # print(index)
            #print(f'e' + str(val))
        elif row['priority'] == 'Non-Essential':
            #val = row['percentage']/nonessential_value*100
            val = row['amount']/sum_non*100
            percent_of_priority.append(val)
            #print(f'n' + str(val))
        elif row['priority'] == 'Unknown':
            try:
                val = row['amount']/sum_unk*100
                #val = row['percentage']/unknown*100
                percent_of_priority.append(val)
                #print(f'u' + str(val))
            except:
                percent_of_priority.append(0)
        a = 0
        for i, r in data_df.iterrows():
            if r['priority'] == 'Essential':
                amount = r['amount']*-1
                a = a + amount
        chart = dict(
            child=['Essential', 'Non-Essential',
                'Unknown'] + list(data_df.category),
            parent=['Needs/Wants', 'Needs/Wants',
                    'Needs/Wants'] + list(data_df.priority),
            value=[essential_value, nonessential_value,
                unknown] + percent_of_priority
        )
    import plotly.io as pio


    fig = px.sunburst(
        chart,
        names='child',
        parents='parent',
        values='value',
        color='value',
        color_continuous_scale=gradient
    )

    #can save as an svg
    fig.write_image('images/sunburst.svg')
    fig.show()

# Part of Tables


# def get_length(df):
#     col = ''
#     for i in df.columns:
#         get_length = df[i].map(len).max()
#     return get_length

def convert_str(series):
    return [str(i) for i in series]

def get_max(dataframe):
    max_num = 0
    max_col = ''
    max_list = []
    for i in range(len(dataframe.columns)):
        if dataframe[dataframe.columns[i]][0] == type('s'):
            continue
        else:
            dataframe[dataframe.columns[i]] = convert_str(dataframe[dataframe.columns[i]])
        get_length = dataframe[dataframe.columns[i]].map(len).max()
        max_list.append(get_length)
        if max_num < get_length:
            max_num = get_length
            max_col = dataframe.columns[i]
            col_num = i
    return max_num, max_col, max_list

# Tables
def make_table(df, colors, rowOddColor, rowEvenColor, filename):
    fig = go.Figure(data=[go.Table(
        columnorder=[i+1 for i in range(len(df.columns))],
        columnwidth=[i*30 for i in get_max(df)[2]],
        header=dict(values=list(df.columns),
                    fill_color=colors[0],
                    align='left',
                    font=dict(family="Arial", size=14, color=colors[1])),
        cells=dict(values=[df[i] for i in df.columns],
                fill_color=[[rowOddColor, rowEvenColor,
                                rowOddColor, rowEvenColor]*4],  # colors[2],
                align='left',
                font=dict(family="Arial", size=12, color=colors[3])))])

    # , width=600, height=350, scale=2)
    #fig.write_image("../data_local/images/table.png", format="png")
    #pdf is higher quality however it omits all the lines below
    max_height = len(df) * 50
    pio.write_image(fig, '../data_local/images/table.pdf',
                    width=700, height=max_height)
    fig.write_image(f'images/table_{filename}.svg')
    fig.show()

# Treemap
def get_percentage(month_num, month_categories):
    percent = []
    mo_slice = month_categories[month_categories['month'] == month_num]
    sum_mo_1 = mo_slice['month_sum'].sum()
    for i in range(len(month_categories)):
        if month_categories['month'][i] == month_num:
            #print(round(month_categories['month_sum'][i], 2))
            #print(round(sum_mo_1)*100)
            amount = round(
                month_categories['month_sum'][i]/round(sum_mo_1)*100, 2)
            #print(amount)
            #break
            percent.append(amount)
    return percent

# def make_treemap(data_df, month_categories, month_sum):
#     if 'Date2' in data_df.columns:
#         data_df = data_df.drop('Date2', axis=1)
#     inside = ['savings', 'savings', 'debt', 'housing', 'transportation',
#             'food', 'utilities', 'medical', 'education', 'childcare', 'personal']
#     outside = ['essential' for i in range(len(inside))]
#     months = month_categories['month'].unique()
#     percentage = []
#     final = []
#     for month in months:
#         percentage.append(get_percentage(month))
#     final = [a for b in percentage for a in b]
#     month_categories['values'] = final

#Treemap
def search_values(cat, cat_dict, df):
    for value in essentials.values():
        if cat in value:
            return True

    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    fig = make_subplots(rows=6, cols=6,
                        column_widths=[0.4 for i in range(6)],
                        subplot_titles=(df.long_month.unique()))

#Treemap
def make_treemap(df, months):
    #months = month_categories['month'].unique()
    import plotly.express as px
    #print(df.head())
    df['month_sum_s'] = [f'${str(i)}' for i in df.month_sum]
    fig = px.treemap(df.sort_values(by=['values']).reset_index(drop=True),
                    title=f"{df['long_month'][0]} Spending",
                    path=['priority', 'category'],
                    values='values',
                    color='month_sum',
                    color_continuous_scale=gradient[::-1],
                    color_continuous_midpoint=np.average(
                        df['month_sum'], weights=df['values']),
                    hover_name='month_sum',
                    custom_data=['month_sum_s', 'percentages'])
    #fig.update_traces(marker_colors = colors_all, selector=dict(type='treemap'))
    #visual = df.loc[df['long_month'] == month]['month_sum_s']
    #fig.update_traces(hovertemplate='%{month_sum}')
    fig.data[0].hovertemplate = '%{label}'
    fig.update_traces(
        hovertemplate="<br>".join([
        "Dollars: %{customdata[0]}",
        "Percentage: %{customdata[1]}"
    ])
        )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.write_image(f'images/treemap{months}.svg')
    fig.show()

#Treemap
def loop_plots(months, df):
    for i, month in enumerate(months):
        i = i+1
        split_month_df = df.loc[df['month'] == month].reset_index(drop=True)
        priority = []
        for cat in split_month_df.category:
            if cat in essentials.keys() or search_values(cat, essentials, df):
                    priority.append('Essential')
            else:
                priority.append('Non-Essential')
        split_month_df['priority'] = priority
        split_month_df['values'] = split_month_df['values'].apply(
            lambda x: x*-1 if x < 0 else x)
        split_month_df['month_sum'] = split_month_df['month_sum'].apply(
            lambda x: round(x*-1) if x < 0 else round(x))
        split_month_df['percentages'] = split_month_df['values'].apply(lambda x: str(x*-1)+'%' if x < 0 else str(x)+'%')
        split_month_df['month_sum'] = split_month_df['month_sum'].apply(lambda x: round(x, 2))
        #print(split_month_df)
        make_treemap(split_month_df, month)
        
# Budget Graph
def budget_table(income):
    income = 100000
    #income = int(input('What is your Yearly income after taxes\n\n'))
    print('---------------------------------------')
    print('---------------------------------------')
    print(f'Total Yearly income:\t\t{income}')
    print('---------------------------------------')
    # savings = int(income * .10/12)
    print('Monthly Ideal amounts')
    print('---------------------------------------')
    print('---------------------------------------')
    print('Category\tPercent\t\tAmount')
    print('---------------------------------------')
    income_dict = {}
    print(f'Home\t\t(25%)\t\t{int(income * .25/12)}')
    income_dict['home'] = [30, int(income * .30/12)]

    print(f'Lifestyle\t(30%)\t\t{int(income * .30/12)}')
    income_dict['lifestyle'] = [15, int(income * .15/12)]

    print(f'Debt\t\t( 5%)\t\t{int(income * .05/12)}')
    income_dict['debt'] = [10, int(income * .10/12)]

    print(f'Savings\t\t(20%)\t\t{int(income * .20/12)}')
    income_dict['savings'] = [20, int(income * .10/12)]

    print(f'Food\t\t(10%)\t\t{int(income * .10/12)}')
    income_dict['food'] = [10, int(income * .15/12)]

    print(f'Transpo\t\t( 5%)\t\t{int(income * .05/12)}')
    income_dict['transportation'] = [10, int(income * .10/12)]

    print(f'Util\t\t( 5%)\t\t{int(income * .05/12)}')
    income_dict['utility'] = [5, int(income * .10/12)]
    return income, income_dict
