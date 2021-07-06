from itertools import chain
import pprint
import budget
pp = pprint.PrettyPrinter(indent=4)


dict1 = {
    '0_format': ['date', 'time', 'list3', 'list4'], 
    '1_seed': {
        'thing': [['lots of words']], 
        'thing2': [['more words']]
        },
    'apple': [['banana']]}
dict2 = {
    '0_format': ['date', 'time', 'list3'], 
    '1_seed': {
    'different_thing': ['words'], 
    'thing3': ['magic']},
    'opal': [['green']],
    'apple': [['banana'], ['grape']]
    }

dict3 = {
    '0_format': ['date', 'time', 'list3', 'category'],
    '1_seed': {
        'thing': [['lots of words']],
        'thing2': [['more words']]
    },
    'apple': [['1', '2', '3', 'banana']],
    'opal': [['1', '2', '3', 'agent']]}

dict4 = {
    '0_format': ['date', 'time', 'list3', 'list4', 'list5'],
    '1_seed': {
        'different_thing': ['words'],
        'thing3': ['magic']},
    'opal': [['1', '2', '3', 'green', 'thing']],
    'apple': [['1', '2', '3', 'banana', 'thing'], ['1', '2', '3',  'grape', 'thing']]
}

# def merge_dict(dict1, dict2):
#     # pulling out format and seed info so it doesnt duplicate
    
#     # Format row first
#     if dict2['0_format'] == dict1['0_format']:
#         format = dict1['0_format']
#         dict1.pop('0_format', None)
#     else:
#         #be very careful here, this can screw up the order of columns
#         for new_col in dict2['0_format']:
#             for col_i in range(len(new_col)):
#                 if new_col not in dict1['0_format']:
#                     dict1['0_format'].insert(col_i, new_col)
#         format = dict1['0_format']
#         dict1.pop('0_format', None)
        
#     print(format)    
#     # Seed row next   
#     seed1 = dict1['1_seed']
#     dict1.pop('1_seed', None)
#     seed2 = dict2['1_seed']
#     dict2.pop('1_seed', None)
    
#     m = {}
#     for k, v in chain(dict1.items(), dict2.items()):
#             m.setdefault(k, []).extend(v)
    
    
#     return m


# pp.pprint(merge_dict(dict1, dict2))



df1 = budget.dict_to_Frame(dict3)
df2 = budget.dict_to_Frame(dict4)
print(df1)
print(df2)
print('\n\n\n')
df3 = df1.append(df2, sort = False).drop_duplicates().reset_index(drop=True)
print(df3)
# for index, row in df3.iterrows():
#     if row

a = df3.groupby(by=['date', 'time', 'list3'])
a.apply(print)

for index, row in df3.iterrows():
    if row['date'][index] and row['time'][index] and row['list3']
    