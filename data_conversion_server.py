import sys
import os

from data_conversion import convert


OUTPUT_DIR = 'data/out/'
INPUT_DIR = 'data/'

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    i = sys.argv[1]
    print(f"Process {i}")
    
    file_name = f"{i}_real_estate_listing.csv"
    out_path = os.path.join(OUTPUT_DIR, file_name)
    in_path = os.path.join(INPUT_DIR, file_name)
    
    convert(in_path, out_path)