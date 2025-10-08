from pico2d import *

open_canvas()

character = load_image('character_running.png')

frame = 0
while True:
    clear_canvas()
    character.clip_draw(frame * 143, 0, 143, 166, 400, 300)
    frame = (frame + 1) % 7
    update_canvas()
    delay(0.1)

close_canvas()