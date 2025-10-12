from pico2d import *
from Class_camera import *

# 스테이지 관련 클래스 및 함수 정의
class Stage1:
    def __init__(self):
        self.image = load_image('background_sheets.png')
        self.width = 800
        self.height = 600
        self.w = 3084
        self.h = 1872
        self.x = 400
        self.y = 400

    def draw(self):
        # 구름
        self.image.clip_draw(0 * 3084 // 3, 1 * 1872 // 3, 3084 // 3, 1872 // 3, self.x - camera.x, self.y, 800, 1000)
        # 나무
        self.image.clip_draw(1 * 3084 // 3, 1 * 1872 // 3, 3084 // 3, 1872 // 3, self.x - camera.x, self.y, 800, 1000)
        # 땅
        self.image.clip_draw(2 * 3084 // 3, 1 * 1872 // 3, 3084 // 3, 1872 // 3, self.x - camera.x, self.y // 4, 800, 400)

stage1 = Stage1()