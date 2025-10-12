from pico2d import *
from Class_camera import *

# 일반 스테이지 관련 클래스 및 함수 정의 (사냥터)
class Stage:
    def __init__(self):
        self.image = load_image('background_sheets.png')
        self.store_image = load_image('store_sheet.png')
        self.width = 800
        self.height = 600
        self.w = 3084
        self.h = 2496
        self.x = 400
        self.y = 400
        self.stage_level = 0
        self.special_stage = False # 상점 진입 혹은 보스 스테이지 진입 시 True로 변경

        self.portal_image = load_image('portal_sheet.png')
        self.portal_sx = 0
        self.portal_ex = 800
        self.portal_y = self.height // 2 - 100


    def draw(self):
        # 스테이지
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
        # 상점
        if self.special_stage and self.stage_level < 3:
            self.store_image.clip_draw(0, 0, 227, 341, self.width // 2 + 100, self.height // 2 - 75, 300, 500)
        # 포탈
        if self.stage_level != 3:
            self.portal_sx = camera.start_position + 50
            self.portal_ex = camera.end_position - 50
            # 화면은 어차피 항상 왼쪽이 0좌표다. 때문에 camera.x를 빼줘야 제대로된 위치에 포탈이 그려진다.
            self.portal_image.clip_draw(0, 0, 128, 256, self.portal_sx - camera.x, self.portal_y, 100, 300)
            self.portal_image.clip_draw(0, 0, 128, 256, self.portal_ex - camera.x, self.portal_y, 100, 300)


stage = Stage()
