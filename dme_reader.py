import pickle
import sys
from pprint import pprint

def sort_by_number(x):
    return x[1:-1]

def sort_by_letter(x):
    return x[0]

if len(sys.argv) != 2:
    print(f"USAGE: {sys.argv[0]} [.dme filepath]")
    sys.exit(-1)

try:
    with open(sys.argv[1], 'rb') as open_file:
        save_data = pickle.load(open_file)
except (FileNotFoundError, OSError, PermissionError):
    print(f"Could not open {sys.argv[1]}")
    sys.exit(-2)

if not isinstance(save_data, dict):
    print(f"Could not read data from {sys.argv[1]}\nData is a {type(save_data)}, expected dict")
    sys.exit(-2)

dict_keys = sorted(save_data.keys(), key=sort_by_number)
dict_keys.sort(key=sort_by_letter)

for key in dict_keys:
    print(f"{key}: ", end='')
    pprint(save_data[key])
