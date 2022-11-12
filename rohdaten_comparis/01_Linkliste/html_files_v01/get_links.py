# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 14:36:11 2022

@author: robin.eberle
"""

import os
import sys
from pathlib import Path
import time

start_time = time.time()
# Get all files
directory = os.getcwd()
files = []

for filename in os.listdir(directory):
    if filename.endswith("txt"): 
        #print(os.path.join(directory, filename))
        files.append(filename)
        continue
    else:
        continue


# Extraxt Links
for file in files:
    with open(file) as f:
        lines = f.readlines()
    
    link_lines = []
    links = []
    
    for line in lines:
        if ("details/show" in line):
            link_lines.append(line)
    
    for string in link_lines:
        link_string = string.split('"')
        for link in string.split('"'):
            if ("details/show" in link):
                print("https://www.comparis.ch" + link)
                links.append(link)

print(time.time()-start_time)
