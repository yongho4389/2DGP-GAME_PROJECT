from pico2d import *
import game_framework

image = None

def pause():
    pass

def resume():
    pass

def init():
    global image
    image = load_image('./image_sheets/title.png')

def finish():
    global image
    del image # 메모리 해제


def update():
    pass

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def handle_events():
    events = get_events() # 내부에 필요 없는 이벤트가 쌓이지 않도록 처리
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            import play_mode
            game_framework.change_mode(play_mode)