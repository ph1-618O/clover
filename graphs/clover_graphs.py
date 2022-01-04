#!/usr/bin/env python3
# coding: utf-8

import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
pio.renderers.default = 'jpg'
import os

#Orca must be installed?
#conda install -c plotly plotly-orca
#Kaleido is for exporting images from plotly
#pip install -U kaleido

if not os.path.exists('images'):
    os.mkdir('images')

def make_table(df):
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.date, df.transaction, df.amount, df.identifier, df.category], fill_color='lavender', align='left'))
    ])
    fig.write_image('images/table.jpg')
    #fig show prints out the jpg
    #fig.show()

data = pd.read_csv('../data/sample_data_categories.csv')
col_names = []
for col in data.columns:
    col_names.append(col)
col_data = []
for i in col_names:
    col_data.append(data[i])

make_table(data)
#make_table(col_names, col_data)
