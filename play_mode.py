from pico2d import *

from Class_Character_main import Character
from Class_stage import Stage
from Class_Store import Store
from Class_monsters import Basic_Monster
from Class_elite_monster import Elite_Monster
from Class_boss_monster import Boss_Monster
from Class_character_controls import *
import game_world
import random

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
    character.start_stand() # 플레이어 초기 상태 설정
    game_world.add_object(character, 2)
    game_world.add_collision_pair('character:monster', character, None) # 몬스터 직접 충돌
    game_world.add_collision_pair('character:elite_monster', character, None)  # 엘리트 몹과의 충돌
    game_world.add_collision_pair('character:boss_monster', character, None)  # 보스 몹과의 충돌

    stage = Stage(character)
    game_world.add_object(stage, 0)

    store = Store(stage, character)
    game_world.add_object(store, 3)

    # 디버깅용 보스 몹 생성
    boss = Boss_Monster(650, 175, 1, stage, character)
    game_world.add_object(boss, 1)
    game_world.add_collision_pair('character:boss_monster', None, boss)

    # 일반 몹 기본 10마리 생성
    # monsters = [Basic_Monster(random.randint(200, 2000), 125, random.choice((-1, 1)), stage, character) for _ in range(10)]
    # game_world.add_objects(monsters, 1)
    # for monster in monsters:
    #     game_world.add_collision_pair('character:monster', None, monster)  # 몬스터 직접 충돌
    #     game_world.add_collision_pair('attack:monster', None, monster)  # 플레이어 공격과 몬스터 충돌 시

    # 엘리트몹 생성 (기본 1마리)
    # elite_monster = Elite_Monster(1200, 175, random.choice((-1, 1)), stage, character)
    # game_world.add_object(elite_monster, 1)
    # game_world.add_collision_pair('character:elite_monster', None, elite_monster)  # 엘리트 몬스터와의 충돌
    # game_world.add_collision_pair('attack:elite_monster', None, elite_monster)  # 플레이어 공격과 몬스터 충돌 시

def update():
    game_world.update()
    game_world.handle_collision()  # 충돌 검사 및 충돌 처리

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass