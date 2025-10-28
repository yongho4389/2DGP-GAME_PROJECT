from pico2d import *
open_canvas()

from Class_Character_main import *
from Class_stage import *
from Class_character_controls import *

# 메인 캐릭터 처리
def Main_character_loop():
    Character_events()  # 키 입력 우선 처리
    character.update()  # 캐릭터 상태 처리
    # 스킬 지속 시간 처리
    if character.skill1_Attacking or character.skill2_Attacking:
        character.attack.skill_update(0.1)
    character.frame_change(0.1)  # 프레임 전환 처리
    character.draw_character()  # 캐릭터 최종 상태 출력

# 게임 루프
while True:
    clear_canvas()
    stage.draw()
    Main_character_loop()
    store.store_draw(character) # 상점을 열면 캐릭터보다 앞에 그려지도록 하기
    update_canvas()
    delay(0.1)

close_canvas()