from pico2d import *
open_canvas()

from Class_Character_main import Character
from Class_stage import Stage
from Class_Store import Store
from Class_character_controls import *
import game_world

character = Character()
character.start_stand()
game_world.add_object(character, 1)
stage = Stage(character)
game_world.add_object(stage, 0)
store = Store(stage, character)
game_world.add_object(store, 2)

# 게임 루프
while True:
    clear_canvas()
    Character_events(character, stage, store)  # 키 입력 우선 처리
    game_world.update()
    game_world.render()
    # store.store_draw(character) # 상점을 열면 캐릭터보다 앞에 그려지도록 하기
    update_canvas()
    delay(0.1)

close_canvas()