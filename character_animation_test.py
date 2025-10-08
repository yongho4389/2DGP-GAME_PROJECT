from pico2d import *
from Class_Character import Character

open_canvas()

character = Character()
Character.draw_basic_attack(character)
while True:
    clear_canvas()
    Character.draw_character(character)
    Character.frame_update(character)
    update_canvas()

close_canvas()