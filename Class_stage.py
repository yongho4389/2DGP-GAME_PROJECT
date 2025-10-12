from pico2d import *
from Class_camera import *

# 일반 스테이지 관련 클래스 및 함수 정의 (사냥터)
class Normal_Stage:
    def __init__(self):
        self.image = load_image('background_sheets.png')
        self.width = 800
        self.height = 600
        self.w = 3084
        self.h = 2496
        self.x = 400
        self.y = 400
        self.stage_level = 3
        self.special_stage = True

    def draw(self):
        if self.special_stage: # 특수 스테이지인 경우 맵 크기는 1배
            # 카메라 위치 최신화
            camera.start_position = 0
            camera.end_position = self.width
            # 구름
            self.image.clip_draw(0 * self.w // 3, (3 - self.stage_level) * self.h // 4,
                                 self.w // 3, self.h // 4,
                                 self.x, self.y,
                                 self.width, 1000)
            # 나무
            self.image.clip_draw(1 * self.w // 3, (3 - self.stage_level) * self.h // 4,
                                 self.w // 3, self.h // 4,
                                 self.x, self.y,
                                 self.width, 1000)
            # 땅
            self.image.clip_draw(2 * self.w // 3, (3 - self.stage_level) * self.h // 4,
                                 self.w // 3, self.h // 4,
                                 self.x, self.y // 4,
                                 self.width, 400)
        else:
            # 카메라 위치 최신화
            camera.start_position = 0
            camera.end_position = (self.width * 3) - 40
            for i in range(3):
                # 구름
                self.image.clip_draw(0 * self.w // 3, (3 - self.stage_level) * self.h // 4,
                                     self.w // 3, self.h // 4,
                                     (i * (self.width - 20)) + self.x - camera.x, self.y,
                                     self.width, 1000)
                # 나무
                self.image.clip_draw(1 * self.w // 3, (3 - self.stage_level) * self.h // 4,
                                     self.w // 3, self.h // 4,
                                     (i * (self.width - 20)) + self.x - camera.x, self.y,
                                     self.width, 1000)
                # 땅
                self.image.clip_draw(2 * self.w // 3, (3 - self.stage_level) * self.h // 4,
                                     self.w // 3, self.h // 4,
                                     (i * (self.width - 20)) + self.x - camera.x, self.y // 4,
                                     self.width, 400)

stage = Normal_Stage()