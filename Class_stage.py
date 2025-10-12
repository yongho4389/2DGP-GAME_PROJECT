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
        camera.start_position = 0
        camera.end_position = self.width * 3 - 40
        for i in range(3):
            # 구름
            self.image.clip_draw(0 * self.w // 3, 1 * self.h // 3, self.w // 3, self.h // 3, (i * self.width - 20) + self.x - camera.x, self.y, self.width, 1000)
            # 나무
            self.image.clip_draw(1 * self.w // 3, 1 * self.h // 3, self.w // 3, self.h // 3, (i * self.width - 20) + self.x - camera.x, self.y, self.width, 1000)
            # 땅
            self.image.clip_draw(2 * self.w // 3, 1 * self.h // 3, self.w // 3, self.h // 3, (i * self.width - 20) + self.x - camera.x, self.y // 4, self.width, 400)

stage1 = Stage1()