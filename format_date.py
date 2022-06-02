#!/usr/bin/env python3
# coding: utf-8

#https: // ielts.com.au/australia/prepare/article-how-to-write-the-date-correctly

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


# regex for "Oct 21, 2014" or "October 21, 2014"
# need more sophisticated validations such as validating the number of days for a specific month
#(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})\s+(\d{4})
# February 2009
#\b(?:Jan(?:uary)?|Feb(?:ruary)?|...|Dec(?:ember)?) (?:19[7-9]\d|2\d{3})(?=\D|$)
# or
#(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})
#yyyy-mm-dd

#(\d+(?:/|\\|-)\d+(?:/|\\|-)\d{4}$)
