from pico2d import *
from Class_Character_main import *

# 캐릭터 키 상호작용
def Character_events():
    events = get_events() # 이벤트 받아와서 events에 저장 (상태의 현황보다는 상태의 변화를 체크하기 때문에, 키를 꾹 누르고 있다고 해서 계속해서 이벤트가 발생하게 되는 것은 아님)
    # 때문에 값을 대입하는 것보다는 값의 증감으로 주는 것이 키 전환에 따른 변화를 다루는 것이 좀 더 자연스러워진다. (키가 동시에 눌려서 로직이 꼬이는 경우, 어차피 증감이 이뤄지기 때문에 최종적으로 원하는 결과를 얻어내기가 더욱 쉬워진다.)
    for event in events: # 받아온 이벤트는 리스트로 전달된다. 때문에 for문으로 하나씩 꺼내서 처리
        if event.type == SDL_QUIT: # 창의 X버튼 누르면 종료
            exit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE: # ESC키가 눌리면 종료
            exit()
        # 좌우 이동
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            if character.Running:
                character.ignore_stand = True
            character.change_direction_left()
            if character.Jumping != True: character.draw_running()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            if character.Running:
                character.ignore_stand = True
            character.change_direction_right()
            if character.Jumping != True: character.draw_running()
        elif event.type == SDL_KEYUP and (event.key == SDLK_a or event.key == SDLK_d) and character.Jumping == False:
            if character.ignore_stand:
                character.ignore_stand = False
            else: character.draw_stand()
        # 점프 및 착지
        elif event.type == SDL_KEYDOWN and event.key == SDLK_k and character.Jumping == False:
            character.draw_jump_and_down()
        # 피격
        # 기본 공격
        elif event.type == SDL_KEYDOWN and event.key == SDLK_j and character.Attacking == False:
            character.draw_basic_attack()
        # skill1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_u and character.Attacking == False:
            character.draw_skill1_attack()
        # 대쉬
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l and character.Dashing == False:
            character.draw_dash()
        # skill2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i and character.Attacking == False:
            character.draw_skill2_attack()

# 캐릭터 상태 업데이트
def Character_update():
    if character.Running:
        character.character_move()
    if character.Jumping:
        character.character_jump()
    if character.Dashing:
        character.character_dash()
    if character.Attacking:
        if character.attack_version == 0 and character.frame == 3:
            character.draw_attack()