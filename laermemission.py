# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 17:23:05 2022

@author: waleed madi
"""

import numpy as np
import shapely.geometry as sh
import pandas as pd
from shapely.ops import transform
from functools import partial
import pyproj

def emission(longitude, latitude, radius=100.0):
    plz_sg = [9000, 9001, 9004, 9006, 9007, 9008, 9009, 9010, 9011, 9012, 9013, 9014, 9015, 9016, 9020, 9022]
    data_path = "./data/larmemission_SG.csv"
    #gets the street coordinates and connects them to lines
    points = pd.read_csv(data_path, sep=';',encoding='utf-8', usecols=[1, 3, 5, 6], index_col=False)
    streets = []
    for index, row in points.iterrows():
        street_points = []
        if((row["PLZ"] in plz_sg) and row["Emissionswert (Lre) Tag [dB(A)]"] != 0 and row["Emissionswert (Lre) Nacht [dB(A)]"] != 0):
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
        #print(streets)
# Geometry transform function based on pyproj.transform
    project = partial(
        pyproj.transform,
        pyproj.Proj('EPSG:4326'),
        pyproj.Proj('EPSG:32633'))

#gets all street in a distance < radius
    point_wohnung = sh.Point(longitude, latitude)
    point_wohnung = transform(project, point_wohnung)
    #dbs = {}
    db_dist = []
    for street, db_tag, db_nacht in streets:
        street = transform(project, street)
        #print(f"street-> {point_wohnung.distance(street)}")
        meter_distance = point_wohnung.distance(street)
        if(meter_distance < radius and meter_distance > 0):
            #gets the laeremmission for all streets in range
            #print(meter_distance)
            #dbs[meter_distance] = [db_tag, db_nacht]
            print(meter_distance, "and", db_tag)
            db_dist.append(np.max(np.mean([db_tag, db_nacht]) + 20*np.log10(1.2/meter_distance), 0))
            #dbs.append(db_tag)
            #dbs.append(db_nacht)
            #print(f"db_tag-> {db_tag}")
        else:
            continue
    #print(f"dbs-> {dbs}")
    #gets the score
    db_dist = np.array(db_dist)
    print(db_dist)
    if not db_dist.size:
        db_tot = 0
    else:
        db_tot = 10*np.log10((10**(db_dist/10)).sum())
    print(db_tot)

    obergrenze = max(points["Emissionswert (Lre) Tag [dB(A)]"])
    untergrenze = min(points["Emissionswert (Lre) Tag [dB(A)]"])

    bewertung = -(10/(obergrenze - untergrenze)) * db_tot + 10.0
    if bewertung < 1:
        bewertung = 1

    return bewertung

if __name__ =='__main__':

    res = emission(9.371279099540738,47.42323136334888, 100.0)
    print(f"der score beträgt: {res}")
    print(emission(9.364279099540738,47.42443136334888, 100.0))
