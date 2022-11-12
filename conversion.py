
import pandas as pd


def convert(inp_file, oup_file):
    # Read input data
    inp_data = pd.read_csv(inp_file, sep=';', index_col='id')
    # Prepare output Dataframe
    oup_header = ["Latitude", "Longitude", "cheapness", "condition", "location", "score"]
    oup_data = pd.DataFrame(index=inp_data.index, columns=oup_header)
    
    # Convert Latitude and Longitude
    oup_data.loc[:, ["Latitude", "Longitude"]] = inp_data["lat_long_string"].apply(latlong_from_gmaps).apply(pd.Series)
    
    # Write DataFrame to csv file
    oup_data.to_csv(oup_file, sep=';')


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
    oup = "data/test_output.csv"
    
    convert(inp, oup)
