#!/usr/bin/env python3
# coding: utf-8

import os
import plotly.graph_objects as go
import pandas as pd
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
rainbow_colors = ['#F94144', '#f3722c', '#F9844A', '#f8961e',
                '#F9C74F', '#90BE6D', '#43AA8B', '#4D908E', '#277DA1', '#577590']
ainbow_colors = ['#F94144', '#f3722c', '#F9844A', '#f8961e',
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
    # fig.show()


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
    data_df['percentage'] = [(i/data_df.amount.sum()*100)
                            for i in data_df.amount]
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
    #fig.show()
