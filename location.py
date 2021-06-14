#!/usr/bin/env python3
# coding: utf-8

# You can have up to 2,500 free directions requests per day
# and the cost for additional requests is $0.50 USD per 1000 additional requests, up to 100,000 daily.
# Location.py takes a string like "FOOD LION #1234 VIRGINIA BEACVA" or "AUTOZONE 1826 ARLINGTON VA" and verifies if there is a city and state located within it
import requests
import json
from config import gKey


def find_location(target_query=None):
    if target_query:
        #target_query = "VIRGINIA BEACVA"
        params = {"address": target_query, "key": gKey}
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        print(f'Testing {target_query}')
        response = requests.get(base_url, params=params)
        location = response.json()
        if response.status_code == 200:
            print('Success!')
            l_type = location["results"][0]["geometry"]['location_type']
            if l_type.lower() == 'approximate':
                print('returning true')
                return True
            else:
                print('returning false')
                return False
        elif response.status_code == 404:
            print('Not Found.')
            return False
        else:
            return 'ERROR'
        
    # Saving this to add a map location for future applications
    # lat = location["results"][0]["geometry"]["location"]["lat"]
    # lng = location["results"][0]["geometry"]["location"]["lng"]
    # print(f'{target_query}: {lat}, {lng}')


def main():
    find_location()


if __name__ == "__main__":
    main()
