# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 19:30:26 2022

"""

import os

directory = os.getcwd()
files = []

base_url = 'https://www.comparis.ch/immobilien/marktplatz/details/show/'

for filename in os.listdir(directory):
    if filename.endswith("txt"): 
        #print(os.path.join(directory, filename))
        files.append(filename)


# Extraxt Links
for file in files:
    with open(file, "rb") as f:
        lines = f.read().decode("UTF-16LE").split("\n")
        
    for line in lines:
            pos = 0
            while(line.find('{"AdId":', pos) > 0):
                pos = line.find('{"AdId":', pos)
                with open('links.txt', 'a') as f:
                    f.write(base_url + line[pos+8:pos+16] + '\n')
                pos += 1
