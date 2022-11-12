# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 17:35:46 2022

@author: robin.eberle
"""

import os
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import geopandas
import geopy
import string
import time

start_t = time.time()

# Get all files
offset = r"./02_Objekt-Detail/html_files_v02"
directory = os.getcwd() + offset
files = []


OUTPUT_FILE = './../data/real_estate_listing.csv'
SPAN_PATTERN = r"<span>(.*)<\/span>"
SVG_PATTERN = r"<svg .*>(.*)<\/svg>"
ADR_PATTERN = r"<span .*>.*<\/span>(.*)<\/h5>"

TAGS = {
    "Zimmer": "zimmer",
    "Baujahr": "baujahr",
    "Mietpreis pro Monat": "mietpreis",
    "Mietpreis pro Monat (exkl. NK)": "mietpreis",
    "Wohnfläche": "Flaeche"
}


def __extract(value):
     result = re.search(SPAN_PATTERN, str(value), re.IGNORECASE)
     if result:
         return result.group(1)
     
     result = re.search(ADR_PATTERN, str(value), re.IGNORECASE)
     if result:
         return result.group(1)   
     
     result = re.search(SVG_PATTERN, str(value), re.IGNORECASE)
     if result:
         return True
     
     return None
   
def __parse_value(label, value):
    if label is None:
        return None 
    
    if "zimmer" in label:
        pass
     
    elif "Flaeche" in label:
        return re.sub("\D","",value)
     
    elif "baujahr" in label:
        return re.sub("\D","",value)
     
    elif "mietpreis" in label:
        return re.sub("\D","",value)
     
    return value
     
   
def __isSupported(tag):
    if tag in TAGS:
        return TAGS[tag]
     
    return None

for filename in os.listdir(directory):
    if filename.endswith("txt"): 
        #print(os.path.join(directory, filename))
        files.append(filename)
        continue
    else:
        continue

def __address2Coord(address):
    lines = address.split(",")
    if len(lines) > 3:
        address = f"{lines[0]}, {lines[-1]}"
    
    locator = geopy.geocoders.Nominatim(user_agent= "myGeocoder")
    location = locator.geocode(address)
    
    if location is None:
        return None, None
   
    return location.latitude, location.longitude

# Output_000-28672701.txt
attributes = []
for file in files:
    print(f"check {file}")
    with open(os.path.join(offset, file), "rb") as f:
        src = f.read().decode("UTF-16LE")

        soup = BeautifulSoup(src, 'html.parser')
        
        labels = soup.find_all('p', class_='css-cyiock')
        values = soup.find_all('p', class_='css-1ush3w6')
        adress = soup.find_all('h5', class_='css-15z12tn')
        
        result = {}        
        for label, value in zip(labels, values):           
            label = __isSupported(__extract(label))
            value = __parse_value(label, __extract(value))

            if label is not None:
                result[label] = value
                
        # address
        lat, lon = __address2Coord(__extract(adress))
        if lat is not None and lon is not None:
            result["Latitude"] = lat
            result["Longitude"] = lon
        
            attributes.append(result)
        
frame = pd.DataFrame(attributes)    
frame.to_csv(OUTPUT_FILE)

print(time.time()-start_t)
