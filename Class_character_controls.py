from pico2d import *
from Class_Character_main import *

# 상태 변환 함수
def change_state(pre_state, cur_state, new_state, Input):
    # 달리기
    if new_state == 'Running':
        if cur_state == 'Jumping':
            if Input == 'a':
                character.change_direction_left()  # 왼쪽
            elif Input == 'd':
                character.change_direction_right()  # 오른쪽
            character.ignore_stand = False
            return
        if cur_state == 'Running':
            character.ignore_stand = True
        if Input == 'a': character.change_direction_left() # 왼쪽
        elif Input == 'd': character.change_direction_right() # 오른쪽
        if cur_state != 'Jumping': character.start_running() # 점프 중이 아닐 때만 달리기 수행
    # 서기
    if new_state == 'Standing':
        if cur_state == 'Jumping': return # 점프 중일 때는 서있기 상태로 전환 불가
        if character.ignore_stand: # 부드러운 방향 전환을 위한 처리
            character.ignore_stand = False
            return
        else: character.start_stand()
    # 점프
    if new_state == 'Jumping':
        if cur_state == 'Jumping' or cur_state == 'Attacking': return
        else: character.start_jump_and_down()
    # 공격
    if new_state == 'Attacking':
        if cur_state == 'Jumping' or cur_state == 'Attacking': return
        if Input == 'j': character.start_basic_attack() # 기본 공격
        elif Input == 'u': character.start_skill1_attack() # 스킬1
        elif Input == 'i': character.start_skill2_attack() # 스킬2
    # 대쉬
    if new_state == 'Dashing':
        if cur_state == 'Dashing' or cur_state == 'Jumping': return
        else: character.start_dash()

    # 캐릭터 현재 상태 최신화
    character.pre_state = cur_state
    character.cur_state = new_state

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
            change_state(character.pre_state, character.cur_state, 'Running', 'a')
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            change_state(character.pre_state, character.cur_state, 'Running', 'd')
        # 제자리 서기
        elif event.type == SDL_KEYUP and (event.key == SDLK_a or event.key == SDLK_d):
            change_state(character.pre_state, character.cur_state, 'Standing', '')
        # 점프 및 착지
        elif event.type == SDL_KEYDOWN and event.key == SDLK_k:
            change_state(character.pre_state, character.cur_state, 'Jumping', 'k')
        # 기본 공격
        elif event.type == SDL_KEYDOWN and event.key == SDLK_j:
            change_state(character.pre_state, character.cur_state, 'Attacking', 'j')
        # skill1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_u:
            change_state(character.pre_state, character.cur_state, 'Attacking', 'u')
        # skill2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            change_state(character.pre_state, character.cur_state, 'Attacking', 'i')
        # 대쉬
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
            change_state(character.pre_state, character.cur_state, 'Dashing', 'l')
        # 포탈 (이건 상태로 취급하지 않음)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            character.taking_portal()

# 캐릭터 상태 업데이트
def Character_update():
    # 히트 박스
    hitbox_size = 50
    character.hx1 = character.x - hitbox_size
    character.hy1 = character.y + hitbox_size
    character.hx2 = character.x + hitbox_size
    character.hy2 = character.y - hitbox_size
    if character.cur_state == 'Running':
        character.character_move()
    if character.cur_state == 'Jumping':
        character.character_jump()
        if character.pre_state == 'Running': # 캐릭터가 뛰는 중이었다면 이동도 같이 수행하기
            character.character_move()
    if character.cur_state == 'Dashing':
        character.character_dash()
    # 공격 적용 타이밍 적용
    if character.cur_state == 'Attacking':
        if character.attack_version == 0 and character.frame == 3: # 프레임 3에 공격 수행
            character.skill2_turning = 0.0
            character.draw_attack()
        elif character.attack_version == 1 and character.frame == 5 and character.motion == 1: # 프레임 5에 공격 수행
            character.draw_attack()
            character.skill1_Attacking = True
        elif character.attack_version == 2 and character.frame == 1 and character.motion == 0: # 프레임 1에 공격 수행
            character.draw_attack()
            character.skill2_Attacking = True