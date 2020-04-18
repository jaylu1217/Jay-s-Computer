#!/usr/bin/env python
# coding: utf-8

# In[15]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files
get_ipython().system('pip install geopy')
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors
import random

# import k-means from clustering stage
from sklearn.cluster import KMeans

get_ipython().system('pip install folium')
import folium # map rendering library
from IPython.display import Image 
from IPython.core.display import HTML 
get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library

print('Libraries imported.')


# In[16]:


address = 'Hsinchu, TW'
CLIENT_ID = 'CN3M4BZ34T3OHU1UKYLZ4DGZ0L404FAKRAWBHM1U15SIKS00'
CLIENT_SECRET = 'QBH5WMC41BH3X43LAMCXSGU1XYNXHVHNTVID5ODYFJAOWD2V'
VERSION = '20180604'
LIMIT = 30
print('Jay Lu')
print('CLIENT_ID: ', CLIENT_ID)
print('CLIENT_SECRET: ', CLIENT_SECRET)


# In[17]:


geolocator = Nominatim(user_agent='foursquare_agent')
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# In[18]:


search_query = 'cafe'
radius = 500
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[19]:


results = requests.get(url).json()
results


# In[20]:


venues = results['response']['venues']
dataframe = json_normalize(venues)
dataframe.head()


# In[21]:


filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]
dataframe_filtered


# In[22]:


dataframe_filtered.name


# In[38]:




venues_map = folium.Map(location=[latitude, longitude], zoom_start=13) 



venues_map


# In[43]:


venue_id = '51c829e4498e6bf2c7c32fac' 
url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(venue_id, CLIENT_ID, CLIENT_SECRET, VERSION)
url


# In[40]:


result = requests.get(url).json()
print(result['response']['venue'].keys())
result['response']['venue']


# In[44]:


try:
    print(result['response']['venue']['rating'])
except:
    print('This venue has not been rated yet.')


# In[45]:


result['response']['venue']['tips']['count']


# In[46]:



url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&ll={},{}&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, radius, LIMIT)
url


# In[50]:


results = requests.get(url).json()
results
items = results['response']['groups'][0]['items']
items[0]


# In[51]:


dataframe = json_normalize(items) # flatten JSON

# filter columns
filtered_columns = ['venue.name', 'venue.categories'] + [col for col in dataframe.columns if col.startswith('venue.location.')] + ['venue.id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# filter the category for each row
dataframe_filtered['venue.categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean columns
dataframe_filtered.columns = [col.split('.')[-1] for col in dataframe_filtered.columns]

dataframe_filtered.head(10)


# In[52]:


venues_map = folium.Map(location=[latitude, longitude], zoom_start=15) # generate map centred around Ecco


# add Ecco as a red circle mark
folium.features.CircleMarker(
    [latitude, longitude],
    radius=10,
    popup='Ecco',
    fill=True,
    color='red',
    fill_color='red',
    fill_opacity=0.6
    ).add_to(venues_map)


# add popular spots to the map as blue circle markers
for lat, lng, label in zip(dataframe_filtered.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        fill=True,
        color='blue',
        fill_color='blue',
        fill_opacity=0.6
        ).add_to(venues_map)

# display map
venues_map


# In[ ]:




