import re
dictionary = {
    '0_format': ['date', 'location data', 'float amount', 'identifier', 'category'],
    'home': [
        ['01/24/21', 'HOME_DEPOT',  -57, 'HOME','home'],
        ['01/12/21', 'LOWES', -100, 'LOWES', 'home'],
        ['02/14/21', 'TRUE_VALUE', -60, 'TRUE', 'home']],

    'fast_food': [
        ['01/28/21', 'CHICK-FIL-A', -14.99, 'CHICK-FIL-A','fast_food'],
        ['03/15/21', 'BOJANGLES 5555 ELIZABETH CITY NY', -12.99, 'BOJANGLES', 'fast_food']
        ],

    'food': [
        ['01/22/21', 'FOOD LION',  -200, 'FOOD LION', 'food'],
        ['02/21/21', 'HARRIS_TEETER', -250, 'HARRIS', 'food'],
        ['03/15/21', 'FARM_FRESH', -150, 'FRESH', 'food']],
    'gas':[
        ['03/22/21', 'SHELL OIL 2423423423423 LUCY, PA', -28, 'SHELL', 'gas']
    ],
    'utilities':[
        ['03/18/21', 'DENVER SANITATION 489-4698-06456 CO', -80, 'SANITATION', 'gas']
        ]
}

#date_formats_year4 = '(\d+/\d+/\d{4}$)'
#date_formats_year2 = '(\d+/\d+/\d{2}$)'

#gets all rows as a list
rows_list = [entry for key, value in dict.items() for entry in value if key!= '0_format']

#setting up filter for dd/mm/yyyy or mm/dd/yyyy
r = re.compile('(\d+/\d+/\d{4}$)')
get_list = 0
for i in rows_list:
        get_list +=list(filter(r.search, [str(j) for j in i]))

# Returns this :::
# print(get_list)
#['05/19/2021', '06/19/2021']

rows_list2 = [list(filter(r.search, [str(j) for j in entry])) for key, value in dict.items() for entry in value if key!= '0_format']
# Returns this :::
#print(rows_list2)
#[[], [], ['05/19/2021'], [], ['06/19/2021'], [], [], [], [], [], [], [], [], []]