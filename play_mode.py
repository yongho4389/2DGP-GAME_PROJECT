from pico2d import *

from Class_Character_main import Character
from Class_stage import Stage
from Class_Store import Store
from Class_character_controls import *
import game_world

import game_framework

boy = None

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            Character_events(character, stage, store, event_list)  # 키 입력 우선 처리

def init():
    global character, stage, store

    character = Character()
    character.start_stand()
    game_world.add_object(character, 1)

    stage = Stage(character)
    game_world.add_object(stage, 0)

    store = Store(stage, character)
    game_world.add_object(store, 2)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass