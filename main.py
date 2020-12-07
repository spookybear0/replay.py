import mouse, keyboard, gd, os
from time import sleep, time
from helpers import replay

path = os.path.dirname(os.path.realpath(__file__))
memory = gd.memory.get_state(load=True)

def main():
    memory.inject_dll(path + "\\dlls\\launch.dll")
    replay.start_replay_recorder()
    
    
if __name__ == "__main__":
    main()