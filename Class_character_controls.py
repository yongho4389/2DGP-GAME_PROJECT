from pico2d import *
from Class_Character_main import *

def Character_events():
    events = get_events() # 이벤트 받아와서 events에 저장 (상태의 현황보다는 상태의 변화를 체크하기 때문에, 키를 꾹 누르고 있다고 해서 계속해서 이벤트가 발생하게 되는 것은 아님)
    # 때문에 값을 대입하는 것보다는 값의 증감으로 주는 것이 키 전환에 따른 변화를 다루는 것이 좀 더 자연스러워진다. (키가 동시에 눌려서 로직이 꼬이는 경우, 어차피 증감이 이뤄지기 때문에 최종적으로 원하는 결과를 얻어내기가 더욱 쉬워진다.)
    for event in events: # 받아온 이벤트는 리스트로 전달된다. 때문에 for문으로 하나씩 꺼내서 처리
        # 다음 이벤트들을 통해 running을 False로 바꿔 종료시킨다.
        # event.type으로 이벤트 종류를 알 수 있다.
        # 이벤트 타입은 다양한 것들이 존재한다.
        # event.key로 눌린 키를 알 수 있다.
        # 키 입력은 https://wiki.libsdl.org/SDL3/SDL_Keycode 사이트를 참고
        if event.type == SDL_QUIT: # 창의 X버튼 누르면 종료
            exit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE: # ESC키가 눌리면 종료
            exit()
        # 좌우 이동
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            character.change_direction_left()
            character.draw_running()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            character.change_direction_right()
            character.draw_running()
        elif event.type == SDL_KEYUP and (event.key == SDLK_a or event.key == SDLK_d):
            character.motion = 0
            character.draw_stand()