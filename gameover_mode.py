from pico2d import *
import game_framework
import title_mode

image = None
intro_start_time = 0.0

def pause():
    pass

def resume():
    pass

def init():
    global image, intro_start_time
    image = load_image('./image_sheets/game_over.png')
    intro_start_time = get_time()

def finish():
    global image
    del image # 메모리 해제


def update():
    # clear 모드가 2초간 지속
    global intro_start_time
    if get_time() - intro_start_time > 2.0:
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def handle_events():
    events = get_events() # 내부에 필요 없는 이벤트가 쌓이지 않도록 처리