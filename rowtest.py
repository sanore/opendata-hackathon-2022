# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 17:23:05 2022

@author: waleed madi
"""

import numpy as np
import shapely.geometry as sh
import pandas as pd

def emission(longitude, latitude, radius):

    data_path = "./data/larmemission_SG.csv"
    #gets the street coordinates and connects them to lines
    points = pd.read_csv(data_path, sep=';',encoding='utf-8', usecols=[1, 5, 6], index_col=False)
    streets = []
    for index, row in points.iterrows():
        street_points = []
        row["Geo Shape"] = row["Geo Shape"].lstrip('"{""coordinates"": [[')
        row["Geo Shape"] = row["Geo Shape"].rstrip('"type":, "LineString"}')
        row["Geo Shape"] = str(row["Geo Shape"]).lstrip('[')
        row["Geo Shape"] = str(row["Geo Shape"]).rstrip(']]')
        row["Geo Shape"] = row["Geo Shape"].split('], [')
        for point in row["Geo Shape"]:
            point = point.strip(' ')
            point = point.strip(']')
            point = point.strip('[')
            point = point.split(', ')
            point = (float(point[0]), float(point[1]))
            street_points.append(point)
        street = sh.LineString(street_points)
        streets.append((street, row["Emissionswert (Lre) Tag [dB(A)]"], row["Emissionswert (Lre) Nacht [dB(A)]"]))

    #gets all street in a distance < radius
    point_wohnung = sh.Point(longitude, latitude)
    dbs = {}
    db_log = 0
    for street, db_tag, db_nacht in streets:
        #print(f"street-> {point_wohnung.distance(street)}")
        if(point_wohnung.distance(street) < radius):
            #gets the laeremmission for all streets in range
            dbs[point_wohnung.distance(street)] = [db_tag, db_nacht]
            db_log = db_log + 10**(np.mean([db_tag, db_nacht])/np.log10(point_wohnung.distance(street)))
            #dbs.append(db_tag)
            #dbs.append(db_nacht)
            #print(f"db_tag-> {db_tag}")
        else:
            continue
    #print(f"dbs-> {dbs}")
    #gets the score
    db_log = np.log10(db_log)

    obergrenze = max(points["Emissionswert (Lre) Tag [dB(A)]"])
    untergrenze = min(points["Emissionswert (Lre) Nacht [dB(A)]"])

    bewertung = -(10/(obergrenze - untergrenze)) * db_log + 10
    if bewertung < 1:
        bewertung = 1

    return bewertung

if __name__ =='__main__':

    res = emission(47.4243138, 9.3719775, 10000)
    print(f"der score beträgt: {res}")
