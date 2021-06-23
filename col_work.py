

# import numpy as np
# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# import json
# with open('data/train_dict.json') as j:
#     dict = json.load(j)

# import pandas as pd
# test_df = pd.read_csv('data/train_cols.csv')

#working with dataframe and dictionary
def rec_col_type(df, dict):
    new_cols = list(df.columns)
    old_cols = dict['0_format']
    # print(f' New {new_cols}')
    # print(f' Old {old_cols}')
    #finding the difference between the col lists
    test_new = set(new_cols)
    test_old = set(old_cols)
    diff_new = test_new.difference(test_old)
    diff_old = test_old.difference(test_new)
    #print(diff_old)
    # diff = list(diff_new) + list(diff_old)
    # print(diff)
    dict_cols = []
    dict_cols_i =[]
    if not diff_new and not diff_old:
        print('Column list is the same')
        return(df, dict)
    if diff_old:
        for i in diff_old:
            dict_cols_index = dict['0_format'].index(i)
            dict_cols_i.append(dict['0_format'].index(i))
            dict['0_format'].remove(i)
            # grabbing the column not in the new dataframe from dict, putting it into a list to add later and removing it
            for key, value in dict.items():
                if key != '0_format':
                    for data_list in value:
                        dict_cols.append(data_list[dict_cols_index])
                        data_list.remove(data_list[dict_cols_index])
    #pp.pprint(dict)
    #finding the index location or column number where the diff is
    if diff_new:
        #print(len(new_cols))
        #print(len(old_cols))
        reordered_df = df.drop(columns=list(diff_new))
        for i in diff_new:
            if i in new_cols:
                #print('Location in DF new cols')
                #print(i)
                index = new_cols.index(i)
                #print(f'index of {i} {index} in new_cols')
                if 'identifier' in new_cols and 'category' in new_cols:
                    id = new_cols.index('identifier')
                    cat = new_cols.index('category')
                    #print(f' id {id}, cat {cat}')
                    if int(id) < int(cat):
                        #inserting into df
                        insert_loc = id
                        reordered_df.insert(loc=insert_loc, column=i, value=df[i])
                        #inserting into dict
                        for key, value in dict.items():
                            if key == '0_format':
                                value.insert(insert_loc, i)
                            else:
                                for data_list in value:
                                    data_list.insert(insert_loc, np.nan)   
    # print('Between diff_new and diff_old')
    # pp.pprint(dict)
    # print(reordered_df)
    # print('After between')
    # print(old_cols)
    #print(dict_cols)
    #print(dict_cols_i)
    if diff_new and diff_old:
        #print('True')
        for i in diff_old:
            #print('Location in DF new cols')
            #print(i)
            for index in dict_cols_i:
                #print(f'index of {i} {index} in old_cols')
                if 'identifier' in old_cols and 'category' in old_cols:
                    id = old_cols.index('identifier')
                    cat = old_cols.index('category')
                    #print(f' id {id}, cat {cat}')
                    if int(id) < int(cat):
                        #inserting into df
                        insert_loc = id
                        reordered_df.insert(
                            loc=insert_loc, column=i, value=dict_cols)
                        #inserting into dict
                        counter = 0
                        for key, value in dict.items():
                            if key == '0_format':
                                value.insert(insert_loc, i)
                            #skipping empties
                            elif key != '0_format' and dict[key]:    
                                for data_list in value:
                                    data_list.insert(insert_loc, dict_cols[counter])
                                    counter += 1
    return reordered_df, dict       
    # print(reordered_df)
    # pp.pprint(dict)
        
# rec_col_type(test_df, dict)
                

