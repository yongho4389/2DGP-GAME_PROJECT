from pico2d import *

class Stage1:
    def __init__(self):
        self.image = load_image('background_sheets.png')
        self.width = 800
        self.height = 600
        self.w = 3084
        self.h = 1872

    def draw(self):
        # 구름
        self.image.clip_draw(0 * 3084 // 3, 1 * 1872 // 3, 3084 // 3, 1872 // 3, 400, 400, 800, 1000)
        # 나무
        self.image.clip_draw(1 * 3084 // 3, 1 * 1872 // 3, 3084 // 3, 1872 // 3, 400, 400, 800, 1000)
        # 땅
        self.image.clip_draw(2 * 3084 // 3, 1 * 1872 // 3, 3084 // 3, 1872 // 3, 400, 100, 800, 400)

stage1 = Stage1()