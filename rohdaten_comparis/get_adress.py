# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 19:54:30 2022

@author: robin.eberle
"""
import geopandas
import geopy
import re

value = "170 m²"

print(re.sub("\D","",value))