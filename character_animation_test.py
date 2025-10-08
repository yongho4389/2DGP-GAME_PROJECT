from pico2d import *

open_canvas()

character = load_image('character_motion_sheets.png')

frame = 0
motion = 0
while True:
    clear_canvas()
    # 1040 x 1488
    character.clip_draw(frame * (1040 // 7), (motion * 1488 // 8), 1040 // 7, 1488 // 8, 400, 300)
    frame = (frame + 1) % 7
    if frame == 0: motion += 1
    update_canvas()
    delay(0.1)

close_canvas()