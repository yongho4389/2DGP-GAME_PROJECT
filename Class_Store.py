from pico2d import *
from Class_stage import *

class Store:
    def __init__(self, stage):
        self.image = load_image('store_sheet.png')
        self.image = load_image('store_element_sheet.png')
        self.x = stage.width // 2 + 100
        self.y = stage.height // 2 - 75

        self.store_onoff = False

    def draw(self):
        self.image.clip_draw(0, 0, 227, 341, self.x, self.y, 300, 500)

    def click(self, mx, my):
        pass
