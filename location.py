#!/usr/bin/env python3
# coding: utf-8

# You can have up to 2,500 free directions requests per day
# and the cost for additional requests is $0.50 USD per 1000 additional requests, up to 100,000 daily.
# Location.py takes a string like "FOOD LION #1234 VIRGINIA BEACVA" or "AUTOZONE 1826 ARLINGTON VA" and verifies if there is a city and state located within it
import requests
import json
from config import gKey
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
            print(f'{target_query}: {lat}, {lng}')
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
            pp.pprint(location)
            l_type = location["results"][0]["geometry"]['location_type']
            # Saving this to add a map location for future applications
            lat = location["results"][0]["geometry"]["location"]["lat"]
            lng = location["results"][0]["geometry"]["location"]["lng"]
            print(f'{target_query}: {lat}, {lng}')
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


def main():
    #find_location()
    found = find_lat_lng('Norfolk')
    lat = found[0]
    lng = found[1]
    find_closest_cities(lat, lng)


if __name__ == "__main__":
    main()
