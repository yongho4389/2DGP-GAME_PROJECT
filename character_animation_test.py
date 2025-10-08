from pico2d import *

open_canvas()

character = load_image('character_motion_sheets.png')

frame = 0
motion = 4
while True:
    clear_canvas()
    # 1288 x 930
    character.clip_draw(frame * (1288 // 8), (motion * 930 // 5), 1288 // 8, 930 // 5, 400, 300)
    frame = (frame + 1) % 8
    update_canvas()
    delay(0.2)

close_canvas()