#!/usr/bin/env python3
# coding: utf-8

# You can have up to 2,500 free directions requests per day
# and the cost for additional requests is $0.50 USD per 1000 additional requests, up to 100,000 daily.
# Location.py takes a string like "FOOD LION #1234 VIRGINIA BEACVA" or "AUTOZONE 1826 ARLINGTON VA" and verifies if there is a city and state located within it
from re import A
from numpy.core.fromnumeric import _transpose_dispatcher
from pandas.core.frame import DataFrame
#import geopy
import requests
import json
from config import gKey
import math
import pprint
pp = pprint.PrettyPrinter(indent=4)


def find_location(target_query=None):
    if target_query:
        #target_query = "VIRGINIA BEACVA"
        params = {"address": target_query, "key": gKey}
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        #print(f'Testing {target_query}')
        response = requests.get(base_url, params=params)
        location = response.json()
        if response.status_code == 200:
            #print('Success!')
            l_type = location["results"][0]["geometry"]['location_type']
            # Saving this to add a map location for future applications
            lat = location["results"][0]["geometry"]["location"]["lat"]
            lng = location["results"][0]["geometry"]["location"]["lng"]
            #print(f'{target_query}: {lat}, {lng}')
            if l_type.lower() == 'approximate':
                #print('returning true')
                return True
            else:
                #print('returning false')
                return False
        elif response.status_code == 404:
            #print('Not Found.')
            return False
        else:
            return 'ERROR'
        

def find_lat_lng(target_query=None):
    if target_query:
        #target_query = "VIRGINIA BEACVA"
        params = {"address": target_query, "key": gKey}
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        #print(f'Testing {target_query}')
        response = requests.get(base_url, params=params)
        location = response.json()
        if response.status_code == 200:
            #print('Success!')
            #pp.pprint(location)
            l_type = location["results"][0]["geometry"]['location_type']
            # Saving this to add a map location for future applications
            lat = location["results"][0]["geometry"]["location"]["lat"]
            lng = location["results"][0]["geometry"]["location"]["lng"]
            #print(f'{target_query}: {lat}, {lng}')
            if l_type.lower() == 'approximate':
                #print('returning true')
                return lat, lng
            else:
                #print('returning false')
                return False
        elif response.status_code == 404:
            #print('Not Found.')
            return False
        else:
            return 'ERROR'

# This function takes a single set of coordinates creates a 355 mile square around it and spirals smaller using the fibbonachi sequence,
# At each coordinate that is produced the city and state is returned 
# 355 miles was used as it is the average square size of an American city, obviously that number is skewed quite a bit because of states like Alaska, 
# and some midwest states where cities are hundreads of miles wide
#
def cities_square(lat, long, miles):
    import math
    # First need to get a radius of 50 miles around the longitude and latitude to set the points for the fib spiral
    # r = radius
    r = miles
    d_lat = r/69
    d_long = d_lat/math.cos(lat)
    #b_left = f'{lat - d_lat}, {long - d_long}'
    north = lat + d_lat
    south = lat - d_lat
    east = long + d_long
    west = long - d_long
    
    bottom_left = ((lat - d_lat), (long - d_long))
    top_left = ((lat + d_lat), (long - d_long))
    top_right = ((lat + d_lat), (long + d_long))
    bottom_right = ((lat - d_lat), (long + d_long))
    #print(top_left, top_right, bottom_right, bottom_left)
    return top_left, top_right, bottom_right, bottom_left   


def fib(n):
    a, b = 0, 0.125
    for _ in range(n):
        yield a
        a, b = b, a + b
        
def reverse_Fibonacci(n):
    a = [0] * n
    a[0] = 0
    a[1] = 1
    for i in range(2, n):
        a[i] = a[i-2] + a[i-1]
    for i in range(n-1, -1, -1):
        print(a[i], end=" ")
    

    
    
def reverse_city(lat, long):
    # sending lat and long to google api to find the city state
    import re
    import geopy
    from geopy.geocoders import GoogleV3
    geolocator = GoogleV3(gKey)
    address = geolocator.reverse(f'{str(lat)}, {str(long)}')
    # Sometimes google api has a full address and sometimes just the city/county, state and zip
    regex_city_st1 = "(?<=,)[^,]+(?=,), [A-Z]{2}" # gets words between commas
    regex_city_st2 = '[^,]+(?=,){2},'
    # if >= 3 commas its probably a full address
    # else its just the city/county, state
    if address:
        if address[0].count(',') >= 3:
            city_st = ''.join(re.findall(regex_city_st1, address[0])).strip()
            #print(city_st)
            return city_st
        elif address[0].lower() == 'united states':
            pass
            #print('In the ocean')
        else:
            #-1 removes the following comma
            city_st = ''.join(re.findall(regex_city_st2, address[0])).strip()[:-1]
            #print(city_st)
            return city_st


def scatter_locales(lat, lng, center):
    expand_100 = cities_square(lat, lng, 25)
    



def spiral_locales(lat, lng, center):
    # Using 25 because that makes a radius of 50ish miles
    decrement_list = list(fib(25))
    phi = 1.618033988749895
    decrement_list = [i/phi if i != 0 else 0 for i in decrement_list]
    # removing second value of 1 because redundancy
    del decrement_list[1]
    print(decrement_list)
    surrounding_locals = []
    for i in decrement_list:
        if i > 25:
            break
        else:
            expand_100 = cities_square(lat, lng, 25-i)
            #cycles 4 times to get shrinking cities
            for coords in expand_100:
                place = reverse_city(coords[0], coords[1])
                if place not in surrounding_locals:
                    surrounding_locals.append(place)
                if place == center:
                    surrounding_locals.append(place)
                    break 
    print(surrounding_locals)
    
def make_location_stop_words():
    center = 'Norfolk, VA'
    found = find_lat_lng(center)
    lat = found[0]
    lng = found[1]
    spiral_locales(lat, lng, center)


def main():
    find_location()
    
    
if __name__ == "__main__":
    main()



