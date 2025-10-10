from pico2d import *
from Class_Character import *
from Class_character_controls import *

open_canvas()

character = Character()
Character.draw_jump_and_down(character)
while True:
    clear_canvas()
    Character.draw_character(character)
    Character.frame_change(character, 0.1)
    update_canvas()
    delay(0.1)
close_canvas()