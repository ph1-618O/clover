from itertools import chain
import pprint
pp = pprint.PrettyPrinter(indent=4)


dict1 = {
    '0_format': ['list1', 'list2', 'list3', 'list4'], 
    '1_seed': {
        'thing': [['lots of words']], 
        'thing2': [['more words']]
        },
    'apple': [['banana']]}
dict2 = {
    '0_format': ['list1', 'list5', 'list3'], 
    '1_seed': {
    'different_thing': ['words'], 
    'thing3': ['magic']},
    'opal': [['green']],
    'apple': [['banana'], ['grape']]
    }

def merge_dict(dict1, dict2):
    # pulling out format and seed info so it doesnt duplicate
    
    # Format row first
    if dict2['0_format'] == dict1['0_format']:
        format = dict1['0_format']
        dict1.pop('0_format', None)
    else:
        #be very careful here, this can screw up the order of columns
        for new_col in dict2['0_format']:
            for col_i in range(len(new_col)):
                if new_col not in dict1['0_format']:
                    dict1['0_format'].insert(col_i, new_col)
        format = dict1['0_format']
        dict1.pop('0_format', None)
        
    print(format)    
    # Seed row next   
    seed1 = dict1['1_seed']
    dict1.pop('1_seed', None)
    seed2 = dict2['1_seed']
    dict2.pop('1_seed', None)
    
    m = {}
    for k, v in chain(dict1.items(), dict2.items()):
            m.setdefault(k, []).extend(v)
    
    
    return m


pp.pprint(merge_dict(dict1, dict2))
