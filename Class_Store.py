from pico2d import *
from Class_stage import *

class Store:
    def __init__(self, stage):
        self.stage = stage
        self.image = load_image('store_sheet.png')
        self.element_image = load_image('store_element_sheet.png')
        self.x = self.stage.width // 2 + 100
        self.y = self.stage.height // 2 - 75

        self.store_onoff = False

    def draw(self):
        self.image.clip_draw(0, 0, 227, 341, self.x, self.y, 300, 500)
    def store_draw(self):
        if self.store_onoff:
            # 기본 창 형성
            self.element_image.clip_draw(0, 170, 210, 170, self.stage.width // 2, self.stage.height // 2, 1400, 600)

    def store_click(self, mx, my):
        if self.stage.special_stage and mx >= self.x - 150 and mx <= self.x + 150 and my >= self.y - 250 and my <= self.y + 250:
            self.store_onoff = True
