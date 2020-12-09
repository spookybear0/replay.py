import json, os, mouse, re

from mouse import click

path = os.path.dirname(os.path.realpath(__file__))
version = "v2"

def packv1(data: list, filename: str):
    open(filename, "w").write(f"v1\n")
    return json.dump(data, open(filename, "a"))

def packv2(data: list, filename: str):
    final = f"{version}\n"
    for d in data:
        clicktype = d[0]
        if clicktype == "up": clicktype = "u"
        elif clicktype == "down": clicktype = "d"
        elif clicktype == "double": clicktype = "dd"
        time = d[2]
        final += f"{clicktype},{time}|"
    return open(filename, "w").write(final)

def unpackv1(data: str):
    input = json.loads(data.split("\n")[1])
    data = []
    for i in input:
        data.append(mouse.ButtonEvent(i[0], i[1], i[2]))
    return data

def unpackv2(data: str):
    final = []
    data = data.split("\n")[1].split("|")[:-1]
    for d in data:
        if d[:2] != "dd" and d[0] == "d": # not double click
            final.append(["down", "left", float(re.findall("[0-9]+.[0-9]+", d)[0])])
        elif d[0] == "u":
            final.append(["up", "left", float(re.findall("[0-9]+.[0-9]+", d)[0])])
        elif d[:2] == "dd":
            final.append(["double", "left", float(re.findall("[0-9]+.[0-9]+", d)[0])])
    return final
    
def unpack_replay_file(filename: str):
    switch = {
        "v1": unpackv1,
        "v2": unpackv2
    }
    version = open(filename, "r").read().split("\n")[0]
    func = switch.get(version)
    if func:
        return func(open(filename, "r").read())
    return

def pack_replay_file(data: list, filename: str):
    switch = {
        "v1": packv1,
        "v2": packv2
    }
    func = switch.get(version)
    if func:
        return func(data, filename)
    return