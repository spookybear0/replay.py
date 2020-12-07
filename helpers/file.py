import json, os

path = os.path.dirname(os.path.realpath(__file__))

def pack_replay_file(data: dict, filename: str):
    return json.dump(data, open(path + "\\" + filename, "w"))
    
def unpack_replay_file(filename: str):
    return json.load(open(path + "\\" + filename, "r"))