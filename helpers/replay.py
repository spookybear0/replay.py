import mouse, keyboard, gd, os
from time import sleep, time
from helpers import file

path = os.path.dirname(os.path.realpath(__file__))
Scene = gd.memory.Scene
LevelType = gd.memory.LevelType
playing_replay = False
recent = []
start_time = time()
started = False

memory = gd.memory.get_state(load=True)
game_manager = memory.get_game_manager()
play_layer = game_manager.get_play_layer()
level = play_layer.get_level_settings().get_level()
level_type = level.get_level_type()
account_manager = memory.get_account_manager()
user_name = account_manager.get_user_name()

def record_input():
    global play_layer
    recorded = []
    mouse.hook(recorded.append)
    # TODO: add keyboard
    while True:
        if play_layer.get_percent() == 0.0:
            play_layer = game_manager.get_play_layer()
        if play_layer.percent >= 100 or play_layer.dead:
            mouse.unhook(recorded.append)
            newrecorded = []
            for r in recorded:
                if isinstance(r, mouse.ButtonEvent) and r.button == "left":
                    newrecorded.append(r)
            return newrecorded

def play_input(input: list):
    mouse.play(input, include_moves=False, include_wheel=False, speed_factor=1.01) #1.01

def play_replay(key, input=None):
    if not input:
        data = [] 
        global recent
        global playing_replay
        global start_time
        playing_replay = True
    else:
        data = []
        for i in input:
            data.append(mouse.ButtonEvent(i[0], i[1], i[2]))
    print("Playing replay")
    keyboard.press_and_release("space")
    while True:
        play_layer = game_manager.get_play_layer()
        if play_layer.percent > 0: 
            sleep(1.5) 
            if data:
                play_input(data)
            else:
                play_input(recent)
            print("Done playing")
            break
    if not data:
        playing_replay = False
keyboard.hook_key("f1", play_replay, True)

def play_replay_file(replayname):
    play_replay(None, file.unpack_replay_file(replayname))

def start_replay_recorder():
    global started
    started = True
    while started:
        play_layer = game_manager.get_play_layer()
        level = play_layer.get_level_settings().get_level()
        level_type = level.get_level_type()
        scene = game_manager.get_scene()
        if scene == Scene.EDITOR_OR_LEVEL or scene == Scene.OFFICIAL_LEVEL:
            play_layer = game_manager.get_play_layer()
            if play_layer.dead or play_layer.percent == 0.0 or play_layer.is_null() or play_layer.percent >= 100 or playing_replay:
                continue
            if level_type != LevelType.SAVED:
                if level_type != LevelType.EDITOR:
                    if level_type != LevelType.OFFICIAL:
                        continue
            if play_layer.percent > 0:
                start_time = time()
                print("Recording...")
                recent = record_input()
                print("Done")
                if play_layer.get_percent() >= 100:
                    def export(key):
                        print("Exporting replay")
                        file.pack_replay_file(recent, f"{user_name} - {level.creator_name} - {level.name}.gdr")
                        try:
                            keyboard.unhook("f2")
                        except KeyError:
                            pass
                    def back(key):
                        try:
                            keyboard.unhook("f2")
                        except KeyError:
                            if not playing_replay:
                                pass
                    keyboard.hook_key("f2", export, True)
                    keyboard.hook_key("esc", back, False)
                continue
            
def stop_replay_recorder():
    global started
    started = False