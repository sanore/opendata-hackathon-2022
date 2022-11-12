# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 14:36:11 2022

@author: robin.eberle
"""

import os
import time
from pathlib import Path
from xml.etree import cElementTree as ET


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

"""
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

"""
with open("TestFile_000.txt", "rb") as f:
    xmlstr = f.read().decode("UTF-16LE").split("\n")


root = ET.fromstring(xmlstr)
"""
for page in list(root):
    title = page.find('href').text
    content = page.find('content').text
    print('href: %s; content: %s' % (title, content))

print(time.time()-start_time)

"""
