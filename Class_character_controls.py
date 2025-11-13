from pico2d import *

# 상태 변환 함수
def change_state(character, pre_state, cur_state, new_state, Input):
    if character.cur_state == 'is_attacked': return # 피격 상태일 때는 조종 불가
    # 달리기
    if new_state == 'Running':
        if cur_state == 'Running' or cur_state == 'Jumping': # 이미 달리고 있거나 점프 중이면 다음 키입력을 통한 서있기를 무시 (부드러운 방향 전환 처리)
            character.ignore_stand = True
        if Input == 'a': character.change_direction_left() # 왼쪽
        elif Input == 'd': character.change_direction_right() # 오른쪽
        if cur_state != 'Jumping':
            character.start_running() # 점프 중이 아닐 때만 달리기 수행
            # 점프 중이 아니라면 현재 상태를 달리기로 변경, 그렇지 않다면 점프 중에 방향 전환만 된 것이므로 상태 변경은 하지 않음
            character.pre_state = cur_state
            character.cur_state = new_state
        return
    # 서기
    if new_state == 'Standing':
        if character.ignore_stand: # 부드러운 방향 전환을 위한 처리
            character.ignore_stand = False
            return
        else: character.start_stand()
    # 점프
    if new_state == 'Jumping':
        if cur_state == 'Jumping' or cur_state == 'Attacking': return
        else:
            character.start_jump_and_down()
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
def Character_events(character, stage, store, events=None):
    # 이벤트 받아와서 events에 저장 (상태의 현황보다는 상태의 변화를 체크하기 때문에, 키를 꾹 누르고 있다고 해서 계속해서 이벤트가 발생하게 되는 것은 아님)
    # 때문에 값을 대입하는 것보다는 값의 증감으로 주는 것이 키 전환에 따른 변화를 다루는 것이 좀 더 자연스러워진다. (키가 동시에 눌려서 로직이 꼬이는 경우, 어차피 증감이 이뤄지기 때문에 최종적으로 원하는 결과를 얻어내기가 더욱 쉬워진다.)
    for event in events: # 받아온 이벤트는 리스트로 전달된다. 때문에 for문으로 하나씩 꺼내서 처리
        # 좌우 이동
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            change_state(character, character.pre_state, character.cur_state, 'Running', 'a')
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            change_state(character, character.pre_state, character.cur_state, 'Running', 'd')
        # 제자리 서기
        elif event.type == SDL_KEYUP and (event.key == SDLK_a or event.key == SDLK_d):
            change_state(character, character.pre_state, character.cur_state, 'Standing', '')
        # 점프 및 착지
        elif event.type == SDL_KEYDOWN and event.key == SDLK_k:
            change_state(character, character.pre_state, character.cur_state, 'Jumping', 'k')
        # 기본 공격
        elif event.type == SDL_KEYDOWN and event.key == SDLK_j:
            change_state(character, character.pre_state, character.cur_state, 'Attacking', 'j')
        # skill1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_u:
            change_state(character, character.pre_state, character.cur_state, 'Attacking', 'u')
        # skill2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            change_state(character, character.pre_state, character.cur_state, 'Attacking', 'i')
        # 대쉬
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
            change_state(character, character.pre_state, character.cur_state, 'Dashing', 'l')
        # 포탈 (이건 상태로 취급하지 않음)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            stage.taking_portal()
        # 상점 관련 클릭
        elif event.type == SDL_MOUSEBUTTONDOWN:
            # x축은 그대로, y축은 아래가 0이 되도록 화면 크기에서 빼주기 (윈도우 좌표에서 pico2d 좌표계로 변경)
            mouse_x, mouse_y = event.x, stage.height - event.y
            store.store_click(mouse_x, mouse_y, character)

