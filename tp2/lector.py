import json

def leer_json (file_name : str):
    file = open(file_name)
    config = json.load(file)
    return config