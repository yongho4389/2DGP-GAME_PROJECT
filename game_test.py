from pico2d import *
open_canvas()

from Class_Character_main import *
from Class_character_controls import *


# character.draw_running()
# 게임 루프
while True:
    clear_canvas()
    Character_events()
    character.draw_character()
    character.frame_change(0.1)
    update_canvas()
    delay(0.1)
close_canvas()