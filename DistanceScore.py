# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 10:49:08 2022

@author: Plehn
"""

import json
import requests
import pandas as pd
import numpy as np

#Importieren der Point of Interest CSV Daten in Pandas Dataframe
POI = pd.read_csv('data/POI.csv', sep=';', engine='python', encoding='utf-8-sig', usecols=[0,1,2], index_col=False)

#CSV Gewichtungen importieren und in dict speichern
Gewichtung = pd.read_csv('data/GewichtungDistanzen.csv', sep=';', engine='python', encoding='utf-8-sig', usecols=[0,1], index_col=False)
Faktoren = {row[0]: row[1] for index, row in Gewichtung.iterrows()}

def getDistance(GeoStart, GeoZiel):
    """
    Findet die kürzeste Strassendistanz zwischen zwei Koordinaten

    Parameters
    ----------
    GeoStart : str
        latitude,longitude
        Beispiel: 47.423207,9.370148.
    GeoZiel : str
        latitude,longitude
        Beispiel: 47.423207,9.370148.

    Returns
    -------
    distance : float
        Kürzeste Distanz.

    """
    lat_1 = GeoStart.split(',')[0].replace(' ','')
    lon_1 = GeoStart.split(',')[1].replace(' ','')
    lat_2 = GeoZiel.split(',')[0].replace(' ','')
    lon_2 = GeoZiel.split(',')[1].replace(' ','')

    payload = {"steps":"false","geometries":"geojson", 'alternatives':'true'}
    r = requests.get(f"http://router.project-osrm.org/route/v1/car/{lon_1},{lat_1};{lon_2},{lat_2}?overview=false",params=payload)
    data = r.json()
    distance = data['routes'][0]['distance']
    return distance


def findNearest(GeoImmo, data):
    """
    Findet die nächste Auto-Routen-Distanz von der Immobilien Koordinate zu den Koordinaten einer Kategorie

    Parameters
    ----------
    GeoImmo : str
        latitude,longitude
        Beispiel: 47.423207,9.370148
    data : pandas dataframe
        row mit Geo Point Daten

    Returns
    -------
    near : float
        Strassen Distanz von Immobilie zu Ziel Koordinate.

    """

    near = 99999999
    bez = 'xxx'

    for index, row in data.iterrows():
        dis = getDistance(GeoImmo, row['Geo Point'])
        if dis < near:
            near = dis
            bez = row['Bezeichnung']
    return near

def getMeanDistance(GeoImmo):
    #Panda Dataframe pro Kategorie erstellen
    GeoKindergarten = POI[POI['Kategorie']=='Kindergarten']
    GeoPrimarschule = POI[POI['Kategorie']=='Primarschule']
    GeoObersufe = POI[POI['Kategorie']=='Obersufenschulhaus']
    GeoSupermarkt = POI[POI['Kategorie']=='Supermarkt']
    #Koordinaten Hauptbahnhof
    bhf = '47.423207,9.370148'

    #Nächste Distanz in den jeweiligen Kategorien ermitteln und in dict speichern
    Entfernungen = {}
    Entfernungen['Kindergarten']=findNearest(GeoImmo, GeoKindergarten)
    Entfernungen['Primarschule']=findNearest(GeoImmo, GeoPrimarschule)
    Entfernungen['Sekundarschule']=findNearest(GeoImmo, GeoObersufe)
    Entfernungen['Supermarkt']=findNearest(GeoImmo, GeoSupermarkt)
    Entfernungen['Bahnhof']=getDistance(GeoImmo, bhf)

    #Durchschnittliche Distanz mit Einbezug der Faktoren
    summe = Faktoren['Kindergarten']*Entfernungen['Kindergarten']+Faktoren['Primarschule']*Entfernungen['Primarschule']+Faktoren['Sekundarschule']*Entfernungen['Sekundarschule']+Faktoren['Supermarkt']*Entfernungen['Supermarkt']+Faktoren['Bahnhof']*Entfernungen['Bahnhof']
    schnitt=summe/(sum(Faktoren.values()))
    return schnitt


def calculate_distanceScore(distances, laerm):
    minimum = np.min(distances)
    maximum = np.max(distances)
    m = 9 / (maximum - minimum)
    
    dist_score = 10-m*(distances-minimum)
    return 0.5*dist_score + 0.5*laerm

def get_CSV_DistanceScore(latitude, longitude):
    """
    Erstellt CSV mit DistanceScore

    Parameters
    ----------
    koordinaten : pd.Dataframe
        Beispiel: {'Koordinaten': ['47.42283125565918,9.37337852509716',]}.
    data_path_POI : str
        datapath to POI.csv.
    data_path_Gewichtung : str
        datapath to GewichtungDistanzen.csv.

    Returns
    -------
    None.

    """
    print("please wait...")
    return getMeanDistance(f"{latitude},{longitude}")






def main(data_path_POI, data_path_Gewichtung, GeoImmo):
    # schnitt = getMeanDistance(data_path_POI, data_path_Gewichtung, GeoImmo)
    # print(schnitt)

    Data = pd.DataFrame({'Koordinaten': ['47.42283125565918,9.37337852509716','47.42115683400792,9.370368424282155',
                                         '47.41739674828894,9.364164058707637','47.4230201636535,9.369918996053677',
                                          '47.42306361814118,9.392078588056503']})

    get_CSV_DistanceScore(Data, data_path_POI, data_path_Gewichtung)






if __name__ == '__main__':
    main('POI.csv', 'GewichtungDistanzen.csv', '47.401401, 9.295019')
