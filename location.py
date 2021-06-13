#!/usr/bin/env python3
# coding: utf-8

# Location.py takes a string like "FOOD LION #1234 VIRGINIA BEACVA" or "AUTOZONE 1826 ARLINGTON VA" and verifies if there is a city and state located within it
import requests
import json
from config import gKey

def find_location():
    target_query = "VIRGINIA BEACVA"
    params = {"address": target_query, "key": gKey}
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    print(f'Testing {target_query}')
    response = requests.get(base_url, params=params)
    location = response.json()
    lat = location["results"][0]["geometry"]["location"]["lat"]
    lng = location["results"][0]["geometry"]["location"]["lng"]
    print(f'{target_query}: {lat}, {lng}')

def main():
    find_location()

if __name__ == "__main__":
    main()
