from pico2d import *

open_canvas()

character = load_image('character_motion_sheets.png')

frame = 0
motion = 4
while True:
    clear_canvas()
    # 2856 x 1910
    character.clip_draw(frame * (2856 // 8), (motion * 1910 // 5), 2856 // 8, 1910 // 5, 400, 300, 400, 400)
    frame = (frame + 1) % 8
    update_canvas()
    delay(0.2)

close_canvas()