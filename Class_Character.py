# 주인공 캐릭터 관련 클래스 및 함수 정의
from pico2d import *

class Character:
    def __init__(self):
        self.image = load_image('character_motion_sheets.png')
        self.frame = 0
        self.start_frame = 3 # 프레임 시작 인덱스
        self.end_frame = 3 # 프레임 종료 인덱스
        self.motion = 0  # 기본 서있기
        # 위치
        self.x = 400
        self.y = 300
        # 크기
        self.width = 100
        self.height = 100
        # animation sheet 크기
        self.sheet_width = 2856
        self.sheet_height = 1910

    def set_motion(self, motion):
        self.motion = motion

    def update(self):
        self.frame = (self.frame + 1) % 8

    # 달리기 모션
    def draw_running(self):
        self.motion = 4
        self.start_frame = 0
        self.end_frame = 7

    # 점프 및 착지
    def draw_jump_and_down(self):
        self.motion = 3
        self.start_frame = 0
        self.end_frame = 3

    # 피격
    def draw_attacked(self):
        self.motion = 3
        self.start_frame = 4
        self.end_frame = 5

    # 기본 공격
    def draw_basic_attack(self):
        self.motion = 2
        self.start_frame = 0
        self.end_frame = 5

    # 스킬1 공격
    def draw_skill1_attack(self):
        self.motion = 1
        self.start_frame = 0
        self.end_frame = 6

    # 대쉬
    def draw_dash(self):
        self.motion = 0
        self.start_frame = 0
        self.end_frame = 0

    # 스킬2 공격
    def draw_skill2_attack(self):
        self.motion = 0
        self.start_frame = 1
        self.end_frame = 2

    # 서있기
    def draw_stand(self):
        self.motion = 0
        self.start_frame = 3
        self.end_frame = 3
    
    # 캐릭터 그리기
    def draw_character(self):
        self.image.clip_draw(self.frame * (self.sheet_width // 8), (self.motion * self.sheet_height // 5), # 시트상 위치
                             self.sheet_width // 8, self.sheet_height // 5, # 시트상 크기
                             self.x, self.y, # 월드 위치
                             self.width, self.height)