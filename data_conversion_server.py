import sys
import os
from multiprocessing import Process
from data_conversion import convert


OUTPUT_DIR = 'data/out/'
INPUT_DIR = 'data/'

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    processes = []
    for i in range(0, 8):
        print(f"Process {i}")
        
        file_name = f"{i}_real_estate_listing.csv"
        out_path = os.path.join(OUTPUT_DIR, file_name)
        in_path = os.path.join(INPUT_DIR, file_name)
        
        proc = Process(target=convert, args=(in_path, out_path))
        proc.start()
        processes.append(proc)
        
        
    for proc in processes:
        proc.join()