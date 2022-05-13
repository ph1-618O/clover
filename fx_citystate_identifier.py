#!/usr/bin/env python3
# coding: utf-8


fix_list = ['24 RICHMOND BREWERY', 'BLUE RIDGE SANITATI 4s4', 'BLUE RIDGE INN', 'ATLANTA COMMISSARY', 'ATLANTA MM GAS', 'ATHENS 44 APPLE STORE']

location_list = ['BLUE RIDGE', 'ATHENS', 'ATLANTA', 'GA', 'RICHMOND']

def check_alpha(word):
    if word.isalpha():
        return word

for location in location_list:
    for fix in fix_list:
        if location in fix and len(location) > 2:
            check_word = fix.split()
            #print(check_word)
            loc=[]
            for word in range(len(check_word)):
                if check_word[word].isalpha():
                    loc.append(check_word[word])
            words = ' '.join(loc)
            print(words)
            #print(location) 
    
