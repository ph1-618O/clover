#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
from datetime import datetime as d
from tabulate import tabulate as chart


date_df = pd.read_csv('data/date_formats.csv')


date_dict = {
    'short': [['%a'],['Mon, Tues, Wed, Thurs, Fri, Sat, Sun']],
    'd_full': [['%A'],['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']],
    'd_num': [['%w'],[i for i in range(1, 8)]],
    'd_num_yr':[['%j'],[i for i in range(1, 365)]],
    'd_mo': [['%d'],[i for i in range(1, 32)]],
    'w_num': [['%W'],[i for i in range(1, 53)]],
    'mo_s': [['%b'],['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']],
    'mo_l': [['%B'],['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']],
    'mo_num': [['%m'],[i for i in range(1, 13)]],
    'yr_l': [['%Y'],[i for i in range(1969, str(d(d.today().year, d.today().month, 1))[:4])]],
    'yr_s': [['%y'],[i for i in range(69, str(d(d.today().year, d.today().month, 1))[2:4])]],
    'hr_24': [['%H'],['0'+ str(i) if len(str(i)) < 2 else i for i in range(0,24)]],
    'hr_12': [['%h'],['0'+ str(i) if len(str(i)) < 2 else i for i in range(0,13)]],
    'suffix': [['%p'],['AM', 'PM']],
    'min': [['%M'],['0'+ str(i) if len(str(i)) < 2 else i for i in range(0,60)]],
    'sec': [['%S'],['0'+ str(i) if len(str(i)) < 2 else i for i in range(0,60)]],
}
def input_date_format(date):
    print('PLEASE CHOOSE THE NUMBER THAT CORRESPONDS TO THE DATE FORMAT\n')
    print()