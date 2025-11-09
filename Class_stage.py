from pico2d import *
from Class_camera import camera

# 일반 스테이지 관련 클래스 및 함수 정의 (사냥터)
class Stage:
    def __init__(self, character):
        self.image = load_image('./image_sheets/background_sheets.png')
        self.store_image = load_image('./image_sheets/store_sheet.png')
        self.width = 800
        self.height = 600
        self.w = 3084
        self.h = 2496
        self.x = 400
        self.y = 400
        self.store_pos_x = self.width // 2 + 100
        self.store_pos_y = self.height // 2 - 75
        self.stage_level = 0 # 보스 스테이지는 3
        self.special_stage = False # 상점 진입 혹은 보스 스테이지 진입 시 True로 변경

        self.portal_image = load_image('./image_sheets/portal_sheet.png')
        self.portal_sx = 0
        self.portal_ex = 800
        self.portal_y = self.height // 2 - 100

        self.character = character

    # 카메라 범위 최신화 (스테이지에 따른 카메라의 허용 범위 설정)
    def set_camera_stage_range(self):
        if self.special_stage:
            camera.start_position = 0
            camera.end_position = self.width
        else:
            camera.start_position = 0
            camera.end_position = (self.width * 3) - 40

    def draw(self):
        # 카메라 범위 최신화
        self.set_camera_stage_range()
        # 스테이지
        if self.special_stage: # 특수 스테이지인 경우 맵 크기는 1배
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
        # 포탈
        if self.stage_level != 3:
            self.portal_sx = camera.start_position + 50
            self.portal_ex = camera.end_position - 50
            # 화면은 어차피 항상 왼쪽이 0좌표다. 때문에 camera.x를 빼줘야 제대로된 위치에 포탈이 그려진다.
            self.portal_image.clip_draw(0, 0, 128, 256, self.portal_sx - camera.x, self.portal_y, 100, 300)
            self.portal_image.clip_draw(0, 0, 128, 256, self.portal_ex - camera.x, self.portal_y, 100, 300)
        # 상점
        if self.special_stage and self.stage_level < 3:
            self.store_image.clip_draw(0, 0, 227, 341, self.store_pos_x, self.store_pos_y, 300, 500)

    # 포탈 이동 처리
    def taking_portal(self):
        if self.stage_level == 3:
            return # 보스 스테이지에서는 포탈 무시
        # 좌측 끝 포탈
        if self.portal_sx >= self.character.get_bb()[0] and self.portal_sx <= self.character.get_bb()[2]:
            if self.stage_level == 0 and not self.special_stage:
                return # 0레벨 일반 스테이지에서 좌측 포탈은 무시
            # 상점 스테이지에서 이전으로 돌아가는 경우
            if self.special_stage:
                self.special_stage = False
                # 스테이지 변경 후 카메라 범위 최신화
                self.set_camera_stage_range()
                # 플레이어 위치 일반 스테이지의 우측 끝으로 보정
                self.character.x = (self.width * 3 - 40) - 50
            else:
                self.stage_level -= 1
                self.special_stage = True
                self.set_camera_stage_range()
                # 플레이어 위치 스페셜 스테이지의 우측 끝으로 보정
                self.character.x = self.width - 50
        # 우측 끝 포탈
        elif self.portal_ex >= self.character.get_bb()[0] and self.portal_ex <= self.character.get_bb()[2]:
            # 일반 스테이지에서 다음으로 넘어가는 경우 스페셜 스테이지로 전환
            if not self.special_stage:
                self.special_stage = True
            # 상점 스테이지라면 다음 레벨로 진입
            else:
                self.stage_level += 1
                self.special_stage = False
                self.set_camera_stage_range()
            # 보스 스테이지 또한 스페셜 스테이지로 전환
            if self.stage_level == 3:
                self.special_stage = True
                self.set_camera_stage_range()
            # 플레이어 위치 좌측 끝으로 보정
            self.character.x = camera.start_position + 50

    def update(self):
        pass
