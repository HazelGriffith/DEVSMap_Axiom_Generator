import json

#filename = input("Enter atomic model filename: ")
filename = 'DEVSMap_Files/counter_atomic.json'
with open(filename) as jfile:
    model = json.load(jfile)
print(model)