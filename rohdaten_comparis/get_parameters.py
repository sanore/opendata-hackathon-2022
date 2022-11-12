# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 17:35:46 2022

@author: robin.eberle
"""

import os
import requests
import re
from bs4 import BeautifulSoup

# Get all files
offset = r"./02_Objekt-Detail/html_files_v01"
directory = os.getcwd() + offset
files = []


SPAN_PATTERN = r"<span>(.*)<\/span>"
SVG_PATTERN = r"<svg .*>(.*)<\/svg>"

def __extract(value):
     result = re.search(SPAN_PATTERN, str(value), re.IGNORECASE)
     if result:
         return result.group(1)
     
     result = re.search(SVG_PATTERN, str(value), re.IGNORECASE)
     if result:
         return True
     
     return None
    

for filename in os.listdir(directory):
    if filename.endswith("txt"): 
        #print(os.path.join(directory, filename))
        files.append(filename)
        continue
    else:
        continue

# Output_000-28672701.txt
attributes = []
for file in files:
    print(f"check {file}")
    with open(os.path.join(offset, file), "rb") as f:
        src = f.read().decode("UTF-16LE")

        soup = BeautifulSoup(src, 'html.parser')
        
        labels = soup.find_all('p', class_='css-cyiock')
        values = soup.find_all('p', class_='css-1ush3w6')
        
        result = {}        
        for label, value in zip(labels, values):           
            label = __extract(label)
            value = __extract(value)
            
            result[label] = value
        
        
        attributes.append(result)
        
        
    #print(tag)
