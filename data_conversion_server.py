import sys
import os

from data_conversion import convert


in_file = sys.argv[1]
print(f"Process {in_file}")

file_name = os.path.basename(in_file)
out_path = os.path.join('data/out', file_name)

convert(in_file, out_path)