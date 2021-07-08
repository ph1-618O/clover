import requests

response = requests.get('https://httpbin.org/ip')

print('Your IP is {0}'.format(response.json()['origin']))


# pip install pandas
# pip install numpy
# pip install fastnumbers
# pip install geopy

# pip install squarify
# pip install beautifulsoup4
# pip install googlesearch-python
# pip install texthero
