import mouse, keyboard, gd, os
from time import sleep, time
from helpers import replay

path = os.path.dirname(os.path.realpath(__file__))
memory = gd.memory.get_state(load=True)

# my plan is to have notifications
# like "replay exported" or "replay.py started"
# this will make the program better
# I am having some trouble getting the dlls to do this though
# this should stay at false until they are created
dlls = False 

def main():
    if dlls:
        memory.inject_dll(path + "\\dlls\\launch.dll")
    replay.start_replay_recorder()
    
    
if __name__ == "__main__":
    main()