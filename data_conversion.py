
import pandas as pd

from condition_score import get_condition_score
from kostenschaetzer import cost_estimator


def convert(inp_file, oup_file):
    # Read input data
    inp_data = pd.read_csv(inp_file, sep=',', index_col='id')
    inp_data["renovation"] = None
    # Prepare output Dataframe
    oup_header = ["Latitude", "Longitude", "cheapness", "condition", "location", "score"]
    oup_data = pd.DataFrame(index=inp_data.index, columns=oup_header)
    
    # Convert Latitude and Longitude
    # temp = inp_data["Latitude Longitude"].apply(latlong_from_gmaps)
    # temp = temp.apply(pd.Series)
    oup_data["Latitude"] = inp_data["Latitude"]
    oup_data["Longitude"] = inp_data["Longitude"]
    
    # Calculate cheapness score
    oup_data["cheapness"] = inp_data.apply(lambda x: cost_estimator(x["mietpreis"], x["Flaeche"], x["zimmer"]), axis=1)
    
    # Calculate condition score
    oup_data["condition"] = inp_data.apply(lambda x: get_condition_score(x["baujahr"], x["renovation"]), axis=1)
    
    # Calculate location score
    oup_data["location"] = oup_data.apply(lambda x: dummy_location_score(x["Latitude"], x["Longitude"]), axis=1)
    
    # Calculate overall score
    oup_data["score"] = oup_data.apply(lambda x: get_overall_score(x["cheapness"], x["condition"], x["location"]), axis=1)
    
    # Write DataFrame to csv file
    oup_data.to_csv(oup_file, sep=';')


def dummy_location_score(latitude, longitude):
    return float(int((latitude+longitude) % 10) + 1)


def get_overall_score(cheapness_score, condition_score, location_score):
    return round(0.5*cheapness_score + 0.3*condition_score + 0.2*location_score, 2)


def latlong_from_gmaps(loc_string):
    lat_str, long_str = tuple(loc_string.split(' '))
    dir = {'N': 1.0, 'S': -1.0, 'E': 1.0, 'W': -1.0}
    lat = (float(lat_str[:lat_str.find('°')]) + float(lat_str[lat_str.find('°')+1:lat_str.find("'")])/60 +\
        float(lat_str[lat_str.find("'")+1:lat_str.find('"')])/3600) * dir[lat_str[lat_str.find('"')+1]]
    long = (float(long_str[:long_str.find('°')]) + float(long_str[long_str.find('°')+1:long_str.find("'")])/60 +\
        float(long_str[long_str.find("'")+1:long_str.find('"')])/3600) * dir[long_str[long_str.find('"')+1]]
    return lat, long


if __name__ == "__main__":
    loc_str = """47°26'07.9"N 9°24'04.6"E"""
    lat, long = latlong_from_gmaps(loc_str)
    inp = "data/real_estate_listing.csv"
    oup = "data/data_output.csv"
    
    convert(inp, oup)
